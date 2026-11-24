# MyStudy v2 — Phase 1 build log (24 Nov 2026)

Scaffold only. Nothing deployed to Cloudflare, nothing pushed to GitHub,
nothing changed on the live Blogger site. Blogger v1 stays live at
mystudy.name.ng until the P5 cutover gate.

## Toolchain (measured 24 Nov 2026)

| Tool | Version | How found |
|---|---|---|
| node | v24.22.1 | `node -v` |
| npm | 10.9.4 | `npm -v` |
| wrangler | 4.167.0 via npx | `npx wrangler --version` |
| rustc / cargo | 1.100.0 | `~/.cargo/bin` (already installed — **no rustup install was needed**; the toolchain was in `~/.cargo/bin` but not on PATH, so builds export `PATH="$HOME/.cargo/bin:$PATH"`) |
| worker-build | 0.9.0 | `~/.cargo-wb01/bin/worker-build` |
| wasm32-unknown-unknown | installed | `rustup target list --installed` |
| wasm-bindgen CLI | present at `~/.cargo-wb01/bin/wasm-bindgen` | supplied to worker-build via `WASM_BINDGEN_BIN` in `scripts/build-worker.sh` |
| esbuild / wasm-opt | present in wordless `node_modules/.bin` | read-only reuse by `scripts/build-worker.sh`; nothing copied |

## Commands + results

### 1. Question importer

```
$ node tools/import-questions/import.mjs
files: 389 total, 199 imported, 190 placeholder-skipped, 0 corrupt-skipped
questions: 11267 seen, 11267 imported, 0 deduped, 2962 with explanations
wrote tools/import-questions/out/report.json and tools/import-questions/out/questions-seed.sql
```

Outputs: `tools/import-questions/out/report.json`,
`tools/import-questions/out/skipped.json`,
`tools/import-questions/out/questions-seed.sql` (29,444 lines).

**Discrepancy vs the repo audit — explained, not hidden.** The audit
(`docs/repo-audit-24-nov.md` §2.3–2.4) counted 11 corrupt files and 10,527
real questions. The importer found **0 corrupt files and 11,267 questions**.
Reason, verified the same day: the 11 files were already repaired in the
working tree of the `/tmp/mystudy-repos/Exam-Questions-Data` clone
(`git status` shows 11 modified files, uncommitted, e.g.
`M json/WAEC_Physics_2024.json`, 1,026 insertions / 24,859 deletions —
mostly reformatting). The importer read the repaired working-tree files.
Against committed HEAD those 11 files would still fail to parse. The
importer itself repaired nothing and invented nothing.

- Placeholder files skipped: **190** — exactly the audit's count.
- 1 question excluded as invalid: `NECO_Computer_2024.json`, a question
  with 5 options (expected 4). It is listed in `report.json`
  (`questions_invalid`). The repaired file still needs that question fixed.
- Explanations: 2,962 of 11,267 (WAEC/NECO 2024 mostly; JAMB 0, Primary 0).
- Dedup: 0 within (exam, subject, year). `topic` is NULL for all 11,267
  rows until a syllabus-based authoring pass assigns topics.
- Placeholders are NOT filled by the importer. Per the user's
  question-bank rule (24 Nov), filling them is a separate syllabus-modelled
  authoring task, labelled `practice:true`, never presented as verbatim
  official papers.

Seed verified by loading it into the migration schema (Python sqlite3,
in-memory):

```
questions rows: 11267
by exam: JAMB 5235, NECO 2744, PRI 560, WAEC 2728
with explanations: 2962
distinct hashes: 11267
topics null: 11267
```

### 2. D1 migrations

```
$ python3 (sqlite3, in-memory): apply 0001_init.sql + 0002_keypoints_vocab.sql
tables: audit_log, exam_sessions, keypoint_progress, login_attempts,
news_categories, news_posts, password_resets, payments, profiles,
questions, sessions, settings, study_data, textbook_chapters, users,
vocabulary_categories, vocabulary_progress, vocabulary_quizzes,
vocabulary_words  (20 tables incl. sqlite_sequence)
```

`0001_init.sql`: users, sessions, password_resets, login_attempts,
profiles, news_categories, news_posts, payments, settings
(premium_price_kobo = 200000 = ₦2,000 once), questions, exam_sessions,
study_data, audit_log. `0002_keypoints_vocab.sql`: textbook_chapters,
keypoint_progress, vocabulary_categories, vocabulary_words,
vocabulary_quizzes, vocabulary_progress.

### 3. React web app

```
$ npm install --workspace=apps/web react@19 react-dom@19 react-router-dom@7 \
    qrcode @types/qrcode vite@6 @vitejs/plugin-react@4 typescript@5
added 102 packages in 22s
$ npm install --workspace=apps/web -D @types/react@19 @types/react-dom@19

$ npm run build
vite v6.4.6 building for production...
✓ 105 modules transformed.
dist/index.html  1.02 kB
dist/assets/index-*.css  4.84 kB
dist/assets/index-*.js  326.70 kB (gzip 105.95 kB)
✓ built in 2.64s
```

First build failed: `tsc` reported `JSX.IntrinsicElements` missing —
`@types/react` / `@types/react-dom` had not been installed (React 19
does not bundle them). Fixed by installing the two `@types/*@19`
dev packages; no source change was needed.

