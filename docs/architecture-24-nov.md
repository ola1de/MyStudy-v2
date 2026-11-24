# MyStudy v2 — React + Rust Architecture

Date: 2026-11-24. Status: design + Phase 1 scaffold in progress. Blogger v1 stays live at mystudy.name.ng until v2 passes staging walkthrough + written approval.
Sources: template inventory `template-inventory-24-nov.md`, repo audit `repo-audit-24-nov.md`, live-site check 24 Nov 2026.

## 0. Decisions

- **Stack:** React 19 + Vite + TypeScript frontend (SPA, PWA-capable), Rust backend compiled to WASM on Cloudflare Workers via `workers-rs`, same D1 + R2 + KV pattern as WORDLESS v2 / Proseforge. No Blogger, no client-side premium, no localStorage as source of truth.
- **Deploy:** user's Cloudflare, scoped API token already connected (account b4fc7bb3e29957d6e05fda13b6330adf). Staging first on `mystudy-staging.<workers-subdomain>.workers.dev`, production only after walkthrough + approval. Custom domain `mystudy.name.ng` cutover is a separate, user-approved step — Blogger DNS is not touched until then.
- **Free-tier constraints [measured from WORDLESS work]:** 100,000 req/day, 10 ms CPU/request, Worker 64 MiB uncompressed, account already at 5/5 free cron triggers — so v2 must NOT depend on a cron trigger. Scheduled publishing, streak resets, etc. are lazy/on-read, not cron-driven. Login password check measured ~31 ms locally in WORDLESS — keep auth work cheap, Argon2id is too heavy for Workers CPU limit; use scrypt-light / PBKDF2 with modest params + rate limiting, and measure on staging.
- **Money:** no paid Cloudflare tier, no paid service required. Paystack is the only external paid flow, and only the user's Paystack keys (pasted in admin) touch money.

## 1. What v1 had, what v2 keeps / fixes

Kept (from template, verified): 48 routes / 55 views, CBT, English Quiz, Learn Hub keypoints (165 topics, 12 subjects), CGPA, admission toolkit, flashcards (Leitner), planner/timetable, budget, Word/PDF/Image toolkits, citation/summarizer, dictionary, Constitution library, vocabulary, post format + TOC (see §6).

Fixed in v2 (evidenced gaps):
1. No auth at all in v1 → full accounts (§2).
2. Premium enforced client-side (`profile.license='premium'` flips it) → server-side only (§4).
3. Bare domain DNS fails, Privacy/Terms 404, 2 homepage posts 404, Learn Hub empty labels → v2 serves only real content; empty states are honest, dead routes return 404 with a working list.
4. Question banks: 49% placeholders, 11 corrupt files, 0 JAMB explanations, no topic tags → normalised import (§5), placeholder years never shown as available.
5. `mystudy-pwa` is one 1.6 KB sw.js with no caching → real PWA: manifest, precache shell, offline question-pack cache, install prompt.
6. Profile was name/institution/course/theme only → full profile (§2.4).

## 2. Auth — compulsory, Google-Authenticator-style

### 2.1 Registration
- Fields: full name, email (unique, verified via code), password (min 12, zxcvbn-style strength meter, breached-password check against a small local list — no external call), exam target (JAMB/WAEC/NECO/Post-UTME), intended course/institution (optional).
- **3 security questions, dropdowns:** user picks 3 *different* questions from a fixed list of 12 (e.g. mother's maiden name is NOT offered — too guessable; use: first primary school, favourite teacher's surname, first pet, city of birth, best friend in secondary school, etc.). Answers are normalised (lowercase, trim), salted + hashed server-side, never stored plaintext, never returned. Used only for password recovery, after email verification.
- **TOTP setup is compulsory, at registration, before the account can use CBT/premium:** server generates a TOTP secret (160-bit, base32), shows a QR code (`otpauth://totp/MyStudy:<email>?secret=...&issuer=MyStudy`) rendered client-side from the secret, plus a manual-code copy button ("Can't scan? Copy this code"). User must enter a valid 6-digit code from their authenticator app (Google Authenticator / Authy / etc.) to finish registration. Recovery codes: 10 one-time codes, shown once, hashed server-side, downloadable/printable.
- No social login in Phase 1. "Like Google" here means authenticator-app 2FA, not Sign in with Google — that is a later, optional addition and must not be promised as shipped.

