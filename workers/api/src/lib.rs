//! MyStudy v2 API worker (Phase 1 scaffold).
//!
//! Routes (architecture §2, §4, §6):
//!   GET  /api/health
//!   POST /api/auth/register-start   (creates the account + TOTP secret, unusable until verified)
//!   POST /api/auth/totp-verify     (compulsory TOTP step that activates the account)
//!   POST /api/auth/login           (password, then TOTP code or recovery code)
//!   GET  /api/news                 (published News only)
//!   GET  /api/news/:slug           (single post; lazy-publishes due scheduled posts)
//!   POST /api/admin/news           (admin only; P2 insert — Phase 1 validates + returns 501)
//! Any other path is served from the ASSETS binding (the React SPA).
//!
//! Envelope: every API response is `{ "ok": bool, "data": ..., "error": { "code", "message" } }`.
//! Premium is never decided here from a client flag — it is read from
//! D1 (`users.premium_status`) per request (architecture §4).

mod auth;
mod security_questions;
mod totp;

use serde::Deserialize;
use serde_json::{json, Value};
use wasm_bindgen::JsValue;
use worker::*;

#[derive(Debug, Deserialize)]
struct UserRow {
    id: i64,
    // Kept for P2 handlers (password reset, admin user view); not read in Phase 1.
    #[allow(dead_code)]
    email: String,
    #[allow(dead_code)]
    name: String,
    password_hash: String,
    totp_secret_enc: Option<String>,
    totp_enabled: i64,
    recovery_codes_hash: String,
    role: String,
    premium_status: String,
}

#[derive(Debug, Deserialize)]
struct NewsRow {
    slug: String,
    title: String,
    excerpt: Option<String>,
    body_html: String,
    featured_image_url: Option<String>,
    category: Option<String>,
    tags_json: String,
    seo_title: Option<String>,
    seo_description: Option<String>,
    published_at: Option<String>,
    toc_json: String,
}

#[derive(Debug, Deserialize)]
struct SessionRow {
    // user_id/premium_status are read by P2 premium-gated handlers;
    // Phase 1 only needs the role. Kept so the session query stays stable.
    #[allow(dead_code)]
    user_id: i64,
    role: String,
    #[allow(dead_code)]
    premium_status: String,
}

fn json_ok(status: u16, data: Value) -> Result<Response> {
    Response::from_json(&json!({ "ok": true, "data": data, "error": null }))
        .map(|r| r.with_status(status))
}

fn json_err(status: u16, code: &str, message: &str) -> Result<Response> {
    Response::from_json(
        &json!({ "ok": false, "data": null, "error": { "code": code, "message": message } }),
    )
    .map(|r| r.with_status(status))
}

fn now_iso() -> String {
    let ms = js_sys::Date::now();
    let d = js_sys::Date::new(&wasm_bindgen::JsValue::from_f64(ms));
    d.to_iso_string().as_string().unwrap_or_default()
}

fn session_cookie(token: &str) -> String {
    format!(
        "mystudy_session={}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800",
        token
    )
}

fn session_token_from(req: &Request) -> Option<String> {
    if let Ok(auth) = req.headers().get("Authorization") {
        if let Some(auth) = auth {
            if let Some(t) = auth.strip_prefix("Bearer ") {
                return Some(t.to_string());
            }
        }
    }
    let cookie = req.headers().get("Cookie").ok()??;
    for part in cookie.split(';') {
        let part = part.trim();
        if let Some(v) = part.strip_prefix("mystudy_session=") {
            return Some(v.to_string());
        }
    }
    None
}

async fn current_session(db: &D1Database, req: &Request) -> Result<Option<SessionRow>> {
    let token = match session_token_from(req) {
        Some(t) => t,
        None => return Ok(None),
    };
    let hash = auth::sha256_hex(&token);
    let row = db
        .prepare(
            "SELECT s.user_id AS user_id, u.role AS role, u.premium_status AS premium_status \
             FROM sessions s JOIN users u ON u.id = s.user_id \
             WHERE s.token_hash = ?1 AND s.revoked = 0 AND s.expires_at > datetime('now')",
        )
        .bind(&[JsValue::from_str(&hash)])?
        .first::<SessionRow>(None)
        .await?;
    Ok(row)
}

