# MyStudy v2 — Staging deploy report (24 Nov 2026, ~02:10 WAT)

**Staging is LIVE:** https://mystudy-v2-staging.ola1de-olawande.workers.dev
- `/api/health` → `{"ok":true,"data":{"service":"mystudy-v2","status":"ok","version":"0.1.0"}}`
- `/api/news` → `{"ok":true,"data":{"posts":[]}}` (no posts yet — expected)
- Homepage renders (React SPA, "Good morning, scholar").
- Worker version ID `4ca04074-f6da-4248-8f64-62e86d3f4600`, startup 12 ms, WASM 587,269 bytes.
- D1 migrations applied to mystudy-db-staging: all 22 tables present
  (users, sessions, password_resets, login_attempts, profiles, news_posts,
  news_categories, payments, settings, questions, exam_sessions, study_data,
  audit_log, textbook_chapters, keypoint_progress, vocabulary_categories,
  vocabulary_words, vocabulary_quizzes, vocabulary_progress, d1_migrations).

## Cloudflare resources (account b4fc7bb3e29957d6e05fda13b6330adf)

| Resource | Name | ID |
|---|---|---|
| D1 (prod, for P5 cutover) | mystudy-db | f8258cd8-5dd0-4f3b-b930-aea5b3c91ba7 |
| D1 (staging) | mystudy-db-staging | 25b6e57e-8c92-4ef7-8d06-548b0c8d39d6 |
| R2 (prod, for P5 cutover) | mystudy-media | (bucket, created 2026-11-24T01:55:06Z) |
| R2 (staging) | mystudy-media-staging | (bucket, created 2026-11-24T01:55:08Z) |

Deploy was done **directly from this VM** with
`~/workspace/mystudy/scripts/deploy-staging-vm.py` (wrangler + the scoped
token via its hsurr: surrogate — the swap works for wrangler). Redeploy
any time with `python3 scripts/deploy-staging-vm.py` from
`~/workspace/mystudy/`. `wrangler.toml` now carries the real D1 IDs.

## GitHub — repo and pushes

- **Repo:** https://github.com/ola1de/MyStudy-v2 — public, created by the user
  2026-11-24T01:54:55Z, default branch main. **Currently EMPTY — the Phase 1
  scaffold is NOT on GitHub yet** (see blocker below).
- Local scaffold commits (in `~/workspace/mystudy/`, not pushed):
  `1261399` (Phase 1 scaffold + staging IDs + deploy workflow),
  `de84e32` (VM deploy launcher). Build verified: `npm run build` passes,
  `cargo test` 6/6.

### Pushed and verified on GitHub

**vocabulary-database** — 1 commit, 45 files, 2.36 MiB:
- `46cfe595b854881f3a36819e0e553c4aae4a997d` — 24→44 categories,
  2,400→4,400 words, index v3. Verified: index.json on main lists 44
  categories. https://github.com/ola1de/vocabulary-database/commit/46cfe595b854881f3a36819e0e553c4aae4a997d

**Exam-Questions-Data** — 5 commits, 201 files, 5.95 MiB:
- `050f5212dbd7b945365a764a3744f3eef09a8fc9` — JAMB 2020 + Hausa 2023 (22 files, 900 Qs)
- `e792392a8c70b196caf1db16cfa141682f9f9798` — WAEC part 1 (44 files)
- `576deedd6e34b3221caad29c06943e1234bebfd3` — WAEC part 2 (44 files)
- `ac25f20eee9f95bbcdc3ed0da813d8bf36509db2` — NECO part 1 (46 files)
- `1a41035d8a2febd32be4628ed3f92a8446a23afe` — NECO part 2 (45 files, HEAD)
  Verified: NECO_Chemistry_2024.json parses on GitHub with real questions +
  explanations; JAMB_English_2020.json has filled passage content.

**mystudy-textbooks** — 3 commits, 274 files, 8.48 MiB:
- `59e03e81f6fbe6cff10c0439435ccb564da8234d` — part 1 (accounting, agric, biology, chemistry, civic, commerce, computer)
- `9af7221e93babf7010d82a1d863b78941f23e583` — part 2 (CRS, economics, English, further maths, geography, government, Hausa)
- `d1b7de2cddd810bf09f2928a5ad1542d06c4e4f8` — part 3 (history, Igbo, IRS, literature, mathematics, physics, Yoruba, HEAD)

Sync records saved next to each durable clone
(`<repo>.muse-github-snapshot-sync.json` under
`~/workspace/mystudy/data-repos/`).

**NOT pushed:** English-Quiz (its duplicates fix was lost in /tmp and is
not in a durable copy — needs redoing first).

### Push mechanics learned
- The GitHub MCP `push_files` transport rejects payloads around 6 MiB
  (HTTP 413). All pushes above were split into ≤ ~3.5 MiB chunks.
- Scaffold chunks are prepared in `/tmp/mystudy-chunk-{1-core,2-docs,3-tools,4-seed}.nul`
  (0.21 / 3.5 / 1.6 / 4.7 MiB). Chunk 4 (the 4.7 MiB generated seed SQL)
  may still 413 — if so, drop it from the repo; it regenerates with
  `npm run import:questions`.
- Scaffold snapshot excludes: `data-repos/`, `node_modules/`, `target/`,
  `dist/`, `build/`, `.wrangler/`, `__pycache__`/`*.pyc`, and the downloaded
  JAMB syllabus PDFs under `docs/fixes-24-nov/jamb-gen/syllabus/` (binary —
  the connector cannot push non-UTF-8 files). These stay local only.

## BLOCKER — one user step needed to finish the GitHub side

Pushing to **ola1de/MyStudy-v2 fails with 403 "Resource not accessible by
integration"** (tried twice, 01:57 and 02:08 WAT). The Muse GitHub App is
installed on the three data repos (those pushes worked) but **not on the
new MyStudy-v2 repo**, and the app cannot create repos or self-install.
The user must add it:

1. Open https://github.com/apps/meta-muse-ai/installations/new
2. Select the **ola1de** account and add repository **MyStudy-v2**
   (all repositories, or at least MyStudy-v2).
3. Tell Muse it's done — then the scaffold pushes in 4 chunks
   (above) and the GitHub Actions workflow will run.

After the scaffold is on GitHub, the auto-deploy workflow
(`.github/workflows/deploy.yml`, already written locally) needs two
GitHub Secrets on the repo (Settings → Secrets and variables → Actions):
- `CLOUDFLARE_API_TOKEN` — the same scoped Cloudflare token as
  WORDLESS/Proseforge. **Muse cannot read the token value back, so the
  user must paste it.**
- `CLOUDFLARE_ACCOUNT_ID` — `b4fc7bb3e29957d6e05fda13b6330adf`
Until those are set, the workflow will fail; staging redeploys keep
working from the VM launcher meanwhile. Do NOT claim GitHub Actions
deploy is live until a workflow run goes green.

## Not touched
- Live Blogger site mystudy.name.ng — untouched. No DNS change, no
  domain cutover. Cutover needs staging walkthrough + written approval.
- No secrets, tokens, passwords or Paystack keys were committed anywhere.
