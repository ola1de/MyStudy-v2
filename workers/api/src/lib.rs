//! MyStudy v2 API worker (Phase 1 scaffold).
//!
//! Routes (architecture §2, §4, §6):
//!   GET  /api/health
//!   POST /api/auth/register-start   (creates the account + TOTP secret, unusable until verified)
//!   POST /api/auth/totp-verify     (compulsory TOTP step that activates the account)
//!   POST /api/auth/login           (password, then TOTP code or recovery code)
//!   GET  /api/news                 (published News only)
//!   GET  /api/news/:slug           (single post; lazy-publishes due scheduled posts)
//!   POST /api/admin/news           (admin only; create a News post)
//!   GET  /api/admin/news           (admin only; all posts, any status, ?status=&category=&q=)
//!   GET  /api/admin/news/:slug     (admin only; single post, full fields)
//!   PUT  /api/admin/news/:slug     (admin only; update a post)
//!   DELETE /api/admin/news/:slug   (admin only; delete a post + best-effort R2 image)
//!   GET  /api/admin/news-categories  (admin only; seeds defaults on first read)
//!   POST /api/admin/news-categories (admin only; create a category)
//!   POST /api/admin/upload         (admin only; base64 image -> R2 MEDIA, <= 2 MB)
//!   GET  /api/media/*              (public; serves R2 objects under news/ only)
//! Any other path is served from the ASSETS binding (the React SPA).
//! Any other path is served from the ASSETS binding (the React SPA).
//!
//! Envelope: every API response is `{ "ok": bool, "data": ..., "error": { "code", "message" } }`.
//! Premium is never decided here from a client flag — it is read from
//! D1 (`users.premium_status`) per request (architecture §4).

mod auth;
mod security_questions;
mod totp;

use base64::{engine::general_purpose::STANDARD as BASE64_STANDARD, Engine as _};
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
    id: i64,
    slug: String,
    title: String,
    excerpt: Option<String>,
    body_html: String,
    featured_image_r2_key: Option<String>,
    featured_image_url: Option<String>,
    category: Option<String>,
    tags_json: String,
    seo_title: Option<String>,
    seo_description: Option<String>,
    seo_keywords: Option<String>,
    og_image: Option<String>,
    status: String,
    published_at: Option<String>,
    author_id: Option<i64>,
    toc_json: String,
    created_at: String,
    updated_at: String,
}