Pages built: Home, News list, Post page (TOC from H2/H3, v1 format),
Register (3 security-question dropdowns + TOTP QR rendered locally as
SVG + manual-code copy + recovery codes shown once), Login (password,
then TOTP/recovery code), Profile (customisable fields; browser-only in
P1, labelled as such), Admin editor shell (title/slug/excerpt/body,
image URL, category, tags, SEO fields, status, TOC preview), Tools
registry (`/tools`), Keypoints design (`/keypoints`), Vocabulary design
(`/vocabulary`).

### 4. Rust worker

```
$ cargo test
running 6 tests
test totp::tests::base32_roundtrip ... ok
test totp::tests::hotp_rfc4226_vectors ... ok   (RFC 4226 Appendix D vectors)
test totp::tests::otpauth_url_shape ... ok
test totp::tests::totp_verify_window ... ok
test auth::tests::recovery_codes_shape ... ok
test auth::tests::password_roundtrip ... ok
test result: ok. 6 passed; 0 failed
```

First `cargo test` failed with 40 errors — all my API misuse, fixed the
same day: `JsValue` is not re-exported by `worker::*` (added
`use wasm_bindgen::JsValue`); `worker::Method` has no `as_str`
(match on the enum directly); `Fetcher::fetch` takes a URL string +
`Option<RequestInit>` (use `fetch_request` for a `Request`);
`Request::new` takes `(url, method)`. No WORDLESS code was copied;
the worker was written from the `worker` 0.9 crate docs and the
architecture doc.

4 dead-code warnings remained (fields/functions kept for P2 handlers);
fixed with `#[allow(dead_code)]` + comments. Final `cargo check`:
clean, 0 warnings.

```
$ bash scripts/build-worker.sh
worker-build --release --no-opt ... Done in 1m 45s
build-worker: wasm-opt -Oz: 857840 -> 587269 bytes (free-tier limit 3145728)
```

WASM 587,269 bytes after `-Oz` — well under the 3 MiB free-tier limit.
`workers/api/build/worker/shim.mjs` present.

### 5. Wrangler validation (no deploy)

```
$ npx wrangler deploy --dry-run
[custom build] build-worker: wasm-opt -Oz: 857840 -> 587269 bytes
✨ Read 4 files from the assets directory /home/hatch/workspace/mystudy/apps/web/dist
Total Upload: 617.40 KiB / gzip: 241.76 KiB
Your Worker has access to the following bindings:
Binding  Resource
env.DB (mystudy-db)  D1 Database
env.MEDIA (mystudy-media)  R2 Bucket
env.ASSETS  Assets
--dry-run: exiting now.
DRYRUN_EXIT=0
```

No deploy was run. Staging/production database ids in `wrangler.toml`
are placeholders (`00000000-...`); real ids are filled at deploy time.

## What is built, stubbed, planned (honest status)

- **Built + verified:** React shell + News read (`GET /api/news`,
  `GET /api/news/:slug`, lazy scheduled publishing); auth
  (`register-start` → TOTP QR/manual code → `totp-verify` →
  `login`, PBKDF2 passwords, lockout, opaque sessions); TOTP
  (RFC 6238, hand-rolled base32 + HMAC-SHA1, RFC 4226 test vectors
  pass); security questions (fixed list of 12, answers PBKDF2-hashed);
  question importer + seed SQL; migrations 0001 + 0002.
- **Stubbed:** `POST /api/admin/news` — checks the D1 admin role
  (403 otherwise), validates the payload, then returns 501: the D1
  insert lands in P2. Admin editor UI exists and reports this honestly.
  Profile page saves in the browser only in P1 (labelled as such).
- **Planned (design + model named, not built):** Paystack + premium
  (P2), CBT JAMB sessions + anti-cheat (P2), Keypoints import + reader
  (P3), Vocabulary import + trainer (P3), Past Questions browser (P3),
  English Quiz (P3), all other tools (P4, registry in
  `apps/web/src/lib/tools.ts`, rendered at `/tools`, full table in
  `docs/architecture-24-nov.md` §11), Study Assistant (P5), cutover (P5).

## Known Phase 1 limitations (restated)

- `totp_secret_enc` is stored as the base32 secret in D1. P2 must
  encrypt it at rest (AES-GCM, key in a Cloudflare secret) — TODO in
  `workers/api/src/auth.rs` and README. Same for Paystack secrets.
- Email verification codes are not sent in Phase 1 (no email provider
  wired yet); registration completes after TOTP verification.
- No Paystack code in Phase 1. No secrets anywhere in the repo.
- Password hashing is PBKDF2-HMAC-SHA256 at 60,000 iterations (not
  100,000) — a deliberate Phase 1 choice for the 10 ms free-tier CPU
  limit; measure on staging before raising it. The stored format
  carries the iteration count, so raising it later does not break
  existing logins.

## Left for P2 (in priority order)

1. `POST /api/admin/news` D1 insert (sanitised body_html, toc_json
   from H2/H3, R2 image upload) + News sitemap/RSS.
2. TOTP secret encryption at rest (AES-GCM) + email verification.
3. Paystack: admin settings UI for keys, create/verify/webhook
   endpoints, premium flip only on verified success.
4. CBT: exam sessions, JAMB format (English compulsory + 3 subjects,
   180 Qs, 120 min), server-side scoring, anti-cheat strikes.
5. Password reset flow: email code + 2 of 3 security answers
   (`verify_security_answer` and `totp_code` are already written for it).
6. Profile server sync + avatar upload to R2.