async fn create_session(db: &D1Database, user_id: i64) -> Result<String> {
    let (token, hash) = auth::new_session_token()
        .map_err(|e| Error::RustError(format!("session token: {e}")))?;
    db.prepare(
        "INSERT INTO sessions (user_id, token_hash, expires_at) \
         VALUES (?1, ?2, datetime('now', '+7 days'))",
    )
    .bind(&[
        JsValue::from_f64(user_id as f64),
        JsValue::from_str(&hash),
    ])?
    .run()
    .await?;
    Ok(token)
}

async fn body_json(mut req: Request) -> Result<Value> {
    req.json::<Value>()
        .await
        .map_err(|_| Error::RustError("invalid JSON body".to_string()))
}

fn bad_request(msg: &str) -> Result<Response> {
    json_err(400, "bad_request", msg)
}

// ---------------------------------------------------------------- auth

async fn register_start(db: &D1Database, req: Request) -> Result<Response> {
    let body = body_json(req).await?;
    let name = body["name"].as_str().unwrap_or("").trim();
    let email = body["email"].as_str().unwrap_or("").trim().to_lowercase();
    let password = body["password"].as_str().unwrap_or("");
    let exam_target = body["exam_target"].as_str().unwrap_or("JAMB");
    let questions = body["security_questions"].as_array();

    if name.is_empty() {
        return bad_request("Full name is required.");
    }
    if !email.contains('@') || email.len() < 5 {
        return bad_request("A valid email address is required.");
    }
    if password.len() < auth::PASSWORD_MIN_LEN {
        return bad_request("Password must be at least 12 characters.");
    }
    let questions = match questions {
        Some(q) if q.len() == 3 => q,
        _ => return bad_request("Pick exactly 3 security questions."),
    };
    let mut seen: Vec<&str> = Vec::new();
    let mut qa: Vec<(String, String)> = Vec::new();
    for item in questions {
        let qid = item["question"].as_str().unwrap_or("");
        let ans = security_questions::normalize_answer(item["answer"].as_str().unwrap_or(""));
        if !security_questions::is_valid_question(qid) {
            return bad_request("Unknown security question.");
        }
        if seen.contains(&qid) {
            return bad_request("Each security question must be different.");
        }
        if ans.len() < 2 {
            return bad_request("Each security answer must be at least 2 characters.");
        }
        seen.push(qid);
        qa.push((qid.to_string(), ans));
    }

    let existing = db
        .prepare("SELECT id FROM users WHERE email = ?1")
        .bind(&[JsValue::from_str(&email)])?
        .first::<Value>(None)
        .await?;
    if existing.is_some() {
        return json_err(409, "email_taken", "An account with this email already exists.");
    }

    let password_hash = auth::hash_password(password)
        .map_err(|e| Error::RustError(format!("hash password: {e}")))?;
    let a1 = auth::hash_security_answer(&qa[0].1)
        .map_err(|e| Error::RustError(format!("hash answer: {e}")))?;
    let a2 = auth::hash_security_answer(&qa[1].1)
        .map_err(|e| Error::RustError(format!("hash answer: {e}")))?;
    let a3 = auth::hash_security_answer(&qa[2].1)
        .map_err(|e| Error::RustError(format!("hash answer: {e}")))?;
    let totp_secret = totp::generate_totp_secret()
        .map_err(|e| Error::RustError(format!("totp secret: {e}")))?;
    let (recovery_codes, recovery_hash_json) = auth::generate_recovery_codes()
        .map_err(|e| Error::RustError(format!("recovery codes: {e}")))?;
    // TODO (P2): encrypt totp_secret at rest (AES-GCM, key in a Cloudflare
    // secret). Phase 1 stores the base32 secret in totp_secret_enc as-is.
    let result = db
        .prepare(
            "INSERT INTO users (email, name, password_hash, totp_secret_enc, totp_enabled, \
             recovery_codes_hash, security_q1, security_q2, security_q3, \
             security_a1_hash, security_a2_hash, security_a3_hash, role, exam_target) \
             VALUES (?1, ?2, ?3, ?4, 0, ?5, ?6, ?7, ?8, ?9, ?10, ?11, 'student', ?12)",
        )
        .bind(&[
            JsValue::from_str(&email),
            JsValue::from_str(name),
            JsValue::from_str(&password_hash),
            JsValue::from_str(&totp_secret),
            JsValue::from_str(&recovery_hash_json),
            JsValue::from_str(&qa[0].0),
            JsValue::from_str(&qa[1].0),
            JsValue::from_str(&qa[2].0),
            JsValue::from_str(&a1),
            JsValue::from_str(&a2),
            JsValue::from_str(&a3),
            JsValue::from_str(exam_target),
        ])?
        .run()
        .await?;
    let user_id = result.meta()?.and_then(|m| m.last_row_id).unwrap_or(0);
    db.prepare("INSERT INTO profiles (user_id, display_name) VALUES (?1, ?2)")
        .bind(&[
            JsValue::from_f64(user_id as f64),
            JsValue::from_str(name),
        ])?
        .run()
        .await?;

    let otpauth_url = totp::totp_setup_url(&totp_secret, &email, "MyStudy");
    json_ok(
        201,
        json!({
            "user_id": user_id,
            "totp_secret": totp_secret,
            "otpauth_url": otpauth_url,
            // Shown ONCE. The frontend must tell the user to save these;
            // only hashes are stored.
            "recovery_codes": recovery_codes,
            "message": "Scan the QR code with your authenticator app, then verify a 6-digit code to activate your account."
        }),
    )
}