#[derive(Debug, Deserialize)]
struct NewsCategoryRow {
    id: i64,
    slug: String,
    name: String,
    description: Option<String>,
    created_at: String,
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

fn admin_news_json(row: &NewsRow) -> Value {
    let mut v = news_json(row);
    let obj = v.as_object_mut().expect("news_json is an object");
    let tags: Vec<String> = serde_json::from_str(&row.tags_json).unwrap_or_default();
    obj.insert("id".to_string(), json!(row.id));
    obj.insert("featured_image_r2_key".to_string(), json!(row.featured_image_r2_key));
    obj.insert("tags".to_string(), json!(tags));
    obj.insert("seo_keywords".to_string(), json!(row.seo_keywords));
    obj.insert("og_image".to_string(), json!(row.og_image));
    obj.insert("status".to_string(), json!(row.status));
    obj.insert("author_id".to_string(), json!(row.author_id));
    obj.insert("created_at".to_string(), json!(row.created_at));
    obj.insert("updated_at".to_string(), json!(row.updated_at));
    v
}

fn category_json(row: &NewsCategoryRow) -> Value {
    json!({
        "id": row.id,
        "slug": row.slug,
        "name": row.name,
        "description": row.description,
        "created_at": row.created_at,
    })
}

// ------------------------------------------------------------ pure helpers
// (no wasm/js_sys here, so cargo test can exercise them natively)

/// Slugify, mirroring apps/web/src/lib/toc.ts: lowercase, drop anything
/// that is not a-z / 0-9 / whitespace / hyphen, collapse whitespace to a
/// single hyphen, truncate to 60 chars, strip trailing hyphens.
fn slugify(text: &str) -> String {
    let mut s: String = text
        .to_lowercase()
        .chars()
        .filter(|c| c.is_ascii_alphanumeric() || *c == '-' || c.is_whitespace())
        .collect();
    s = s
        .split_whitespace()
        .collect::<Vec<&str>>()
        .join("-");
    // split_whitespace already drops leading/trailing whitespace and
    // collapses runs, but a leading/trailing hyphen can survive; trim it.
    let mut s: String = s.chars().take(60).collect();
    while s.ends_with('-') {
        s.pop();
    }
    while s.starts_with('-') {
        s.remove(0);
    }
    s
}

/// Strip all HTML tags from `s` (used for heading text).
fn strip_tags(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    let mut in_tag = false;
    for c in s.chars() {
        match c {
            '<' => in_tag = true,
            '>' => in_tag = false,
            _ => {
                if !in_tag {
                    out.push(c);
                }
            }
        }
    }
    out
}

fn ascii_lower_bytes(s: &str) -> Vec<u8> {
    s.bytes().map(|b| b.to_ascii_lowercase()).collect()
}

fn find_bytes(hay: &[u8], needle: &[u8], from: usize) -> Option<usize> {
    if needle.is_empty() || from > hay.len() {
        return None;
    }
    hay[from..]
        .windows(needle.len())
        .position(|w| w == needle)
        .map(|p| from + p)
}

fn is_heading_open_at(lower: &[u8], i: usize) -> Option<u8> {
    // lower[i..] starts with "<h2" or "<h3" followed by whitespace, '>' or '/'.
    if i + 3 > lower.len() || lower[i] != b'<' || lower[i + 1] != b'h' {
        return None;
    }
    let level = match lower[i + 2] {
        b'2' => 2u8,
        b'3' => 3u8,
        _ => return None,
    };
    if i + 3 == lower.len() {
        return Some(level);
    }
    match lower[i + 3] {
        b' ' | b'\t' | b'\n' | b'\r' | b'>' | b'/' => Some(level),
        _ => None,
    }
}

/// Build the table of contents from H2/H3 headings, mirroring toc.ts:
/// slugify (max 60 chars, dedup with -2/-3...), toc returned only when
/// there are >= 3 headings. Also returns the HTML with `id` + class
/// injected on each heading, so the toc ids actually exist in the stored
/// body_html (PostPage uses the stored body_html as-is when toc is set).
fn build_toc(html: &str) -> (Vec<Value>, String) {
    let lower = ascii_lower_bytes(html);
    let bytes = html.as_bytes();
    let mut toc: Vec<Value> = Vec::new();
    let mut seen: Vec<(String, usize)> = Vec::new();
    let mut out = String::with_capacity(html.len());
    let mut i = 0usize;
    let mut last = 0usize;
    while i < bytes.len() {
        let level = match is_heading_open_at(&lower, i) {
            Some(l) => l,
            None => {
                i += 1;
                continue;
            }
        };
        // End of the opening tag.
        let tag_end = match find_bytes(&lower, b">", i) {
            Some(off) => off,
            None => break,
        };
        let close_tag = format!("</h{level}>");
        let close = match find_bytes(&lower, close_tag.as_bytes(), tag_end) {
            Some(off) => off,
            None => break,
        };
        let attrs = &html[i + 3..tag_end];
        let inner = &html[tag_end + 1..close];
        let text = strip_tags(inner).trim().to_string();
        if text.is_empty() {
            i = close + close_tag.len();
            continue;
        }
        let base = {
            let s = slugify(&text);
            if s.is_empty() {
                "section".to_string()
            } else {
                s
            }
        };
        let n = match seen.iter_mut().find(|(s, _)| *s == base) {
            Some((_, count)) => {
                *count += 1;
                *count
            }
            None => {
                seen.push((base.clone(), 1));
                1
            }
        };
        let slug = if n > 1 {
            format!("{base}-{n}")
        } else {
            base
        };
        toc.push(json!({ "id": slug, "text": text, "level": level }));
        // Rebuild the heading: drop any pre-existing id="..." (toc.ts
        // only strips double-quoted ids), keep other attributes.
        let cleaned = remove_id_attr(attrs);
        out.push_str(&html[last..i]);
        out.push_str(&format!(
            "<h{level}{cleaned} id=\"{slug}\" class=\"anchor-heading\">{inner}</h{level}>"
        ));
        i = close + close_tag.len();
        last = i;
    }
    out.push_str(&html[last..]);
    let toc = if toc.len() >= 3 { toc } else { Vec::new() };
    (toc, out)
}

/// Remove ` id="..."` (double-quoted only, mirroring toc.ts) from an
/// attribute string.
fn remove_id_attr(attrs: &str) -> String {
    let mut out = attrs.to_string();
    loop {
        let cur_lower = out.to_lowercase();
        let Some(p) = cur_lower.find(" id=\"") else {
            break;
        };
        let rest = &out[p + 5..];
        match rest.find('"') {
            Some(end) => {
                out.replace_range(p..p + 5 + end + 1, "");
            }
            None => break,
        }
    }
    out
}

/// Sanitise editor HTML: drop script/style/iframe/object/embed elements
/// entirely (tag + contents; an unclosed one drops to end of input),
/// strip form tags but keep their contents, drop event-handler
/// attributes (on*) and javascript: href/src attributes. Everything
/// else is passed through unchanged.
fn sanitise_html(html: &str) -> String {
    // Pass 1: remove dangerous whole elements (script/style/iframe/
    // object/embed). Form is handled in pass 2 (tags only).
    let mut s = html.to_string();
    for tag in ["script", "style", "iframe", "object", "embed"] {
        s = remove_element(&s, tag);
    }
    // Pass 2: rebuild every remaining tag, dropping form tags, on*
    // attributes and javascript: href/src attributes.
    let mut out = String::with_capacity(s.len());
    let bytes = s.as_bytes();
    let mut i = 0usize;
    while i < bytes.len() {
        if bytes[i] != b'<' {
            // Copy through to the next '<' (byte-safe: '<' is ASCII,
            // so the slice boundary is a char boundary).
            let next = find_bytes(bytes, b"<", i).unwrap_or(bytes.len());
            out.push_str(&s[i..next]);
            i = next;
            continue;
        }
        // Find '>' respecting quotes.
        let mut j = i + 1;
        let mut quote: Option<u8> = None;
        while j < bytes.len() {
            let c = bytes[j];
            match quote {
                Some(q) => {
                    if c == q {
                        quote = None;
                    }
                }
                None => match c {
                    b'"' | b'\'' => quote = Some(c),
                    b'>' => break,
                    _ => {}
                },
            }
            j += 1;
        }
        if j >= bytes.len() {
            // Unclosed '<': drop it and the rest (cannot be a valid tag).
            break;
        }
        let tag_inner = &s[i + 1..j];
        let trimmed = tag_inner.trim_start();
        if trimmed.starts_with('!') || trimmed.starts_with('?') {
            // Comment / doctype / processing instruction: keep as-is.
            out.push_str(&s[i..=j]);
            i = j + 1;
            continue;
        }
        let is_close = trimmed.starts_with('/');
        let name_start = if is_close { 1 } else { 0 };
        let name: String = trimmed[name_start..]
            .chars()
            .take_while(|c| c.is_ascii_alphanumeric() || *c == '-' || *c == ':')
            .collect();
        let name_lower = name.to_lowercase();
        if name_lower == "form" {
            // Strip the form tags, keep the contents.
            i = j + 1;
            continue;
        }
        if is_close {
            out.push_str(&format!("</{name_lower}>"));
            i = j + 1;
            continue;
        }
        let attrs_str = &trimmed[name.len()..];
        let attrs = parse_attrs(attrs_str);
        let mut rebuilt = format!("<{name_lower}");
        for (aname, avalue, aquote) in attrs {
            let alower = aname.to_lowercase();
            if alower.starts_with("on") {
                continue;
            }
            if (alower == "href" || alower == "src")
                && avalue.as_deref().is_some_and(is_javascript_url)
            {
                continue;
            }
            match avalue {
                Some(v) => {
                    let q = aquote.unwrap_or('"');
                    rebuilt.push_str(&format!(" {aname}={q}{v}{q}"));
                }
                None => rebuilt.push_str(&format!(" {aname}")),
            }
        }
        // Preserve a trailing '/' for self-closing tags.
        if attrs_str.trim_end().ends_with('/') {
            rebuilt.push('/');
        }
        rebuilt.push('>');
        out.push_str(&rebuilt);
        i = j + 1;
    }
    out
}

/// Remove every `<tag ...>...</tag>` (or self-closing `<tag .../>`)
/// element from `html`, case-insensitively. Searching is done on an
/// ASCII-lowercased byte copy so indices stay valid in the original.
fn remove_element(html: &str, tag: &str) -> String {
    let lower = ascii_lower_bytes(html);
    let open_pat = format!("<{tag}").into_bytes();
    let close_pat = format!("</{tag}>").into_bytes();
    let mut out = String::with_capacity(html.len());
    let mut pos = 0usize;
    loop {
        let Some(found) = find_bytes(&lower, &open_pat, pos) else {
            out.push_str(&html[pos..]);
            break;
        };
        // The match must be a real tag open: next char whitespace, '>' or '/'.
        let after = lower.get(found + open_pat.len()).copied();
        match after {
            Some(b' ') | Some(b'\t') | Some(b'\n') | Some(b'\r') | Some(b'>') | Some(b'/') => {}
            _ => {
                out.push_str(&html[pos..found + open_pat.len()]);
                pos = found + open_pat.len();
                continue;
            }
        }
        out.push_str(&html[pos..found]);
        let gt = match find_bytes(&lower, b">", found) {
            Some(g) => g,
            None => break, // unclosed tag: drop to end
        };
        if html[found..gt].trim_end().ends_with('/') {
            pos = gt + 1;
            continue;
        }
        match find_bytes(&lower, &close_pat, gt) {
            Some(off) => {
                pos = off + close_pat.len();
            }
            None => break, // unclosed element: drop to end
        }
    }
    out
}

/// Parse an attribute string into (name, value, quote) triples. Values
/// keep their original text; quote is the quote char used, if any.
fn parse_attrs(s: &str) -> Vec<(String, Option<String>, Option<char>)> {
    let mut attrs = Vec::new();
    let b = s.as_bytes();
    let mut i = 0usize;
    while i < b.len() {
        while i < b.len() && (b[i] == b' ' || b[i] == b'\t' || b[i] == b'\n' || b[i] == b'\r' || b[i] == b'/') {
            i += 1;
        }
        if i >= b.len() {
            break;
        }
        let start = i;
        while i < b.len() && b[i] != b'=' && b[i] != b' ' && b[i] != b'\t' && b[i] != b'\n' && b[i] != b'\r' && b[i] != b'/' && b[i] != b'>' {
            i += 1;
        }
        if i == start {
            break;
        }
        let name = s[start..i].to_string();
        while i < b.len() && (b[i] == b' ' || b[i] == b'\t') {
            i += 1;
        }
        if i < b.len() && b[i] == b'=' {
            i += 1;
            while i < b.len() && (b[i] == b' ' || b[i] == b'\t') {
                i += 1;
            }
            if i < b.len() && (b[i] == b'"' || b[i] == b'\'') {
                let q = b[i] as char;
                i += 1;
                let vstart = i;
                while i < b.len() && b[i] != q as u8 {
                    i += 1;
                }
                let value = s[vstart..i].to_string();
                if i < b.len() {
                    i += 1;
                }
                attrs.push((name, Some(value), Some(q)));
            } else {
                let vstart = i;
                while i < b.len() && b[i] != b' ' && b[i] != b'\t' && b[i] != b'\n' && b[i] != b'\r' {
                    i += 1;
                }
                attrs.push((name, Some(s[vstart..i].to_string()), None));
            }
        } else {
            attrs.push((name, None, None));
        }
    }
    attrs
}

fn is_javascript_url(value: &str) -> bool {
    // Ignore leading control/whitespace and any whitespace/control
    // chars smuggled inside the scheme ("java\tscript:").
    let cleaned: String = value
        .chars()
        .filter(|c| !c.is_whitespace() && !c.is_control())
        .collect();
    cleaned.to_lowercase().starts_with("javascript:")
}

/// Normalise a client-supplied datetime to SQLite `YYYY-MM-DD HH:MM:SS`
/// (the format `datetime('now')` and publish_due() compare against, so
/// an ISO `2026-11-24T06:00:00Z` must not be stored verbatim — its 'T'
/// sorts after ' ' and would never be `<= datetime('now')` same-day).
/// Accepts `YYYY-MM-DD`, `YYYY-MM-DD HH:MM:SS` and ISO-8601 forms.
fn normalise_datetime(value: &str) -> Option<String> {
    let v = value.trim();
    if v.len() == 10 && v.as_bytes()[4] == b'-' && v.as_bytes()[7] == b'-' {
        return Some(format!("{v} 00:00:00"));
    }
    if v.len() >= 19 {
        let head = &v[..19];
        let hb = head.as_bytes();
        if hb[4] == b'-' && hb[7] == b'-' && (hb[10] == b'T' || hb[10] == b't' || hb[10] == b' ') && hb[13] == b':' && hb[16] == b':' {
            let mut out = String::with_capacity(19);
            out.push_str(&head[..10]);
            out.push(' ');
            out.push_str(&head[11..19]);
            return Some(out);
        }
    }
    None
}

/// `now_iso()` in SQLite `datetime('now')` format (`YYYY-MM-DD HH:MM:SS`).
fn now_sqlite(iso: &str) -> String {
    normalise_datetime(iso).unwrap_or_else(|| "1970-01-01 00:00:00".to_string())
}

fn opt_js(opt: &Option<String>) -> JsValue {
    match opt {
        Some(s) => JsValue::from_str(s),
        None => JsValue::NULL,
    }
}

fn opt_str(body: &Value, key: &str) -> Option<String> {
    match body.get(key) {
        Some(Value::String(s)) => {
            let t = s.trim();
            if t.is_empty() {
                None
            } else {
                Some(t.to_string())
            }
        }
        _ => None,
    }
}

fn parse_tags(value: &Value) -> Vec<String> {
    match value {
        Value::Array(arr) => arr
            .iter()
            .filter_map(|v| v.as_str().map(|s| s.trim().to_string()))
            .filter(|s| !s.is_empty())
            .collect(),
        Value::String(s) => s
            .split(',')
            .map(|t| t.trim().to_string())
            .filter(|t| !t.is_empty())
            .collect(),
        _ => Vec::new(),
    }
}

/// seo_keywords may arrive as a string ("a, b") or an array.
fn parse_keywords(value: &Value) -> Option<String> {
    match value {
        Value::String(s) => {
            let t = s.trim();
            if t.is_empty() {
                None
            } else {
                Some(t.to_string())
            }
        }
        Value::Array(_) => {
            let tags = parse_tags(value);
            if tags.is_empty() {
                None
            } else {
                Some(tags.join(", "))
            }
        }
        _ => None,
    }
}

const MAX_UPLOAD_BYTES: usize = 2 * 1024 * 1024;

fn upload_ext(content_type: &str) -> Option<&'static str> {
    match content_type.trim().to_lowercase().as_str() {
        "image/jpeg" => Some("jpg"),
        "image/png" => Some("png"),
        "image/webp" => Some("webp"),
        "image/gif" => Some("gif"),
        "image/avif" => Some("avif"),
        _ => None,
    }
}