### 2.2 Sign-in / sessions
- Email + password, then TOTP code (or a recovery code, which is then burned). 5 failed attempts → 15-min lockout per account + per IP, logged.
- Sessions: opaque random token, HttpOnly + Secure + SameSite=Lax cookie, 7-day sliding, server-side session table in D1, revocable from profile ("Sign out everywhere"). No JWT with premium claims — premium is looked up server-side per request.
- Password reset: email code → answer 2 of 3 security questions correctly → set new password → TOTP still required on next sign-in. Security answers alone never reset a password without the email code.

### 2.3 Roles
- `student` (default), `admin` (only the owner account + accounts promoted by an admin in admin UI; first admin is seeded by the owner, not self-service). Admin-only: News posts, Paystack settings, question-bank import, user management. Students can never create/edit News, even via API — enforced in Rust, not in React.

### 2.4 Profile (customisable)
Display name, avatar (upload to R2 or URL, max 2 MB, resized server-side), bio, exam target + subjects, target score, institution/course, theme (light/dark + accent, as in v1), notification prefs, study streak display. Public profile is opt-in; by default only the student + admin see it.

## 3. Data model (D1, SQLite)

Core tables (migration `0001` in Phase 1, extended per phase):
- `users` (id, email unique, name, password_hash, totp_secret_enc, totp_enabled, recovery_codes_hash, security_q1..3 + answer hashes, role, premium_until / premium_status, created_at, last_login)
- `sessions`, `password_resets`, `login_attempts`
- `profiles` (user_id FK, display_name, avatar_r2_key, bio, exam_target, subjects_json, target_score, theme, accent)
- `questions` (id, exam, subject, year, topic, q_text, options_json[4], answer_idx, explanation nullable, source_file, hash unique for dedup)
- `exams` / `exam_sessions` (id, user_id, exam, subjects_json, started_at, ends_at, server_seed, status, answers_json, score_json, strikes, submitted_at) — answers are scored server-side at submit; the client never receives answer keys during the exam.
- `news_posts` (id, slug unique, title, excerpt, body_html sanitised, featured_image_r2_key/url, category, tags_json, seo_title, seo_description, seo_keywords, og_image, status draft/published/scheduled, published_at, author_id, toc_json)
- `news_categories`, `payments` (id, user_id, paystack_ref unique, amount_kobo, status, verified_at, raw_json), `settings` (key/value: paystack_public_key, paystack_secret_enc, premium_price_kobo, premium_duration)
- `study_data` (user_id, tool, data_json) — planner, timetable, budget, flashcards, CGPA history, bookmarks; migrated from v1 localStorage on first sign-in via an import tool, user-confirmed.
- `audit_log` (actor, action, target, at) for admin actions + premium grants.

R2 buckets: `mystudy-media` (avatars, news images), `mystudy-exports` (optional). KV: only for rate-limit counters if needed; D1 is the source of truth.

## 4. Premium + Paystack — no cheating, no bypass

- Price: ₦2,000 once, as in v1, until the user confirms otherwise. Stored in `settings.premium_price_kobo = 200000`, editable in admin.
- Admin pastes Paystack **public key + secret key** in Admin → Settings → Payments (test keys first on staging). Secret is encrypted at rest (AES-GCM, key in Cloudflare secret, never in git, never returned to the frontend).
- Flow: student clicks Upgrade → Rust creates a `payments` row (status `pending`, unique reference `MS-<random>`) → frontend opens Paystack Inline / redirect with the **public** key only → Paystack returns to `/premium/callback?reference=...` → Rust calls Paystack Verify API (`GET /transaction/verify/:reference`) with the **secret** key server-side → only on `status == success` + amount matches + reference matches the pending row does Rust set `premium_status='active'` and mark the payment `verified`. Webhook (`/api/payments/webhook`, signature verified with the secret) is the second path and also verifies via the API — a webhook alone never grants premium.
- Every premium-gated check (CBT question count, premium tools) reads `users.premium_status` from D1 in Rust on each request. The frontend never decides premium. No activation key, no device-ID key, no localStorage flag.
- Refunds / disputes are manual in Paystack dashboard + admin can revoke premium (audit-logged).

## 5. CBT — like JAMB