async fn totp_verify(db: &D1Database, req: Request) -> Result<Response> {
    let body = body_json(req).await?;
    let user_id = body["user_id"].as_i64().unwrap_or(0);
    let code = body["code"].as_str().unwrap_or("");
    let user = db
        .prepare("SELECT * FROM users WHERE id = ?1")
        .bind(&[JsValue::from_f64(user_id as f64)])?
        .first::<UserRow>(None)
        .await?;
    let user = match user {
        Some(u) => u,
        None => return json_err(404, "not_found", "Account not found."),
    };
    let secret = match &user.totp_secret_enc {
        Some(s) => s.clone(),
        None => return json_err(400, "no_totp", "No TOTP setup found for this account."),
    };
    let now_ms = js_sys::Date::now() as u64;
    if !totp::verify_totp(&secret, code, now_ms) {
        return json_err(401, "invalid_code", "That code is not valid. Check your authenticator app and try again.");
    }
    db.prepare("UPDATE users SET totp_enabled = 1 WHERE id = ?1")
        .bind(&[JsValue::from_f64(user_id as f64)])?
        .run()
        .await?;
    let token = create_session(db, user_id).await?;
    let mut resp = json_ok(200, json!({ "user_id": user_id, "totp_enabled": true }))?;
    resp.headers_mut()
        .set("Set-Cookie", &session_cookie(&token))?;
    Ok(resp)
}

