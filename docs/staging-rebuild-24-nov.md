# MyStudy v2 — Staging UI rebuild + real News editor (24 Nov 2026)

**Staging:** https://mystudy-v2-staging.ola1de-olawande.workers.dev
**Worker version:** `3b2c58ee-19ef-4822-8e49-22b697c4c917` (WASM 763,550 bytes; startup 13 ms)
**GitHub:** https://github.com/ola1de/MyStudy-v2 (scaffold pushed in 3 chunks:
`fc0b561`, `086bfbc`, `370524e`; rebuild pushed as a further snapshot — see
the sync record at `~/workspace/mystudy.muse-github-snapshot-sync.json`).

## Why: the user visited staging and judged it, rightly, poor
Worse than the Blogger site: no images, no elements, no icons, no SVGs,
everything on a single plain page, not structured, not user-friendly, no
school/educational feel. And "everything about the website is screaming AI
generated" — the rebuild below is built from the v1 template's own design
language, not from a generic template.

## Part A — scaffold on GitHub (done)
All 335 scaffold files pushed. The one exception: `.github/workflows/deploy.yml`
cannot be pushed by the Muse GitHub App (403 on tree creation whenever that
path is included — GitHub Apps cannot write workflow files via the API). It
exists locally only; add it via the GitHub web UI, as with Proseforge's CI
workflow. The two Cloudflare secrets (`CLOUDFLARE_API_TOKEN`,
`CLOUDFLARE_ACCOUNT_ID`) still need pasting by the user before Actions deploy
can run. Staging redeploys keep working from the VM launcher
(`scripts/deploy-staging-vm.py`).

## Part B — the News post editor (done, verified live 26/26 checks)
Backend (Rust, `workers/api/src/lib.rs` only): the 501 stub is gone.
- `POST /api/admin/news` (201), `GET /api/admin/news` (filters status/category/q),
  `GET /api/admin/news/:slug`, `PUT /api/admin/news/:slug`, `DELETE /api/admin/news/:slug`
- `GET/POST /api/admin/news-categories` (seeds JAMB, WAEC, NECO, Admissions, Study Tips, Announcements)
- `POST /api/admin/upload` (images only, ≤2 MB, R2 `news/<yyyymm>/<hex>.<ext>`)
- `GET /api/media/*` (public, `news/` keys only)
- All admin routes enforce role in Rust (403 otherwise). body_html is sanitised
  (script/iframe/object/embed/form stripped, `on*` attributes and `javascript:`
  links dropped). TOC built server-side from H2/H3 (same slugify rules as
  `lib/toc.ts`, ≥3 headings). `published_at` normalised to SQLite datetime so
  lazy publishing works. `cargo test` 12/12, `cargo check` 0 warnings.
- Frontend (`AdminPosts.tsx`, rewritten `AdminEditor.tsx`, `admin.css`):
  posts list (search, category/status filters, edit/delete), Blogger-style
  editor (contenteditable toolbar: H2/H3, bold/italic, lists, blockquote, code,
  link, image), featured image via R2 upload or URL, category picker + create,
  tags, excerpt, SEO title (60) / description (160) / keywords / OG image,
  draft/published/scheduled + publish date, Save draft / Publish / Preview
  (v1 post format with TOC).
- Live end-to-end test (`/tmp/mystudy-e2e-test.py`, throwaway accounts,
  random passwords never printed/stored, accounts deleted after): **26/26
  passed**, including create → publish → public read → edit → duplicate slug
  409 → delete draft → 403 as non-admin → oversize upload 400. One test-run
  hiccup: Python urllib is dropped by the edge (403/RemoteDisconnected) —
  the script uses curl throughout.
- Seeded post (published, live): "MyStudy v2 is coming: accounts, a real CBT
  and a bigger question bank" — `/news/mystudy-v2-is-coming-accounts-a-real-cbt-and-a-bigger-questi`,
  4-heading TOC, featured banner image served from R2 via `/api/media`.
  No permanent admin account was created: the seed post's author is NULL
  after the throwaway test accounts were deleted. **The user/owner still needs
  a real admin account** (register on staging, then promote via D1
  `UPDATE users SET role='admin'`) before they can use the editor themselves.

## Part C — homepage rebuild (done, verified live)
Direction: v1 template's own language, not a generic AI site. No gradient
hero, no "Good morning, scholar", no identical rounded cards.
- Masthead: "Focus. Practice. Graduate stronger." (the v1 greeting),
  honest copy, hand-built SVG scene (open book, graduation cap, stacked books,
  pencil — `components/HeroArt.tsx`), dark navy header strip, Fraunces headings.
- Every number generated from the repos (`tools/generate-content-data.py` →
  `apps/web/src/data/content.ts`): 11,267 past questions (JAMB 5,235 / WAEC
  2,728 / NECO 2,744 / Primary 560), 8,580 syllabus-modelled practice
  questions, 13,650 keypoint quiz questions / 273 chapters / 1,482 modules,
  4,400 vocabulary words / 44 categories.
- Sections: bank strip, CBT band (real JAMB rules: 180 questions, 2 hours,
  English compulsory), 21-subject index with real counts, Keypoints +
  Vocabulary sections, tools grouped in rows (not cards), News (real posts),
  contact band (mystudyacademicsuite@gmail.com, WhatsApp +234 810 025 9673).
- Shared SVG icon library (`components/icons.tsx`, one 24-grid stroke).
- Keypoints page: real subject table (chapters, quiz counts). Vocabulary page:
  all 44 real categories + search. Tools page: grouped by honest status
  (built / shell only / planned). Post page: author "MyStudy" (v1 showed
  "Unknown"), bottom share bar.
- `npm run build` passes (110 modules; JS 357 KB, CSS 16.5 KB). Live JS bundle
  verified to contain the new masthead copy.

## Still incomplete / honest gaps
- The editor UI flow was verified through the exact API calls the editor
  makes, plus build checks — no live-browser click-through was possible from
  this VM (no live-browser tool in this session). `document.execCommand`
  toolbar buttons (notably Code/blockquote) compile but were not exercised
  in a real browser.
- Keypoints reader and Vocabulary trainer are still P3 (pages list real
  content; the reader/trainer are not built). CBT, Paystack and the other
  tools are still planned per the Tools page — none is claimed as working.
- 2,071 practice keypoint questions and 122 vocabulary terms still need
  human subject review. JSS/Primary keypoints and Literature prescribed
  texts are still missing.
- No permanent staging admin account exists yet (see above).
- `.github/workflows/deploy.yml` still needs adding via the web UI, and the
  two Cloudflare secrets pasting, before GitHub Actions deploy can run.

## Not touched
Live Blogger site mystudy.name.ng, DNS, production D1/R2. Staging only.