- JAMB format enforced: English compulsory + 3 other subjects (4 total), 180 questions (English 60, others 40 each), 2 hours (120 min) — not user-editable. WAEC/NECO/Post-UTME keep their own subject counts/times, defined in a server config table.
- Server issues an exam session with a server-side clock (`ends_at` in D1). Client timer is display only; submit after `ends_at` is rejected. Questions are served without answers/explanations; answers are submitted per-question (autosave) and scored only at submit in Rust.
- Free: 5 questions/subject (as in v1, now enforced server-side). Premium: full counts. Attempting to request more than the tier allows returns 403.
- Anti-cheat (server-enforced, client-assisted): one active session per user, session token bound to the exam, tab-blur / fullscreen-exit strikes counted server-side (3 strikes = auto-submit, as in v1's proctor), copy/paste + right-click blocked in the exam UI, questions shuffled per session from the bank (seeded server-side). Webcam proctor is NOT in Phase 1 — it needs consent, bandwidth, and a face-detection path that does not fit the free tier; the v1 webcam code is not carried over as a promise.
- Results: per-subject score, total /400 for JAMB, corrections + explanations only after submit, and only for questions that have an explanation in the bank. History kept server-side.
- Question import: normalised importer (script in `tools/import-questions/`) from the cloned repos in `/tmp/mystudy-repos/` + the audit: import only real files (JAMB 2021–2025, WAEC/NECO 2024–2025, Primary 2026, English-Quiz 900), skip the 190 placeholder files and the 11 corrupt files (list them in the import report), dedup by content hash, three schemas normalised to one, metadata (exam/subject/year) taken from filename only. Explanations and topic tags are a separate authoring task — not invented by the importer.

## 6. News (was Blog) — admin-only, full editor

- Only `admin` can create/edit/publish. Students see published News only.
- Editor fields: title, slug (auto, editable), excerpt, body (rich text: H2/H3, bold/italic, bullets, numbered lists, blockquote, code, tables, links), featured image (upload to R2 or URL), category (pick + create), tags (multi, with suggestions), SEO title (60 chars), SEO description (160), SEO keywords, OG image, status (draft / published / scheduled — scheduled is lazy: published when first read after `published_at`, no cron), author.
- Rendering keeps the v1 post format the user loves: eyebrow (category) → Fraunces serif title → meta (author/date/read-time) → share row → featured image (first image or featured, max 520 px) → TOC → body → tags → share → comments (Phase 2, moderated). TOC: scan H2/H3, slugify (max 60 chars, dedup `-2`/`-3`), show if ≥3 headings, open `<details>` with ordered list, H3 indented — same as template shell path. Fonts: Inter body, Fraunces H2, Plus Jakarta Sans H3 (Fraunces must actually be loaded in v2 — it was not in v1).
- SEO: per-post title/description/OG/Twitter + JSON-LD (NewsArticle), sitemap + RSS generated from D1.

## 7. Other tools (upgraded, Phase 2+)

All v1 tools ported to server-backed, account-linked versions, in priority order: CGPA calculator, Learn Hub (keypoints from `mystudy-textbooks`, only subjects with real chapters shown), Past Questions browser (only years with real questions), English Quiz, Flashcards, Admission Toolkit (JAMB combination checker, aggregate predictor), Study Planner / Timetable / Deadline Planner, Budget Tracker, Word/PDF/Image toolkits (client-side processing where possible, no upload of private docs by default), Citation/Summarizer, Dictionary (server-side lookup from `merged.json`, never shipped to browser), Vocabulary, Constitution library. Missing subjects/topics (CRS/IRS/Civic/History/Computer/Further Maths, JSS/Primary textbooks, syllabus/tutorials/Post-UTME/BECE) are authoring work — v2 shows them as "coming soon", not as empty shells.

**Rule (user, 24 Nov 2026): every tool must be fully rebuilt, better than v1, each with a better/different model — not a copy of the v1 localStorage JavaScript.** The registry in §11 names each tool's v2 model and its honest status (built / stubbed / planned). No tool is claimed as working until it is built and verified.

## 10. Keypoints + Vocabulary — nicely and perfectly done

### 10.1 Keypoints (server-backed, from mystudy-textbooks)

- **Source:** `mystudy-textbooks` — 166 chapters, 503 modules, 4,630 quiz questions, 12 subjects, SSS 1–3 only (audit §6). Imported once into D1 (`textbook_chapters`, migration 0002); the reader loads one module at a time from the API.
- **Reader model (different from v1):** v1 kept a 165-topic registry in the template and fetched chapter JSON from jsDelivr at runtime, showing subjects with zero topics as if they existed. v2: module reader with prev/next, progress bar, "mark module done", KaTeX maths, then a 10-question test from the chapter's quiz pool. Progress (`keypoint_progress`: modules done, best/average score, tests taken) is recorded server-side — it cannot be edited in the browser.
- **Coverage — full, no shallow topics left:** the 12 imported subjects are the starting point, not the finish. Missing subjects must be authored to full coverage: CRS, IRS, Civic Education, Computer Studies, Further Mathematics, History, Hausa, Igbo, Yoruba (no chapters at all in the repo), plus JSS 1–3 and Primary levels (no content at any level). "Full coverage" means every syllabus topic at every level taught, each with modules that teach the topic properly — not a one-paragraph stub — and a real quiz pool per chapter. Literature chapters are generic frameworks, not the JAMB prescribed texts; those are authored against the current JAMB syllabus.
- **Schema note:** Mathematics files use a different schema (`topic`/`ss_level`/`icon`/`color`) from the other 11 subjects — the P3 importer normalises both to one table.
- **Honesty rule:** only subjects with real imported chapters are offered. Everything else is "coming soon", never an empty shell. Chapter content comes verbatim from the repo; new chapters are authored against the official JAMB/WAEC/NECO syllabuses — the importer never invents module content or quiz questions.

### 10.2 Vocabulary (server-backed, from vocabulary-database)

- **Source:** `vocabulary-database` — 24 categories × 100 words = 2,400 words, the best-structured dataset in the audit: `{id, word, pos, definition, example}` (audit §8).
- **Model (different from v1):** v1 loaded words from jsDelivr at runtime and kept learned words/streaks in localStorage. v2: words in D1 (`vocabulary_words`), progress server-side (`vocabulary_progress`), 30-question tests per category as in v1, streaks from server-recorded study days.
- **Index fix:** the repo's `index.json` lists only 14 of the 24 categories — 10 categories (admin-vocabulary, animal-habitats, capability-adjectives, environment, idioms, natural-phenomena, professions, proverbs, sensory-sounds, umbrella-terms) were in the data but unreachable from v1's category list. The P3 importer regenerates the index from the data files; it never trusts the repo's index.
- **Filling the gaps:** every omitted category gets filled and topics go to full coverage — no shallow or half-done categories left. New categories follow the existing schema exactly: 100 words each as `{id, word, pos, definition, example}`, plus 100 quiz questions per category (`vocabulary_quizzes`), and the index is updated to list every category. Words and quiz questions come from real vocabulary sources and the syllabus — the importer never invents definitions or examples.

## 11. Tools registry — every v1 tool, its v2 model, its status

The registry lives in code at `apps/web/src/lib/tools.ts` and is rendered at `/tools` in the React shell. Status meanings: **built** (implemented in the scaffold and verified — see `docs/phase1-build-24-nov.md`), **stubbed** (UI/API exists but the write path is not wired yet, and it says so), **planned** (design + model named, not built yet — never shown as working).

| Tool | v2 model (different from v1) | Status | Phase |
|---|---|---|---|
| Home dashboard | React shell; stats from D1 per user; News from GET /api/news | built | P1 |
| Register / Sign in | Rust: PBKDF2, compulsory TOTP, 3 security questions, lockout, opaque sessions | built | P1 |
| News read | Admin-only editor; read path live from D1, v1 post format + TOC | built | P1 |
| News editor | Title/slug/excerpt/body, image URL or R2 upload, category, tags, SEO, draft/published/scheduled | stubbed | P1/P2 |
| Profile | Display name, avatar to R2, bio, exam target, subjects, target score, theme/accent; server sync in P2 | built (shell) | P1/P2 |
| CBT Practice | Rust exam sessions: server clock, seeded shuffle, server-side scoring, D1 premium check, 3-strike anti-cheat | planned | P2 |
| Premium + Paystack | Admin pastes keys; server verifies via Paystack API + webhook signature; premium flips only on verified success | planned | P2 |
| Keypoints | Server-backed chapters (§10.1); module reader + 10-Q tests; full-coverage authoring | planned | P3 |
| Vocabulary | Server-backed words (§10.2); regenerated 24-category index; 100 Qs per category | planned | P3 |
| Past Questions browser | Reads the normalised questions table; only years with real questions offered | planned | P3 |
| English Quiz | Server-backed from the 900 current questions (Old* twins dropped); timed, explanations after submit | planned | P3 |
| Dictionary | Server-side lookup from merged.json (121,340 entries); 72 MB dictionary never shipped to the browser | planned | P4 |
| CGPA Calculator | Exact decimal math (integer hundredths, no float); semesters saved server-side; server-generated transcript | planned | P4 |
| Graduation Predictor / GPA→Class | Same exact-math engine as CGPA; reads saved semesters from D1 | planned | P4 |
| Admission Toolkit | Server-side course table; aggregate formulas per university, versioned in D1 | planned | P4 |
| Flashcards (Leitner) | Server-backed decks in study_data; 3-box scheduling computed server-side | planned | P4 |
| Exam Planner / Lecture / Study Planner / Timetable / Revision / Deadline / Outline | Server-backed in study_data; server clock; revision generator uses Keypoints progress (weak topics first) | planned | P4 |
| Budget Tracker | Integer-kobo money (never float); expenses server-side; summaries in Rust | planned | P4 |
| Study Streak & XP | Server-side streak from recorded activity; XP rules in Rust, one source of truth | planned | P4 |
| Word Office | React editor; DOCX read via mammoth, write via docx lib, client-side PDF export; docs optionally in R2 | planned | P4 |
| PDF Toolkit | Client-side pdf-lib (files never leave the device); server fallback for large files; OCR via Workers AI, labelled AI, optional | planned | P4 |
| Image Toolkit | Canvas + Web Worker processing; saved outputs to R2; EXIF stripped client-side before upload | planned | P4 |
| Word & Character Counter | Client-side; words, characters, sentences, reading time | planned | P4 |
| Citation Generator / Quick Cite | Local templates formatting ONLY user-supplied metadata — citations never invented; optional Workers AI metadata extraction, labelled AI-suggested | planned | P4 |
| Note Summarizer | Local extractive summarizer first (no invented content); optional Workers AI abstractive, labelled AI | planned | P4 |
| Text Compare | Client-side Myers diff, word-level highlighting | planned | P4 |
| Constitution Library | Server-side sections (227, Ch. I–VIII); search in Rust; amendment status verified before presenting as current law | planned | P4 |
| Unit Converter | Client-side exact tables; rational factors, exact temperature formulas | planned | P4 |
| Chart Generator | Client-side canvas charts; PNG/CSV export locally; data never leaves the device | planned | P4 |
| Bookmarks | Server-backed per user (study_data) | planned | P4 |
| Study Assistant chatbot | Workers AI with tool-aware context; answers about tools only, never invents exam answers; v1 bot endpoint not carried over as-is | planned | P5 |

## 8. Phases

- **P0 — Discovery (done 24 Nov):** template inventory + repo audit.
- **P1 — Scaffold + Auth + News read path (this build):** monorepo, Rust API + D1 migrations, React shell with v1 design, registration + TOTP QR + security questions, sign-in, profile, News list + post page with TOC, admin editor (create/publish), staging deploy.
- **P2 — Paystack + Premium (server-verified) + CBT JAMB:** payments, premium gating, exam sessions, scoring, results, anti-cheat strikes.
- **P3 — Question import + Learn Hub + Keypoints/Vocabulary:** normalised import, past-questions browser, keypoints (§10.1), English Quiz, vocabulary (§10.2, index regenerated to all 24 categories).
- **P4 — Remaining tools + PWA offline:** CGPA, planner, budget, toolkits, dictionary/vocabulary, offline packs — every tool rebuilt to its §11 model, not a copy of v1.
- **P5 — Cutover:** staging walkthrough, data migration from Blogger (News posts), DNS for mystudy.name.ng, rollback = Blogger stays as-is until cutover is confirmed.

## 9. Open decisions (need the user, not blocking P1)

1. Premium price: stay ₦2,000 once? 2. Paystack keys: test keys for staging, live keys only when ready — never in chat. 3. First admin: ola1de.olawande@gmail.com? 4. JAMB English compulsory: enforce in v2 (v1 did not)? Assumed yes — confirm. 5. Webcam proctor: in or out for P2?