async fn login(db: &D1Database, req: Request) -> Result<Response> {
    let body = body_json(req).await?;
    let email = body["email"].as_str().unwrap_or("").trim().to_lowercase();
    let password = body["password"].as_str().unwrap_or("");
    let code = body["totp_code"].as_str().unwrap_or("");

    // Lockout: 5 failed attempts in the last 15 minutes.
    let fails = db
        .prepare(
            "SELECT COUNT(*) AS n FROM login_attempts \
             WHERE email = ?1 AND success = 0 AND attempted_at > datetime('now', '-15 minutes')",
        )
        .bind(&[JsValue::from_str(&email)])?
        .first::<Value>(None)
        .await?;
    let fail_count = fails
        .as_ref()
        .and_then(|v| v.get("n"))
        .and_then(|v| v.as_i64())
        .unwrap_or(0);
    if fail_count >= 5 {
        return json_err(429, "locked_out", "Too many failed attempts. Try again in 15 minutes.");
    }

    let user = db
        .prepare("SELECT * FROM users WHERE email = ?1")
        .bind(&[JsValue::from_str(&email)])?
        .first::<UserRow>(None)
        .await?;
    let user = match user {
        Some(u) => u,
        None => {
            // Record the failure without revealing whether the email exists.
            let _ = db
                .prepare("INSERT INTO login_attempts (email, success) VALUES (?1, 0)")
                .bind(&[JsValue::from_str(&email)])?
                .run()
                .await;
            return json_err(401, "invalid_credentials", "Email or password is incorrect.");
        }
    };
    if !auth::verify_password(password, &user.password_hash) {
        let _ = db
            .prepare("INSERT INTO login_attempts (email, success) VALUES (?1, 0)")
            .bind(&[JsValue::from_str(&email)])?
            .run()
            .await;
        return json_err(401, "invalid_credentials", "Email or password is incorrect.");
    }
    if user.totp_enabled == 1 {
        if code.is_empty() {
            return json_err(401, "totp_required", "Enter the 6-digit code from your authenticator app.");
        }
        let secret = user.totp_secret_enc.clone().unwrap_or_default();
        let now_ms = js_sys::Date::now() as u64;
        let code_ok = totp::verify_totp(&secret, code, now_ms);
        let mut recovery_ok = false;
        if !code_ok {
            // Recovery code: check the hash, then burn it.
            let hashes: Vec<String> =
                serde_json::from_str(&user.recovery_codes_hash).unwrap_or_default();
            let wanted = auth::sha256_hex(code);
            if hashes.contains(&wanted) {
                recovery_ok = true;
                let remaining: Vec<String> =
                    hashes.into_iter().filter(|h| *h != wanted).collect();
                let _ = db
                    .prepare("UPDATE users SET recovery_codes_hash = ?1 WHERE id = ?2")
                    .bind(&[
                        JsValue::from_str(&serde_json::to_string(&remaining).unwrap_or_default()),
                        JsValue::from_f64(user.id as f64),
                    ])?
                    .run()
                    .await;
            }
        }
        if !code_ok && !recovery_ok {
            let _ = db
                .prepare("INSERT INTO login_attempts (email, success) VALUES (?1, 0)")
                .bind(&[JsValue::from_str(&email)])?
                .run()
                .await;
            return json_err(401, "invalid_code", "That authenticator code is not valid.");
        }
    }
    let _ = db
        .prepare("INSERT INTO login_attempts (email, success) VALUES (?1, 1)")
        .bind(&[JsValue::from_str(&email)])?
        .run()
        .await;
    let _ = db
        .prepare("UPDATE users SET last_login = ?1 WHERE id = ?2")
        .bind(&[
            JsValue::from_str(&now_iso()),
            JsValue::from_f64(user.id as f64),
        ])?
        .run()
        .await;
    let token = create_session(db, user.id).await?;
    let mut resp = json_ok(
        200,
        json!({ "user_id": user.id, "role": user.role, "premium_status": user.premium_status }),
    )?;
    resp.headers_mut()
        .set("Set-Cookie", &session_cookie(&token))?;
    Ok(resp)
}

// ---------------------------------------------------------------- news

async fn publish_due(db: &D1Database) -> Result<()> {
    // Lazy publishing (architecture §6): no cron trigger, so a scheduled
    // post goes live the first time it is read after published_at.
    db.prepare(
        "UPDATE news_posts SET status = 'published' \
         WHERE status = 'scheduled' AND published_at IS NOT NULL \
         AND published_at <= datetime('now')",
    )
    .run()
    .await?;
    Ok(())
}

fn news_json(row: &NewsRow) -> Value {
    let tags: Vec<String> = serde_json::from_str(&row.tags_json).unwrap_or_default();
    let toc: Value = serde_json::from_str(&row.toc_json).unwrap_or(json!([]));
    json!({
        "slug": row.slug,
        "title": row.title,
        "excerpt": row.excerpt,
        "body_html": row.body_html,
        "featured_image_url": row.featured_image_url,
        "category": row.category,
        "tags": tags,
        "seo_title": row.seo_title,
        "seo_description": row.seo_description,
        "published_at": row.published_at,
        "toc": toc,
    })
}