fn upload_key(yyyymm: &str, random_hex: &str, ext: &str) -> String {
    format!("news/{yyyymm}/{random_hex}.{ext}")
}

fn hex_encode(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}

async fn admin_session(db: &D1Database, req: &Request) -> Result<Option<SessionRow>> {
    match current_session(db, req).await? {
        Some(s) if s.role == "admin" => Ok(Some(s)),
        _ => Ok(None),
    }
}

fn forbidden_news(msg: &str) -> Result<Response> {
    json_err(403, "forbidden", msg)
}

async fn fetch_news_by_slug(db: &D1Database, slug: &str) -> Result<Option<NewsRow>> {
    db.prepare("SELECT * FROM news_posts WHERE slug = ?1")
        .bind(&[JsValue::from_str(slug)])?
        .first::<NewsRow>(None)
        .await
}

async fn fetch_news_by_id(db: &D1Database, id: i64) -> Result<Option<NewsRow>> {
    db.prepare("SELECT * FROM news_posts WHERE id = ?1")
        .bind(&[JsValue::from_f64(id as f64)])?
        .first::<NewsRow>(None)
        .await
}

async fn slug_taken(db: &D1Database, slug: &str, except_id: Option<i64>) -> Result<bool> {
    let row = match except_id {
        Some(id) => {
            db.prepare("SELECT id FROM news_posts WHERE slug = ?1 AND id != ?2")
                .bind(&[JsValue::from_str(slug), JsValue::from_f64(id as f64)])?
                .first::<Value>(None)
                .await?
        }
        None => {
            db.prepare("SELECT id FROM news_posts WHERE slug = ?1")
                .bind(&[JsValue::from_str(slug)])?
                .first::<Value>(None)
                .await?
        }
    };
    Ok(row.is_some())
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

async fn admin_news_create(db: &D1Database, req: Request) -> Result<Response> {
    // Admin check enforced in Rust, not in React (architecture §2.3).
    let session = admin_session(db, &req).await?;
    let session = match session {
        Some(s) => s,
        None => return forbidden_news("Only an admin can create News posts."),
    };
    let body = body_json(req).await?;
    let title = body["title"].as_str().unwrap_or("").trim().to_string();
    if title.is_empty() {
        return bad_request("title is required.");
    }
    let raw_slug = body["slug"].as_str().unwrap_or("").trim();
    let slug = if raw_slug.is_empty() {
        slugify(&title)
    } else {
        slugify(raw_slug)
    };
    if slug.is_empty() {
        return bad_request("slug could not be generated from the title; provide a slug.");
    }
    let raw_body = body["body_html"].as_str().unwrap_or("");
    if raw_body.trim().is_empty() {
        return bad_request("body_html is required.");
    }
    let status = body["status"].as_str().unwrap_or("draft").trim().to_string();
    if !matches!(status.as_str(), "draft" | "published" | "scheduled") {
        return bad_request("status must be draft, published or scheduled.");
    }
    let published_raw = body["published_at"].as_str().map(|s| s.trim().to_string());
    let published_at: Option<String> = match status.as_str() {
        "published" => Some(match &published_raw {
            Some(p) if !p.is_empty() => match normalise_datetime(p) {
                Some(n) => n,
                None => return bad_request("published_at is not a valid datetime."),
            },
            _ => now_sqlite(&now_iso()),
        }),
        "scheduled" => match &published_raw {
            Some(p) if !p.is_empty() => match normalise_datetime(p) {
                Some(n) => Some(n),
                None => return bad_request("published_at is not a valid datetime."),
            },
            _ => return bad_request("A scheduled post needs a published_at date."),
        },
        _ => match &published_raw {
            Some(p) if !p.is_empty() => match normalise_datetime(p) {
                Some(n) => Some(n),
                None => return bad_request("published_at is not a valid datetime."),
            },
            _ => None,
        },
    };
    if slug_taken(db, &slug, None).await? {
        return json_err(409, "slug_taken", "A post with that slug already exists.");
    }
    let clean_body = sanitise_html(raw_body);
    if strip_tags(&clean_body).trim().is_empty() && clean_body.trim().is_empty() {
        return bad_request("body_html is empty after sanitising.");
    }
    let (toc, body_with_ids) = build_toc(&clean_body);
    let toc_json = serde_json::to_string(&toc).unwrap_or_else(|_| "[]".to_string());
    let tags = parse_tags(&body["tags"]);
    let tags_json = serde_json::to_string(&tags).unwrap_or_else(|_| "[]".to_string());
    let excerpt = opt_str(&body, "excerpt");
    let featured_image_url = opt_str(&body, "featured_image_url");
    let featured_image_r2_key = opt_str(&body, "featured_image_r2_key");
    let category = opt_str(&body, "category");
    let seo_title = opt_str(&body, "seo_title");
    let seo_description = opt_str(&body, "seo_description");
    let seo_keywords = parse_keywords(&body["seo_keywords"]);
    let og_image = opt_str(&body, "og_image");
    let result = db
        .prepare(
            "INSERT INTO news_posts (slug, title, excerpt, body_html, featured_image_r2_key, \
             featured_image_url, category, tags_json, seo_title, seo_description, seo_keywords, \
             og_image, status, published_at, author_id, toc_json) \
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16)",
        )
        .bind(&[
            JsValue::from_str(&slug),
            JsValue::from_str(&title),
            opt_js(&excerpt),
            JsValue::from_str(&body_with_ids),
            opt_js(&featured_image_r2_key),
            opt_js(&featured_image_url),
            opt_js(&category),
            JsValue::from_str(&tags_json),
            opt_js(&seo_title),
            opt_js(&seo_description),
            opt_js(&seo_keywords),
            opt_js(&og_image),
            JsValue::from_str(&status),
            opt_js(&published_at),
            JsValue::from_f64(session.user_id as f64),
            JsValue::from_str(&toc_json),
        ])?
        .run()
        .await;
    let result = match result {
        Ok(r) => r,
        Err(e) => {
            // A race on the UNIQUE slug surfaces here even after the check.
            if format!("{e:?}").contains("UNIQUE") {
                return json_err(409, "slug_taken", "A post with that slug already exists.");
            }
            return Err(e);
        }
    };
    let id = result.meta()?.and_then(|m| m.last_row_id).unwrap_or(0);
    match fetch_news_by_id(db, id).await? {
        Some(row) => json_ok(201, admin_news_json(&row)),
        None => json_ok(
            201,
            json!({
                "id": id, "slug": slug, "title": title, "excerpt": excerpt,
                "body_html": body_with_ids, "featured_image_r2_key": featured_image_r2_key,
                "featured_image_url": featured_image_url, "category": category,
                "tags": tags, "seo_title": seo_title, "seo_description": seo_description,
                "seo_keywords": seo_keywords, "og_image": og_image, "status": status,
                "published_at": published_at, "author_id": session.user_id, "toc": toc,
            }),
        ),
    }
}

async fn admin_news_list(db: &D1Database, req: &Request) -> Result<Response> {
    if admin_session(db, req).await?.is_none() {
        return forbidden_news("Only an admin can list all News posts.");
    }
    publish_due(db).await?;
    let url = req.url()?;
    let mut status_f: Option<String> = None;
    let mut category_f: Option<String> = None;
    let mut q_f: Option<String> = None;
    for (k, v) in url.query_pairs() {
        match k.as_ref() {
            "status" => status_f = Some(v.trim().to_string()),
            "category" => category_f = Some(v.trim().to_string()),
            "q" => q_f = Some(v.trim().to_string()),
            _ => {}
        }
    }
    if let Some(s) = &status_f {
        if !matches!(s.as_str(), "draft" | "published" | "scheduled") {
            return bad_request("status must be draft, published or scheduled.");
        }
    }
    let mut sql =
        String::from("SELECT * FROM news_posts WHERE 1 = 1");
    let mut params: Vec<JsValue> = Vec::new();
    if let Some(s) = &status_f {
        params.push(JsValue::from_str(s));
        sql.push_str(&format!(" AND status = ?{}", params.len()));
    }
    if let Some(c) = &category_f {
        if !c.is_empty() {
            params.push(JsValue::from_str(c));
            sql.push_str(&format!(" AND category = ?{}", params.len()));
        }
    }
    if let Some(q) = &q_f {
        if !q.is_empty() {
            let like = format!(
                "%{}%",
                q.replace('\\', "\\\\").replace('%', "\\%").replace('_', "\\_")
            );
            params.push(JsValue::from_str(&like));
            let n = params.len();
            sql.push_str(&format!(
                " AND (title LIKE ?{n} ESCAPE '\\' OR excerpt LIKE ?{n} ESCAPE '\\' \
                 OR body_html LIKE ?{n} ESCAPE '\\')"
            ));
        }
    }
    sql.push_str(" ORDER BY created_at DESC, id DESC LIMIT 500");
    let res = db.prepare(sql).bind(&params)?.all().await?;
    let rows: Vec<NewsRow> = res.results()?;
    let items: Vec<Value> = rows.iter().map(admin_news_json).collect();
    json_ok(200, json!({ "posts": items }))
}

async fn admin_news_one(db: &D1Database, req: &Request, slug: &str) -> Result<Response> {
    if admin_session(db, req).await?.is_none() {
        return forbidden_news("Only an admin can view a News post in the admin area.");
    }
    publish_due(db).await?;
    match fetch_news_by_slug(db, slug).await? {
        Some(row) => json_ok(200, admin_news_json(&row)),
        None => json_err(404, "not_found", "That news post does not exist."),
    }
}

async fn admin_news_update(db: &D1Database, req: Request, slug: &str) -> Result<Response> {
    if admin_session(db, &req).await?.is_none() {
        return forbidden_news("Only an admin can update News posts.");
    }
    let existing = match fetch_news_by_slug(db, slug).await? {
        Some(r) => r,
        None => return json_err(404, "not_found", "That news post does not exist."),
    };
    let body = body_json(req).await?;
    let mut title = existing.title.clone();
    let mut new_slug = existing.slug.clone();
    let mut excerpt = existing.excerpt.clone();
    let mut body_html = existing.body_html.clone();
    let mut toc_json = existing.toc_json.clone();
    let mut featured_image_r2_key = existing.featured_image_r2_key.clone();
    let mut featured_image_url = existing.featured_image_url.clone();
    let mut category = existing.category.clone();
    let mut tags: Vec<String> =
        serde_json::from_str(&existing.tags_json).unwrap_or_default();
    let mut seo_title = existing.seo_title.clone();
    let mut seo_description = existing.seo_description.clone();
    let mut seo_keywords = existing.seo_keywords.clone();
    let mut og_image = existing.og_image.clone();
    let mut status = existing.status.clone();
    let mut published_at = existing.published_at.clone();

    if let Some(v) = body.get("title") {
        match v.as_str() {
            Some(t) if !t.trim().is_empty() => title = t.trim().to_string(),
            _ => return bad_request("title must not be empty."),
        }
    }
    if let Some(v) = body.get("slug") {
        match v.as_str() {
            Some(s) if !s.trim().is_empty() => {
                let s = slugify(s.trim());
                if s.is_empty() {
                    return bad_request("slug could not be generated; provide a slug.");
                }
                new_slug = s;
            }
            _ => return bad_request("slug must not be empty."),
        }
    }
    if body.get("excerpt").is_some() {
        excerpt = opt_str(&body, "excerpt");
    }
    if let Some(v) = body.get("body_html") {
        match v.as_str() {
            Some(b) if !b.trim().is_empty() => {
                let clean = sanitise_html(b);
                if clean.trim().is_empty() {
                    return bad_request("body_html is empty after sanitising.");
                }
                let (toc, with_ids) = build_toc(&clean);
                body_html = with_ids;
                toc_json = serde_json::to_string(&toc).unwrap_or_else(|_| "[]".to_string());
            }
            _ => return bad_request("body_html must not be empty."),
        }
    }
    if body.get("featured_image_r2_key").is_some() {
        featured_image_r2_key = opt_str(&body, "featured_image_r2_key");
    }
    if body.get("featured_image_url").is_some() {
        featured_image_url = opt_str(&body, "featured_image_url");
    }
    if body.get("category").is_some() {
        category = opt_str(&body, "category");
    }
    if body.get("tags").is_some() {
        tags = parse_tags(&body["tags"]);
    }
    if body.get("seo_title").is_some() {
        seo_title = opt_str(&body, "seo_title");
    }
    if body.get("seo_description").is_some() {
        seo_description = opt_str(&body, "seo_description");
    }
    if body.get("seo_keywords").is_some() {
        seo_keywords = parse_keywords(&body["seo_keywords"]);
    }
    if body.get("og_image").is_some() {
        og_image = opt_str(&body, "og_image");
    }
    if let Some(v) = body.get("status") {
        match v.as_str() {
            Some(s) if matches!(s.trim(), "draft" | "published" | "scheduled") => {
                status = s.trim().to_string();
            }
            _ => return bad_request("status must be draft, published or scheduled."),
        }
    }
    if body.get("published_at").is_some() {
        match body["published_at"].as_str() {
            Some(p) if !p.trim().is_empty() => match normalise_datetime(p.trim()) {
                Some(n) => published_at = Some(n),
                None => return bad_request("published_at is not a valid datetime."),
            },
            _ => published_at = None,
        }
    }
    if status == "published" && published_at.is_none() {
        published_at = Some(now_sqlite(&now_iso()));
    }
    if status == "scheduled" && published_at.is_none() {
        return bad_request("A scheduled post needs a published_at date.");
    }
    if new_slug != existing.slug && slug_taken(db, &new_slug, Some(existing.id)).await? {
        return json_err(409, "slug_taken", "A post with that slug already exists.");
    }
    let tags_json = serde_json::to_string(&tags).unwrap_or_else(|_| "[]".to_string());
    db.prepare(
        "UPDATE news_posts SET slug = ?1, title = ?2, excerpt = ?3, body_html = ?4, \
         featured_image_r2_key = ?5, featured_image_url = ?6, category = ?7, tags_json = ?8, \
         seo_title = ?9, seo_description = ?10, seo_keywords = ?11, og_image = ?12, \
         status = ?13, published_at = ?14, toc_json = ?15, updated_at = datetime('now') \
         WHERE id = ?16",
    )
    .bind(&[
        JsValue::from_str(&new_slug),
        JsValue::from_str(&title),
        opt_js(&excerpt),
        JsValue::from_str(&body_html),
        opt_js(&featured_image_r2_key),
        opt_js(&featured_image_url),
        opt_js(&category),
        JsValue::from_str(&tags_json),
        opt_js(&seo_title),
        opt_js(&seo_description),
        opt_js(&seo_keywords),
        opt_js(&og_image),
        JsValue::from_str(&status),
        opt_js(&published_at),
        JsValue::from_str(&toc_json),
        JsValue::from_f64(existing.id as f64),
    ])?
    .run()
    .await?;
    match fetch_news_by_id(db, existing.id).await? {
        Some(row) => json_ok(200, admin_news_json(&row)),
        None => json_err(404, "not_found", "That news post does not exist."),
    }
}

async fn admin_news_delete(
    db: &D1Database,
    req: &Request,
    bucket: Option<&Bucket>,
    slug: &str,
) -> Result<Response> {
    if admin_session(db, req).await?.is_none() {
        return forbidden_news("Only an admin can delete News posts.");
    }
    let existing = match fetch_news_by_slug(db, slug).await? {
        Some(r) => r,
        None => return json_err(404, "not_found", "That news post does not exist."),
    };
    // Best-effort R2 cleanup: the stored key, or the key implied by a
    // /api/media/<key> featured-image URL.
    let r2_key: Option<String> = existing
        .featured_image_r2_key
        .clone()
        .filter(|k| !k.is_empty())
        .or_else(|| {
            existing
                .featured_image_url
                .as_ref()
                .and_then(|u| u.strip_prefix("/api/media/").map(|k| k.to_string()))
                .filter(|k| k.starts_with("news/"))
        });
    db.prepare("DELETE FROM news_posts WHERE id = ?1")
        .bind(&[JsValue::from_f64(existing.id as f64)])?
        .run()
        .await?;
    if let (Some(bucket), Some(key)) = (bucket, r2_key) {
        let _ = bucket.delete(key).await;
    }
    json_ok(200, json!({ "deleted": true }))
}

// ------------------------------------------------------------ categories

const DEFAULT_CATEGORIES: [(&str, &str); 6] = [
    ("JAMB", "jamb"),
    ("WAEC", "waec"),
    ("NECO", "neco"),
    ("Admissions", "admissions"),
    ("Study Tips", "study-tips"),
    ("Announcements", "announcements"),
];

async fn admin_news_categories_list(db: &D1Database, req: &Request) -> Result<Response> {
    if admin_session(db, req).await?.is_none() {
        return forbidden_news("Only an admin can manage News categories.");
    }
    let count = db
        .prepare("SELECT COUNT(*) AS n FROM news_categories")
        .first::<Value>(None)
        .await?;
    let n = count
        .as_ref()
        .and_then(|v| v.get("n"))
        .and_then(|v| v.as_i64())
        .unwrap_or(0);
    if n == 0 {
        for (name, slug) in DEFAULT_CATEGORIES {
            let _ = db
                .prepare(
                    "INSERT OR IGNORE INTO news_categories (slug, name) VALUES (?1, ?2)",
                )
                .bind(&[JsValue::from_str(slug), JsValue::from_str(name)])?
                .run()
                .await;
        }
    }
    let res = db
        .prepare("SELECT * FROM news_categories ORDER BY id ASC")
        .all()
        .await?;
    let rows: Vec<NewsCategoryRow> = res.results()?;
    let items: Vec<Value> = rows.iter().map(category_json).collect();
    json_ok(200, json!({ "categories": items }))
}

async fn admin_news_category_create(db: &D1Database, req: Request) -> Result<Response> {
    if admin_session(db, &req).await?.is_none() {
        return forbidden_news("Only an admin can create News categories.");
    }
    let body = body_json(req).await?;
    let name = body["name"].as_str().unwrap_or("").trim().to_string();
    if name.is_empty() {
        return bad_request("name is required.");
    }
    let raw_slug = body["slug"].as_str().unwrap_or("").trim();
    let slug = if raw_slug.is_empty() {
        slugify(&name)
    } else {
        slugify(raw_slug)
    };
    if slug.is_empty() {
        return bad_request("slug could not be generated from the name; provide a slug.");
    }
    let existing = db
        .prepare("SELECT id FROM news_categories WHERE slug = ?1")
        .bind(&[JsValue::from_str(&slug)])?
        .first::<Value>(None)
        .await?;
    if existing.is_some() {
        return json_err(409, "slug_taken", "A category with that slug already exists.");
    }
    let description = opt_str(&body, "description");
    let result = db
        .prepare("INSERT INTO news_categories (slug, name, description) VALUES (?1, ?2, ?3)")
        .bind(&[
            JsValue::from_str(&slug),
            JsValue::from_str(&name),
            opt_js(&description),
        ])?
        .run()
        .await;
    let result = match result {
        Ok(r) => r,
        Err(e) => {
            if format!("{e:?}").contains("UNIQUE") {
                return json_err(409, "slug_taken", "A category with that slug already exists.");
            }
            return Err(e);
        }
    };
    let id = result.meta()?.and_then(|m| m.last_row_id).unwrap_or(0);
    let row = db
        .prepare("SELECT * FROM news_categories WHERE id = ?1")
        .bind(&[JsValue::from_f64(id as f64)])?
        .first::<NewsCategoryRow>(None)
        .await?;
    match row {
        Some(r) => json_ok(201, category_json(&r)),
        None => json_ok(
            201,
            json!({ "id": id, "slug": slug, "name": name, "description": description }),
        ),
    }
}

// ------------------------------------------------------------ upload / media

async fn admin_upload(db: &D1Database, bucket: &Bucket, req: Request) -> Result<Response> {
    if admin_session(db, &req).await?.is_none() {
        return forbidden_news("Only an admin can upload images.");
    }
    let body = body_json(req).await?;
    let filename = body["filename"].as_str().unwrap_or("").trim().to_string();
    let content_type = body["content_type"].as_str().unwrap_or("").trim().to_string();
    let data_b64 = body["data_base64"].as_str().unwrap_or("");
    if filename.is_empty() {
        return bad_request("filename is required.");
    }
    let ext = match upload_ext(&content_type) {
        Some(e) => e,
        None => {
            return json_err(
                400,
                "bad_request",
                "content_type must be image/jpeg, image/png, image/webp, image/gif or image/avif.",
            );
        }
    };
    if data_b64.is_empty() {
        return bad_request("data_base64 is required.");
    }
    let cleaned: String = data_b64.chars().filter(|c| !c.is_whitespace()).collect();
    let bytes = match BASE64_STANDARD.decode(&cleaned) {
        Ok(b) => b,
        Err(_) => return json_err(400, "invalid_base64", "data_base64 is not valid base64."),
    };
    if bytes.len() > MAX_UPLOAD_BYTES {
        return json_err(400, "too_large", "Image is larger than the 2 MB maximum.");
    }
    let iso = now_iso();
    let yyyymm = format!("{}{}", &iso[0..4], &iso[5..7]);
    let random = auth::random_bytes(8)
        .map_err(|e| Error::RustError(format!("random bytes: {e}")))?;
    let key = upload_key(&yyyymm, &hex_encode(&random), ext);
    bucket
        .put(key.clone(), bytes)
        .http_metadata(HttpMetadata {
            content_type: Some(content_type.clone()),
            ..Default::default()
        })
        .execute()
        .await?;
    json_ok(201, json!({ "key": key, "url": format!("/api/media/{key}") }))
}

async fn media_get(bucket: &Bucket, key: &str) -> Result<Response> {
    if key.is_empty() || !key.starts_with("news/") || key.contains("..") {
        return json_err(404, "not_found", "That media file does not exist.");
    }
    let obj = match bucket.get(key.to_string()).execute().await? {
        Some(o) => o,
        None => return json_err(404, "not_found", "That media file does not exist."),
    };
    let content_type = obj
        .http_metadata()
        .content_type
        .filter(|c| !c.is_empty())
        .unwrap_or_else(|| {
            match key.rsplit('.').next().unwrap_or("") {
                "jpg" | "jpeg" => "image/jpeg".to_string(),
                "png" => "image/png".to_string(),
                "webp" => "image/webp".to_string(),
                "gif" => "image/gif".to_string(),
                "avif" => "image/avif".to_string(),
                _ => "application/octet-stream".to_string(),
            }
        });
    let body = match obj.body() {
        Some(b) => b,
        None => return json_err(404, "not_found", "That media file does not exist."),
    };
    let bytes = body.bytes().await?;
    let mut resp = Response::from_bytes(bytes)?;
    resp.headers_mut().set("Content-Type", &content_type)?;
    resp.headers_mut()
        .set("Cache-Control", "public, max-age=31536000, immutable")?;
    Ok(resp)
}

// ---------------------------------------------------------------- entry

#[event(fetch)]
pub async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let url = req.url()?;
    let path = url.path();
    let method = req.method();

    // Public media reads need only the R2 binding, not D1.
    if path.starts_with("/api/media/") {
        let bucket = match env.bucket("MEDIA") {
            Ok(b) => b,
            Err(_) => {
                return json_err(500, "no_media", "Media binding MEDIA is not configured.")
            }
        };
        return match method {
            Method::Get => {
                let key = &path["/api/media/".len()..];
                media_get(&bucket, key).await
            }
            _ => json_err(404, "not_found", "That API route does not exist."),
        };
    }

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
            (Method::Post, "/api/admin/news") => admin_news_create(&db, req).await,
            (Method::Get, "/api/admin/news") => admin_news_list(&db, &req).await,
            (Method::Get, p) if p.starts_with("/api/admin/news/") => {
                let slug = &p["/api/admin/news/".len()..];
                if slug.is_empty() || slug.contains('/') {
                    json_err(400, "bad_request", "A news slug is required.")
                } else {
                    admin_news_one(&db, &req, slug).await
                }
            }
            (Method::Put, p) if p.starts_with("/api/admin/news/") => {
                let slug = &p["/api/admin/news/".len()..];
                if slug.is_empty() || slug.contains('/') {
                    json_err(400, "bad_request", "A news slug is required.")
                } else {
                    admin_news_update(&db, req, slug).await
                }
            }
            (Method::Delete, p) if p.starts_with("/api/admin/news/") => {
                let slug = &p["/api/admin/news/".len()..];
                if slug.is_empty() || slug.contains('/') {
                    json_err(400, "bad_request", "A news slug is required.")
                } else {
                    let bucket = env.bucket("MEDIA").ok();
                    admin_news_delete(&db, &req, bucket.as_ref(), slug).await
                }
            }
            (Method::Get, "/api/admin/news-categories") => {
                admin_news_categories_list(&db, &req).await
            }
            (Method::Post, "/api/admin/news-categories") => {
                admin_news_category_create(&db, req).await
            }
            (Method::Post, "/api/admin/upload") => match env.bucket("MEDIA") {
                Ok(bucket) => admin_upload(&db, &bucket, req).await,
                Err(_) => {
                    json_err(500, "no_media", "Media binding MEDIA is not configured.")
                }
            },
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

#[cfg(test)]
mod news_tests {
    use super::*;

    #[test]
    fn slugify_mirrors_toc_ts() {
        assert_eq!(slugify("JAMB 2027 Registration Guide!"), "jamb-2027-registration-guide");
        assert_eq!(slugify("  Study   Tips & Tricks  "), "study-tips-tricks");
        assert_eq!(slugify(""), "");
        // 60-char cap, trailing hyphens stripped.
        let long = "a".repeat(70);
        assert_eq!(slugify(&long).len(), 60);
        assert_eq!(slugify("hello world-"), "hello-world");
    }

    #[test]
    fn toc_needs_three_headings_and_dedups() {
        let html = "<h2>First</h2><p>x</p><h3>Second</h3><p>y</p><h2>First</h2><p>z</p>";
        let (toc, with_ids) = build_toc(html);
        assert_eq!(toc.len(), 3);
        assert_eq!(toc[0]["id"], "first");
        assert_eq!(toc[1]["id"], "second");
        assert_eq!(toc[2]["id"], "first-2");
        assert_eq!(toc[2]["level"], 2);
        assert!(with_ids.contains("<h2 id=\"first\" class=\"anchor-heading\">First</h2>"));
        assert!(with_ids.contains("<h2 id=\"first-2\" class=\"anchor-heading\">First</h2>"));
        // Fewer than 3 headings: toc is empty (toc.ts rule), ids still injected.
        let (toc2, _) = build_toc("<h2>Only</h2><p>x</p><h3>Two</h3>");
        assert!(toc2.is_empty());
        // Headings with inner tags: text is stripped for the slug/text.
        let (toc3, _) = build_toc("<h2><b>Bold</b> Title</h2><h2>B</h2><h2>C</h2>");
        assert_eq!(toc3[0]["id"], "bold-title");
        assert_eq!(toc3[0]["text"], "Bold Title");
    }

    #[test]
    fn sanitise_strips_dangerous_tags_attrs_and_js_hrefs() {
        let html = "<p onclick=\"evil()\" onmouseover='x'>Hi</p>\
            <script>alert(1)</script><style>.a{}</style>\
            <iframe src=\"https://evil.example\"></iframe>\
            <a href=\"javascript:alert(1)\">click</a>\
            <a href=\"JaVaScRipT:alert(1)\">click2</a>\
            <a href=\"https://example.com\">ok</a>\
            <form action=\"/x\"><input name=\"q\"></form>";
        let clean = sanitise_html(html);
        assert!(!clean.contains("<script"));
        assert!(!clean.contains("alert(1)</script>"));
        assert!(!clean.contains("<style"));
        assert!(!clean.contains("<iframe"));
        assert!(!clean.to_lowercase().contains("onclick"));
        assert!(!clean.to_lowercase().contains("onmouseover"));
        assert!(!clean.to_lowercase().contains("javascript:"));
        assert!(clean.contains("href=\"https://example.com\""));
        assert!(!clean.contains("<form"));
        assert!(clean.contains("<input name=\"q\">"));
        // Unclosed script drops to end of input.
        assert_eq!(sanitise_html("<p>ok</p><script>alert(1)"), "<p>ok</p>");
        // Non-ASCII text survives byte-based scanning.
        assert!(sanitise_html("<p>Yorùbá — ẹ ku abọ̀</p>").contains("Yorùbá"));
    }

    #[test]
    fn datetime_normalisation_is_sqlite_format() {
        assert_eq!(
            normalise_datetime("2026-12-01T09:30:00.000Z").as_deref(),
            Some("2026-12-01 09:30:00")
        );
        assert_eq!(
            normalise_datetime("2026-12-01 09:30:00").as_deref(),
            Some("2026-12-01 09:30:00")
        );
        assert_eq!(
            normalise_datetime("2026-12-01").as_deref(),
            Some("2026-12-01 00:00:00")
        );
        assert_eq!(normalise_datetime("not a date"), None);
        assert_eq!(now_sqlite("2026-11-24T06:39:23.000Z"), "2026-11-24 06:39:23");
    }

    #[test]
    fn upload_ext_and_key() {
        assert_eq!(upload_ext("image/jpeg"), Some("jpg"));
        assert_eq!(upload_ext("image/png"), Some("png"));
        assert_eq!(upload_ext("image/webp"), Some("webp"));
        assert_eq!(upload_ext("image/gif"), Some("gif"));
        assert_eq!(upload_ext("image/avif"), Some("avif"));
        assert_eq!(upload_ext("image/svg+xml"), None);
        assert_eq!(upload_ext("application/pdf"), None);
        assert_eq!(
            upload_key("202611", "0123456789abcdef", "png"),
            "news/202611/0123456789abcdef.png"
        );
        assert_eq!(hex_encode(&[0xab, 0x01, 0xff]), "ab01ff");
    }

    #[test]
    fn tags_and_keywords_parsing() {
        let tags = parse_tags(&json!([" jamb ", "", "2027"]));
        assert_eq!(tags, vec!["jamb".to_string(), "2027".to_string()]);
        let tags2 = parse_tags(&json!("a, b ,c"));
        assert_eq!(tags2, vec!["a".to_string(), "b".to_string(), "c".to_string()]);
        assert_eq!(parse_keywords(&json!("a, b")).as_deref(), Some("a, b"));
        assert_eq!(
            parse_keywords(&json!(["a", "b"])).as_deref(),
            Some("a, b")
        );
        assert_eq!(parse_keywords(&json!("  ")), None);
    }
}
