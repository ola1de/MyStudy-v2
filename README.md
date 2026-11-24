# MyStudy v2 — Phase 1 scaffold

React 19 + Vite + TypeScript frontend, Rust backend compiled to WASM on
Cloudflare Workers via `workers-rs` (`worker` 0.9 + `worker-build` 0.9.0),
D1 + R2. Blogger v1 stays live at mystudy.name.ng until v2 passes a
staging walkthrough + written approval. Nothing here has been deployed.

Design: `docs/architecture-24-nov.md`. Template inventory:
`docs/template-inventory-24-nov.md`. Repo audit:
`docs/repo-audit-24-nov.md`. Build log: `docs/phase1-build-24-nov.md`.

## Layout

```
mystudy/
  apps/web/            React SPA (home, News, post page with TOC, auth, profile, admin editor shell)
  workers/api/         Rust worker crate (mystudy-worker) + D1 migrations
  tools/import-questions/  Node importer: Exam-Questions-Data JSON -> canonical seed SQL
  wrangler.toml        staging only; production is a separate P5 step
  scripts/build-worker.sh
```

## Toolchain (measured 24 Nov 2026)

- node v24.22.1, npm 10.9.4, wrangler 4.167.0 (via npx)
- rustc 1.100.0, cargo 1.100.0, worker-build 0.9.0, wasm32-unknown-unknown target
  — already installed at `~/.cargo/bin` (add to PATH: `export PATH="$HOME/.cargo/bin:$PATH"`).
  No rustup install was needed.
- worker-build needs a wasm-bindgen CLI and esbuild. In this VM they are
  supplied from local installs by `scripts/build-worker.sh`
  (`$HOME/.cargo-wb01/bin/wasm-bindgen`, esbuild from the wordless repo's
  node_modules — read-only reuse, nothing copied). On a normal machine
  worker-build downloads its own tools and the overrides are unset.
- Build with `--no-opt` in this VM: wasm-opt's binaryen download is blocked
  here. `scripts/build-worker.sh` runs wasm-opt `-Oz` itself when a
  `wasm-opt` binary is available (wordless node_modules has one).

## Setup

```bash
export PATH="$HOME/.cargo/bin:$PATH"
npm install
npm run build            # builds apps/web -> apps/web/dist
npm run import:questions # runs the question importer (reads /tmp/mystudy-repos)
bash scripts/build-worker.sh   # builds workers/api -> build/worker/shim.mjs
npx wrangler deploy --dry-run  # validates wrangler.toml without deploying
```

Local dev (no Cloudflare account needed for the frontend):

```bash
npm run dev:web          # Vite dev server for apps/web
npx wrangler dev         # local Worker with local D1/R2 (from repo root)
```

## Auth (Phase 1, per architecture §2)
- Registration: name, email, password (min 12), exam target, **3 different
  security questions** picked from a fixed list of 12 (see
  `workers/api/src/security_questions.rs`). Answers are normalised
  (lowercase, trim) and PBKDF2-hashed server-side — never stored plaintext.
- **TOTP is compulsory at registration:** `POST /api/auth/register-start`
  returns an `otpauth://` URL + base32 secret; the frontend renders the QR
  as an SVG **locally** (no external QR service at runtime) and offers a
  manual-code copy button. The account is unusable until
  `POST /api/auth/totp-verify` succeeds with a valid 6-digit code from the
  user's authenticator app. 10 one-time recovery codes are issued once.
- Sign-in: email + password, then TOTP code (or a burned recovery code).
  5 failed attempts → 15-minute lockout. Sessions are opaque tokens;
  only the SHA-256 hash is stored in D1; cookie is HttpOnly/Secure/SameSite=Lax.
- Roles: `student` (default), `admin`. Only an admin can create News
  (`POST /api/admin/news` returns 403 otherwise — enforced in Rust).

## Keypoints + Vocabulary (design in Phase 1, build in P3)

- **Keypoints** (architecture §10.1): server-backed chapters from `mystudy-textbooks`
  (166 chapters, 503 modules, 4,630 quiz questions, 12 subjects SSS 1–3). Tables in
  `workers/api/migrations/0002_keypoints_vocab.sql`. Missing subjects (CRS, IRS, Civic,
  Computer, Further Maths, History, Hausa, Igbo, Yoruba) + JSS/Primary are authoring work
  to full coverage — no shallow topics left. Design page: `/keypoints`.
- **Vocabulary** (architecture §10.2): server-backed words from `vocabulary-database`
  (24 categories × 100 words, `{id, word, pos, definition, example}` + 100 quiz
  questions per category). The P3 importer regenerates the category index from the data
  files — the repo's `index.json` lists only 14 of 24 categories. Design page: `/vocabulary`.

## Tools registry

Every v1 tool, its v2 rebuild model, and its honest status (built / stubbed / planned)
lives in `apps/web/src/lib/tools.ts` and renders at `/tools`. The rule: every tool is
fully rebuilt, better than v1, each with a better/different model — not a copy of the
v1 localStorage JavaScript. No tool is claimed as working until it is built and verified.
The full table is in `docs/architecture-24-nov.md` §11.

## Known Phase 1 limitations (honest)

- `totp_secret_enc` is stored as the base32 secret in D1 in Phase 1.
  P2 must encrypt it at rest (AES-GCM, key in a Cloudflare secret) — see
  the TODO in `workers/api/src/auth.rs`. The same applies to Paystack
  secrets in `settings` (P2, architecture §4).
- `POST /api/admin/news` is a stub that validates the admin role and the
  payload, then returns 501 until the D1 insert lands in P2. News **read**
  paths (`GET /api/news`, `GET /api/news/:slug`) are real and work against D1.
- Email verification codes are not sent in Phase 1 (no email provider
  wired yet) — registration completes after TOTP verification; email
  verification is a P2 item.
- No Paystack code in Phase 1 (P2). No secrets of any kind are in this repo.

## Deploy (staging only, when the user approves — NOT run in Phase 1)

```bash
wrangler d1 create mystudy-db-staging
wrangler d1 migrations apply mystudy-db-staging --env staging
wrangler r2 bucket create mystudy-media-staging
wrangler deploy --env staging
```

Then fill the real database/binding ids into `wrangler.toml` for staging.
Production cutover (DNS for mystudy.name.ng) is P5 and needs the user's
written approval.