async fn news_list(db: &D1Database) -> Result<Response> {
    publish_due(db).await?;
    let res = db
        .prepare(
            "SELECT * FROM news_posts WHERE status = 'published' \
             AND (published_at IS NULL OR published_at <= datetime('now')) \
             ORDER BY published_at DESC LIMIT 20",
        )
        .all()
        .await?;
    let rows: Vec<NewsRow> = res.results()?;
    let items: Vec<Value> = rows.iter().map(news_json).collect();
    json_ok(200, json!({ "posts": items }))
}

async fn news_one(db: &D1Database, slug: &str) -> Result<Response> {
    publish_due(db).await?;
    let row = db
        .prepare(
            "SELECT * FROM news_posts WHERE slug = ?1 AND status = 'published' \
             AND (published_at IS NULL OR published_at <= datetime('now'))",
        )
        .bind(&[JsValue::from_str(slug)])?
        .first::<NewsRow>(None)
        .await?;
    match row {
        Some(r) => json_ok(200, news_json(&r)),
        None => json_err(404, "not_found", "That news post does not exist."),
    }
}

async fn admin_news(db: &D1Database, req: Request) -> Result<Response> {
    // Admin check enforced in Rust, not in React (architecture §2.3).
    let session = current_session(db, &req).await?;
    match session {
        Some(s) if s.role == "admin" => {}
        _ => {
            return json_err(
                403,
                "forbidden",
                "Only an admin can create News posts.",
            );
        }
    }
    let body = body_json(req).await?;
    let title = body["title"].as_str().unwrap_or("").trim();
    let slug = body["slug"].as_str().unwrap_or("").trim();
    let body_html = body["body_html"].as_str().unwrap_or("");
    if title.is_empty() || slug.is_empty() || body_html.is_empty() {
        return bad_request("title, slug and body_html are required.");
    }
    // TODO (P2): insert into news_posts (with sanitised body_html,
    // category/tags/SEO fields, toc_json built from H2/H3) and return 201.
    // Phase 1 validates the admin role + payload and stops here so the
    // stub is never mistaken for a working write path.
    json_err(
        501,
        "not_implemented",
        "News creation lands in P2. Admin check passed; the D1 insert is not wired yet.",
    )
}

// ---------------------------------------------------------------- entry

#[event(fetch)]
pub async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let url = req.url()?;
    let path = url.path();
    let method = req.method();

    if path.starts_with("/api/") {
        let db = match env.d1("DB") {
            Ok(d) => d,
            Err(_) => return json_err(500, "no_db", "Database binding DB is not configured."),
        };
        return match (method, path) {
            (Method::Get, "/api/health") => json_ok(
                200,
                json!({ "status": "ok", "service": "mystudy-v2", "version": "0.1.0" }),
            ),
            (Method::Post, "/api/auth/register-start") => register_start(&db, req).await,
            (Method::Post, "/api/auth/totp-verify") => totp_verify(&db, req).await,
            (Method::Post, "/api/auth/login") => login(&db, req).await,
            (Method::Get, "/api/news") => news_list(&db).await,
            (Method::Get, p) if p.starts_with("/api/news/") => {
                let slug = p.trim_start_matches("/api/news/");
                if slug.is_empty() || slug.contains('/') {
                    json_err(400, "bad_request", "A news slug is required.")
                } else {
                    news_one(&db, slug).await
                }
            }
            (Method::Post, "/api/admin/news") => admin_news(&db, req).await,
            _ => json_err(404, "not_found", "That API route does not exist."),
        };
    }

    // Everything else: the React SPA from the ASSETS binding.
    let assets = match env.assets("ASSETS") {
        Ok(a) => a,
        Err(_) => {
            return Response::ok(
                "MyStudy v2 — the web app is not built yet. Run `npm run build` first.",
            )
        }
    };
    let index_url = format!("{}://{}/index.html", url.scheme(), url.host_str().unwrap_or("mystudy.local"));
    let mut resp = assets.fetch_request(req).await?;
    if resp.status_code() == 404 {
        // SPA fallback: serve index.html for client-side routes.
        resp = assets.fetch(&index_url, None).await?;
    }
    Ok(resp)
}
