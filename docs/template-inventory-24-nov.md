# MyStudy Blogger Template — Deep Inventory

**Source file:** `~/workspace/user/files/theme-5334759134063131007__8__0_xo41.xml`
**File:** 1,725,121 bytes, 24,439 lines (`wc -l` reports 24,438 — no trailing newline) — **not edited**
**Template identity:** MyStudy Academic Suite v4, design system v15 "Quiet Confidence" (comment, line 722)
**Inventoried:** 24 Nov 2026, by parsing the file with Python/regex and reading the relevant code sections. Line numbers below refer to this file.
**Scope rule:** only what is in the file is recorded. Question banks, Keypoints JSON, dictionary and constitution texts live in external GitHub repos and are **not** in this file, so this inventory records the *references* to them, not their contents. Where the template renders a tile/list unconditionally, that is stated — it does not prove the underlying posts or files exist.

## 0. How the template works

- Blogger XML theme (`b:defaultwidgetversion='2'`, `b:layoutsVersion='3'`, responsive). It is a single-page app inside Blogger: one `<section class="view" id="view-…">` per tool, switched by a JS router (`history.pushState`, lines ~11945+).
- Routes are `?p=<route>` (48 distinct `?p=` values found) and `#<route>` hash routes; static pages are `/p/<slug>.html` (about, about-us, contact, contact-us). Blogger's real Blog1 widget still renders posts; the theme then re-renders them into its own shell or a "native" reader (see §4).
- **Local-first, no server user accounts.** All user data lives in `localStorage` (main blob `MST_APP_DATA`, plus per-tool keys — see Appendix C). There is no sign-in, no password, no Google auth, no QR code, no security questions and no Paystack anywhere in the file (Paystack: 0 hits; "security question": 0 hits).
- **External data sources referenced** (all `cdn.jsdelivr.net/gh/ola1de/…` unless stated): `Exam-Questions-Data@main/json/` (CBT), `English-Quiz@main/` (English Quiz), `mystudy-textbooks` (Keypoints), `vocabulary-database@main` (Vocabulary), `mystudy-dic@main/data/` (Dictionary), `nigeria-constitution@main/` (Constitution), `mystudy-pwa@main/sw.js` (service worker), `bot.mystudysuite.workers.dev` (Study Assistant chatbot), `mystudy-licensing.mystudysuite.workers.dev` (licensing/admin). Libraries via cdnjs/unpkg: Font Awesome, html2canvas, jsPDF, mammoth, pdf-lib, TinyMCE, docx-preview, html-docx-js, jszip, KaTeX (math rendering in CBT/Keypoints).
- PWA: inline base64 manifest (`MyStudy Academic Suite`, start URL `/`, theme colour `#5b57e8`), 192/512 icons, service worker from `mystudy-pwa`. Install prompt, notification prompt and cookie banner are built in.

## 1. Tool / page inventory

55 `<section class="view">` blocks. Route titles are from `routeTitles` (line 11946); descriptions are the per-route `<title>`/meta descriptions in `<head>` (lines 98–~600).

| # | Route (`?p=`) | Tool | Purpose / key inputs → outputs | Storage | Free / Premium |
|---|---|---|---|---|---|
| 1 | `home` | Home dashboard | Greeting, license pill, countdown, stats, tool tiles, latest posts | `MST_APP_DATA`, `MST_VISIT_COUNT` | Free |
| 2 | `learn` | Learn Hub | Entry to Past Questions / Syllabus / Keypoints / Tutorials (see §3) | — (navigation only) | Free |
| 3 | `learn-years` | Choose Year | Year tiles 2026–2020 (rendered unconditionally; see §3) | — | Free |
| 4 | `learn-subjects` | Choose Subject | Subject tiles (18 subjects, §3) | — | Free |
| 5 | `examlevel` | Choose Exam Level | JAMB / WAEC / NECO / Post-UTME / Primary chooser | — | Free |
| 6 | `examboard` | Choose Exam Board | WAEC or NECO chooser for O-Level content | — | Free |
| 7 | `cbt` | CBT Practice | Timed mocks — see §2 | `MST_CBT_RESUME`, `MST_APP_DATA.cbtHistory`, cached question JSON `MSE_<EXAM>_<file>_<year>` | **Gated: 5 Qs/subject free, 40 premium** |
| 8 | `english` | English Quiz | 9 categories, timed quiz — see §5 | `MST_EQ_HIST`, `MST_EQ_RESUME`, session cache `MST_EQ_CACHE_<id>` | **Gated: 5 Qs / 10 min free, 40 Qs / 40 min premium** |
| 9 | `stats` | Performance Stats | CBT, English Quiz, Vocabulary, Keypoint history; averages, best, mastery bars, trend chart (Chart.js) | Reads the history keys above + `MST_TB_HIST`, `MST_VOCAB_HIST` | Free (shows a freemium notice when not premium) |
| 10 | `flashcards` | Flashcards (Leitner 3-box) | Spaced-repetition deck builder; cards you struggle with return more often | `MST_APP_DATA` (flashcard state lives in the app blob; no dedicated key found) | Free |
| 11 | `cgpa` | CGPA Calculator | 4.0/5.0 scales; course title/code/units/grade rows; semester GPA + cumulative CGPA; class of degree; printable transcript | `MST_APP_DATA.cgpa` (scale, semesters, draft) | Free |
| 12 | `predictor` | Graduation Target Predictor | Target class + semesters left → exact GPA required each semester | — (computed) | Free |
| 13 | `gpaclass` | GPA → Class of Degree | Converts a GPA to its class on the chosen scale | — | Free |
| 14 | `examplanner` | Exam Planner | Upcoming exams with live countdowns, reminder alarms, study targets | `MST_APP_DATA.exams` | Free |
| 15 | `lecture` | Lecture Schedule | Weekly lecture timetable with classroom-style reminders | `MST_APP_DATA.lectures` | Free |
| 16 | `study` | Study Planner (Pomodoro + Feynman) | Pomodoro focus timer; Feynman-style note revision | `MST_APP_DATA.studySessions`, `feynman` | Free |
| 17 | `timetable` | Class Timetable | Weekly class timetable builder, printable/shareable | (in app blob) | Free |
| 18 | `revision` | Revision Timetable Generator | Generates a revision timetable | (in app blob) | Free |
| 19 | `deadline` | Deadline Planner | Deadline tracking/planning | (in app blob) | Free |
| 20 | `outline` | Note Outline Builder | Builds structured note outlines | (in app blob) | Free |
| 21 | `budget` | Budget Tracker | Monthly ₦ limit + expense log | `MST_APP_DATA.budget` {limit, expenses} | Free |
| 22 | `streak` | Study Streak & XP | Daily study streak + XP for consistency | `MST_APP_DATA.streak`, `MST_TB_STREAK`, `MST_VOCAB_STREAK` | Free |
| 23 | `admission` | Admission Toolkit | JAMB + Post-UTME command centre (combos + aggregate) | — | Free |
| 24 | `admission-combo` | UTME Subjects & O-Level Checker | Course → 3 UTME subjects (English auto-added as 4th) + 5 O-Level core subjects; 8 faculties, 78 courses (see §5) | — | Free |
| 25 | `admission-agg` | Post-UTME Aggregate Predictor | JAMB (0–400) + O-Level grades + per-university formula → aggregate; JAMB/8 = /50 component | — | Free |
| 26 | `word` | Word Office | Browser A4 editor (TinyMCE); templates: blank, resume, report, letter, research paper; DOCX/PDF export | `MST_APP_DATA.word` {docs, activeId} | Free |
| 27 | `pdf` | PDF Toolkit | Merge, split, compress, reorder, page numbers, watermark, image-to-PDF, PDF-to-image, OCR, E-Sign (draw signature → transparent PNG), organise | — (files in memory; docs via app blob) | Free |
| 28 | `image` | Image Toolkit | Compress (KB), resize, convert, batch, watermark, EXIF stripper, QR generator | — | Free |
| 29 | `wordcount` | Word & Character Counter | Counts words/characters in pasted text | — | Free |
| 30 | `citation` | Citation Generator | Full references; styles include APA, MLA, Harvard, Chicago, IEEE, Vancouver (66 hits for the style names) | — | Free |
| 31 | `quickcite` | Quick Cite | Inline citations | — | Free |
| 32 | `summarizer` | Note Summarizer | Paste notes → short/medium/long bullet summaries, offline | — | Free |
| 33 | `textcompare` | Text Compare | Side-by-side text comparison/diff | — | Free |
| 34 | `textbook` | Keypoints (Topic view) | Topic reader: modules + 10-question test — see §3 | `mst.textbook.v1`, `MST_TB_HIST` | Free |
| 35 | `vocabulary` | Vocabulary | Word learning with streaks; 30-question test (`TEST_LEN = 30`, line 11160) | `MST_VOCAB_HIST`, `MST_VOCAB_LAST_DAY`, `MST_VOCAB_LEARNED`, `MST_VOCAB_STREAK`, `mst.vocab.v1` | Free |
| 36 | `dictionary` | Dictionary | Word lookup from `mystudy-dic` data files (`<letter>.json` via jsDelivr) | — | Free |
| 37 | `constitution` | Nigerian Constitution (1999) | Full text — 8 chapters, 7 schedules; searchable, chapter TOC with filter, sticky sidebar | Fetched from `nigeria-constitution@main` (`manifest.json`) | Free |
| 38 | `blog` | Blog | Post grid/list, search (redirects to Blogger native search), bookmarking | `mst_bookmarks` | Free |
| 39 | `label` | Browse (label) | Blogger label listing page | — | Free |
| 40 | `post` | Article | Single-post reader — see §4 | — | Free |
| 41 | `bookmarks` | My Bookmarks | Saved posts/pages | `mst_bookmarks` | Free |
| 42 | `profile` | Profile & Settings | Name, institution, course, theme, accent, skin, license, backup/restore, wipe — see §5/§7 | `MST_APP_DATA.profile` | Free |
| 43 | `about` | About Us | "All-in-one academic suite for Nigerian students"; local-first storage; email + WhatsApp support | — | Free |
| 44 | `contact` | Contact Us | Blogger native ContactForm widget, polished UX | — | Free |
| 45 | `howto` | How To Use | Usage guide + stats | — | Free |
| 46 | `convert` | Unit Converter | Length, mass, temperature, area, volume, time | — | Free |
| 47 | `chart` | Chart Generator | Data table → Bar, Line, Pie, Doughnut, Radar; export transparent PNG/JPG/PDF/CSV or embed snippet | — | Free |
| 48 | `error` | 404 — Page Not Found | Error page (also carries the only footer text seen) | — | Free |

Category hub views (no separate tool logic): `cat-practice` (Practice & Assessment), `cat-academics` (Academics & Planning), `cat-documents` (Documents & Creation), `cat-admission` (Admission & Life), `cat-smart` (Smart Helpers), `cat-study` (Study & Productivity), `cat-legal` (Legal & Civic Library), `cat-read` (Blog & Reading).

**Premium gating — the whole picture.** Only CBT and English Quiz are gated. `MST_isPremium()` (line 4515) is true only when `profile.license === 'premium'`; its only other use is the verified badge. There is no per-tool paywall anywhere else in the file.

**Assistant (no route).** Floating "Study Assistant" chatbot: tries `POST https://bot.mystudysuite.workers.dev/chat/json` (message + last 12 history + deviceId + name, 20 s timeout), falls back to a local rule-based answerer (`localAnswer`) that explains tools, CBT activation and the Device ID. History in `msa_chat_v4` (last 60 messages). Hidden on CBT/quiz/Word views.

## 2. CBT — full detail

**Source of questions.** `CBT_REPO_BASE = 'https://cdn.jsdelivr.net/gh/ola1de/Exam-Questions-Data@main/json/'` (line 12959). Files are fetched per subject/year, e.g. `<EXAM>_<file>_<year>.json`, and cached in localStorage (`MSE_<EXAM>_<file>_<year>`). No question content is in the template itself.

**Exam types (setup `<select id="cbt-mode">`, lines 6791–6797).** JAMB (UTME), WAEC, NECO, Post-UTME, Primary School (Common Entrance).

**Subjects — secondary pool (`CBT_DB.sec`, lines 12964–12986), 21 subjects:** English Language, Mathematics, Biology, Physics, Chemistry, Literature-in-English, Government, Economics, Commerce, Financial Accounting, Agricultural Science, Geography, C.R.S, I.R.S, Civic Education, History, Computer Studies, Further Mathematics, Yoruba, Hausa, Igbo.
**Primary pool (`CBT_DB.pri`, lines 12987–12999), 11 subjects:** English Language, Mathematics, Basic Science & Tech, Social Studies, Vocational Aptitude, Quantitative Reasoning, Verbal Reasoning, Civic Education, Agricultural Science, Current Affairs, Computer Studies.
**Selection limits (lines 13116–13127):** JAMB max 4 subjects, Primary max 6, WAEC/NECO/Post-UTME max 9. English is **not** forced compulsory in the CBT picker (unlike the combo checker, §5).

**Years.** Year dropdown is populated current year down to 2010 (line 13074); the fetcher tries the chosen year first, then falls back through 2025–2015 in order (lines 13154–13155). Primary files have no year suffix (`PRI_<file>_2026.json` → `_2025.json` → `.json`).

**Timing.** Duration is a user-editable number input, default 60 min, minimum 5 (line 6803). The template does **not** enforce JAMB's real format (120 min / 180 questions): maximum is 4 subjects × 40 = 160 questions. Timer counts down `MM:SS`, auto-submits at 00:00 (`tick()`, line 13794).

**Question count — free vs premium.** Hard-coded in `processQuestions` (lines 13206–13208): free = 5 questions per subject, premium = 40. The setup form also shows a "Questions per subject" input (`#cbt-count`, value 40, min 5, line 6806) but **no JavaScript reads it** — it is decorative. The setup copy says "Freemium: 5 Qs per subject. Activate Premium for the full 40." (line 6824); in-exam badge shows `MODE · DEMO` when free (line 13232).

**Question format.** Normalised to `{q, o[], a, passage, passageType, exp}` (lines 13184–13205). Options A–D (answer may be a number, a letter, or the full option text). Passage/poem items are flattened so the passage stays grouped with its questions; top-level items are shuffled. KaTeX renders maths (`$…$`, `$$…$$`, `\begin{…}`).

**Runtime UX.** Subject tabs, per-subject question navigator grid (current subject only), Prev/Next, Flag, keyboard shortcuts (A–D answer, N/→ next, P/← previous, S submit, R close pop-up), passage panel beside the question when present, on-screen calculator button shown only for calculation subjects (`_updateCalcVisibility`, lines 13783–13790; allowed list includes Mathematics, Physics, Financial Accounting/Accounting, Commerce, Further Mathematics, Chemistry, Economics). Setup copy claims "JAMB → Basic calc. WAEC/NECO → Scientific calc." — two separate calculator implementations were **not** traced in this inventory; only one toggle (`CBT.toggleCalc()`, line 13869) was found.

**Scoring.** 1 mark per correct answer, no negative marking, unanswered = 0. Result shows `%`, `score / total`, and a per-subject breakdown bar. History is appended to `MST_APP_DATA.cbtHistory` (`{date, mode, subjects, score, total, pct, perSubj, duration}`).

**Corrections / explanations.** "View Corrections" re-opens the exam in review mode: answers locked, correct option highlighted green, your wrong answer struck through in red, and an Explanation card appears **only if the question JSON carries an `exp`/`explanation` field** (lines 13744–13753). No explanation is generated by the template.

**Resume.** In-progress exams auto-save to `MST_CBT_RESUME` on every answer/navigation; "Resume Last Session" restores state (including flags) if the saved exam has not expired (`_loadSaved` rejects sessions whose `end` has passed). English Quiz has its own resume key (`MST_EQ_RESUME`).

**Anti-cheat / AI Proctor (optional, off by default).** A checkbox on setup (`#cbt-ai-toggle`, persisted as `settings.aiProctor`). When on: requests fullscreen, blocks right-click and copy/paste/devtools shortcuts (F12, Ctrl+C/V/X/U/P/S, Ctrl+Shift+I/J/C), strikes on tab/window switch, window blur, fullscreen exit; webcam + microphone via `getUserMedia` (640×480, 15–20 fps) with FaceDetector if available, otherwise a skin-tone + motion fallback; speech-band noise analysis (250 Hz–3.8 kHz) with adaptive room-floor calibration; no-face, multi-person, off-centre/too-far, camera-covered and dark-room detection. **3 strikes = auto-submit** (`_aiMaxViolations = 3`, `_aiStrike`, lines 13615–13633). Grace period ~6 s at start. If camera/mic permission is denied, tab/keyboard monitoring continues. Separately, while any CBT view is active the sidebar/topbar are hidden by an exam-lock (`cbtRoute()` / `exam-lock`, lines 24383+), whether or not the proctor is on.

**Licensing / premium flow — the exact mechanism.**

| Step | What the file does |
|---|---|
| Device ID | `CBT_deviceFingerprint()` / `devId()` (lines 13002–13013, 11870–11883): hash of userAgent + language + screen colour depth + screen size + timezone offset → `Mxxx-xxxx` (mobile) or `Dxxx-xxxx` (desktop), stored in localStorage `_sys_dev_id`. Fallback `D000-0000`. |
| Payment (as written in the template) | Modal (lines 11894–11912): transfer **₦2,000** to **Access Bank 1892737645, Omotoso Omotayo Olawande**, then "Send Receipt on WhatsApp" (`wa.me/2348100259673`, prefilled text includes the Device ID). |
| Activation | User pastes the key sent back on WhatsApp into the modal; the template `POST`s `https://mystudy-licensing.mystudysuite.workers.dev/check` with `{deviceId, activationCode}` (lines 11920, 13919). On `{success: true}` it calls `markFull()`. |
| Local unlock | `markFull()` / `CBT_activateFull()` write `localStorage._sys_core_auth_v2 = reverse(btoa(deviceId + '_LOCAL_LIC_V1'))` and set `profile.license = 'premium'` (lines 11884–11890, 13029–13033). `CBT_isFull()` (lines 13015–13028) accepts either that stored value **or** `profile.license === 'premium'`, and self-heals the stored key from the profile flag. |
| Admin key generation | Saving a profile whose **name + institution** match admin credentials triggers `POST …/auth {username: name, password: institution}` (lines 16611, 16956). On success the Worker returns HTML that injects admin controls; the Activation Generator then `POST`s `…/make {username, password, deviceId}` and displays the returned `key` (lines 16933–16939). |
| Backup safety | Backup export scrubs all licence fields (`license`, `activationKey`, `premium`, `tier`, … — `BK_LICENSE_FIELDS`, lines 16645–16646) and never exports `_sys_core_auth_v2` / `_sys_dev_id`, so Premium cannot travel in a shared backup file. |

**Bypass-relevant facts (for the rebuild, not a how-to):** the premium check is entirely client-side — the expected local value is a reversible transform of the Device ID, and the profile flag alone is enough for `CBT_isFull()` to re-issue it. The Worker `/check` is the only server-side gate in the current design, and it is only consulted at activation time, not per exam. The user's rebuild brief ("No cheating, no bypass", server-verified Paystack) directly addresses this.

## 3. Learn Hub

**Categories (`LEARN_CATS`, lines 12392–12402).** Past Questions (`pastq`, split JAMB `past-jamb` / O-Level `past-olevel` with board picker), Syllabus (`syllabus-jamb` / `syllabus-olevel`, no year), Keypoints (`textbooks-jamb` / `textbooks-olevel`, no year), Tutorials (`tutorial`, no year).

**Years.** `LEARN_YEARS = ['2026','2025','2024','2023','2022','2021','2020']` (line 12381).

**Subjects (Learn Hub, 18).** Mathematics, English, Physics, Chemistry, Biology, Economics, Government, Literature, Geography, Commerce, Accounting, Agric, CRS, IRS, Civic, History, Computer, Further Math (lines 12382–12391). Note: Yoruba, Hausa and Igbo exist in CBT but **not** in Learn Hub.

**How content loads — and why pages can be empty.** Feed-based discovery was removed (comments at lines 12460–12463, 12513–12517). Year and subject tiles are rendered for **all** supported years/subjects unconditionally; clicking one goes to Blogger's native `/search/label/{prefix}-{year}` (or subject) page. If no Blogger post carries that label, the page shows "No posts found for this label yet." That is the mechanism behind the empty 2024/2025 JAMB Past Questions pages found on the live site. Past Questions, Syllabus and Tutorials therefore depend entirely on Blogger posts with the right labels; the template contains no past-question or syllabus text itself.

**Keypoints / Textbooks (the one Learn Hub area with real in-template structure).**
- Registry `SUBJECTS` (lines 10351–10370): 18 subjects with `file_prefix`, `folder`, `available`. Available = true (12): Mathematics, English, Physics, Chemistry, Biology, Economics, Government, Literature, Geography, Commerce, Accounting, Agric. Available = false (6): **CRS, IRS, Civic, History, Computer, Further Math** — these have no topics at all (see below).
- Topic registry `TOPICS` (lines 10373–10635): **165 topics across 12 subjects, each split SSS 1 / SSS 2 / SSS 3** — full list in Appendix A.
- Topic content is **not** in the template. Each topic loads `{BASE}/{folder}/{file_prefix}-{level}-{slug}.json` from `BASE = 'https://cdn.jsdelivr.net/gh/ola1de/mystudy-textbooks'` (lines ~10345, 10808). Each JSON must contain `modules[]` (each `{title, html}`) and a `quiz[]` pool; malformed data throws. The reader shows one module at a time with prev/next, a progress bar, "mark module done", KaTeX rendering, and a **10-question test** (`TEST_LEN = 10`) drawn from the quiz pool, with score, time and per-topic progress (`modulesDone`, `bestScore`, `avgScore`, `tests`) persisted in `mst.textbook.v1` and history in `MST_TB_HIST` (+ streak keys `MST_TB_STREAK` / `MST_TB_LAST_DAY`).
- **Missing by construction:** no JSS 1–3 topics (registry is SSS only); no topics for CRS, IRS, Civic, History, Computer, Further Math; no English/Physics/etc. topics beyond the 165 listed. Whether every one of the 165 JSON files actually exists in the `mystudy-textbooks` repo was **not** checked (repo not in scope) — the registry is a promise, not proof.

**Tutorials.** A `tutorial` category exists in `LEARN_CATS` with `noYear: true`; no tutorial content or topic list is embedded in the template — tutorials are Blogger posts by label, like Past Questions.

**Vocabulary / Dictionary (adjacent to Learn Hub).** Vocabulary loads word data from `vocabulary-database` (jsDelivr + raw.githubusercontent fallback), tracks learned words and streaks, 30-question test. Dictionary looks up `<letter>.json` from `mystudy-dic@main/data/`.

## 4. News / Blog post format — the format the user loves

Posts are Blogger posts rendered by the real Blog1 widget, then re-rendered by the theme. Two render paths exist:

1. **Shell/app path** (`inject()`, lines 3805–3953): used when the app shell is active. Header = eyebrow (first label) + title + meta + action buttons; then featured image; then TOC; then body; then tags; then share bar; then comments.
2. **Native path** (`<div class="native-blog-wrap">`, lines 3956+): a self-contained reader, max-width 880 px, card with 18 px radius, used when the shell is unavailable. Same content order.

**Exact post structure (native path, lines 3956–3980+).**

- Eyebrow: first label as an uppercase, letter-spaced pill linking to `/search/label/<label>`.
- Title: `<h1 class="single-post-title entry-title">`, Fraunces serif, 2.3 rem, weight 600.
- Meta row: author (Blogger `post.author.name` — falls back to blank, which is why live posts show "Unknown"), published date, read time, comment count linking to `#comments`. Read time = words ÷ 220, minimum 1 min (line 3848).
- Action row: Bookmark button, Tweet (X), Facebook, WhatsApp share links.
- Featured image: the **first image in the post body is extracted** and moved into `<figure class="featured-image">` above the body (lines 3770–3786; if the post has no image, the feed thumbnail is used, upscaled to `/s1600/`). Displayed full-width, max-height 520 px, `object-fit: cover`, 16 px radius.
- Body: `<div class="post-body entry-content">` with the post HTML. Typography (lines 4313–4401): Inter 1.05 rem, line-height 1.78; H2 Fraunces 1.7 rem, H3 Plus Jakarta Sans 1.3 rem; links primary-coloured with underline; `pre`/`code` JetBrains Mono on dark `#0e1116`; images max-width 100%, 12 px radius; blockquotes with a 3 px primary left border on a soft background, and in the richer rules a large opening quote mark; bullet lists use a 7 px primary dot (no default disc); ordered lists use numbered primary circles; tables have a soft header row; `hr` is dashed.
- Tags: `.post-labels` / `.post-tag` pills (primary-tinted, 99 px radius) linking to label pages.
- Share bar (bottom): "Share this post" + X / Facebook / WhatsApp / copy-link buttons.
- Comments: header "Discussion" with count and the note that a comment appears after a quick moderation check; Blogger's native `#comments` node is relocated into the reader when available, otherwise a Blogger comment iframe (`blogger.com/comment-iframe.g?blogID=5334759134063131007&postID=…`).
- Extras the theme adds: YouTube embeds are wrapped in a 16:9 responsive `.yt-embed`; `[text|url]` shorthand in post HTML becomes a "magic button" link and `[DOWNLOAD]` becomes a Download button (`Learn.transform`, lines 12696–12701); videos are extracted by `Learn.extractVideo`.

**Table of Contents — two implementations, same look.**

- **Shell path** (`enrichContent`, lines 3788–3802, 3842–3845): scans `h2, h3` in the post body, slugifies each heading (lowercase, non-alphanumerics stripped, spaces → `-`, max 60 chars, `-2`, `-3`… for duplicates), sets it as the heading `id`, adds class `anchor-heading` (scroll-margin 80 px). The TOC is emitted **only if there are ≥ 3 headings**, as `<details class="post-toc" open>` with an `<ol class="toc-list">`; H3 items get class `toc-l3` (indented, circle marker). It is inserted after the featured image, else at the top. On `/p/` pages any baked-in TOC is stripped instead.
- **Learn Hub path** (`Learn.injectTOC`, lines 12702–12739): scans `h2, h3, h4`; needs **≥ 2 headings**; builds a **closed-by-default** `<details class="mst-toc">` whose summary reads "Table of Contents" plus a count badge ("N sections") and a chevron that rotates 180° when open; H3 links are indented 22 px, H4 38 px; clicking a link smooth-scrolls to the heading and updates the URL hash. Inserted after the first image (treated as the featured image), else at the top.
- TOC styling (lines 1792–1803, 4370–4379): bordered card, primary-tinted header, left accent border (4 px) in the native reader, hover state on links.

**SEO (per-post and per-route).** `<head>` carries a hand-written `<title>` + `description` + `og:title/description` + `twitter:title/description` for **every** route (lines 98–~600), `og:locale en_NG`, `twitter:card summary_large_image`, `og:url` from the canonical view URL, and a note that a duplicate canonical was deliberately removed because Blogger's `all-head-content` already outputs one. Post pages add `article:author` and JSON-LD (`@type` WebApplication/Article with author name). There is **no in-template post editor, no SEO fields per post, no category/tag picker and no image upload** — posts are authored in Blogger; category/tags are Blogger labels, and the theme only *reads* them.

**Short verbatim excerpts from the template (total under 50 words, as instructed):** the TOC summary reads "Table of Contents"; the comments subtitle reads "Share your thoughts — your comment appears after a quick moderation check."; the home greeting reads "Focus. Practice. Graduate stronger."

## 5. Other tools — detail

- **CGPA.** Scales 4.0 and 5.0 (grade sets A–F; 5.0 adds E). Grade points: 5.0 scale A=5…F=0; 4.0 scale A=4…F=0. Class thresholds — 5.0: ≥4.5 First Class, ≥3.5 Second Class Upper, ≥2.4 Second Class Lower, ≥1.5 Third Class, ≥1.0 Pass; 4.0: ≥3.5 First, ≥3.0 Upper, ≥2.0 Lower, ≥1.0 Pass (`classOf`, line 15984). Inputs: name, institution, course (with autocomplete from built-in Nigerian institution/course lists `NIG_INST` / `NIG_COURSES`, lines 15969–15970), semester name, per-course rows. Outputs: semester GPA, cumulative CGPA, class, printable transcript (generated in a hidden iframe, with watermark + logo). Draft auto-saves; semesters can be saved, edited, deleted.
- **English Quiz.** 9 categories from `https://cdn.jsdelivr.net/gh/ola1de/English-Quiz@main/` (line 18455): Language Skills, Grammar, Vocabulary, Reading Comprehension, Writing Skills, Listening Skills, Parts of Speech, Literature, General English Knowledge. Full: 40 questions, 40 min; demo/free: 5 questions, 10 min (`Q_COUNT`/`DUR_MIN`, lines 18467–18470). Same runtime as CBT (tabs, flag, navigator, resume, corrections with explanations when present). History capped at 100 attempts (`MST_EQ_HIST`).
- **Admission Toolkit.** Combo checker: 8 faculties, **78 courses**, each with 3 UTME subjects + 5 O-Level subjects (English + Maths usually compulsory) — `COURSES` (lines ~18959+). Aggregate predictor: JAMB/8 (out of 50) plus O-Level and Post-UTME components per university formula; validates JAMB 0–400.
- **Flashcards.** Leitner 3-box deck builder (create decks/cards, review, promote/demote boxes). No question bank is embedded; decks are user-created.
- **Planner / timetable / budget / streak.** Exam Planner: exam name/date countdowns + alarms + targets. Lecture Schedule + Class Timetable: weekly grids. Study Planner: Pomodoro timer + Feynman notes. Budget: monthly limit + expense entries in ₦. Streak & XP: daily check-in streak with XP; achievements on Profile (CGPA, visits `MST_VISIT_COUNT`, streak, quizzes taken).
- **Word Office.** TinyMCE A4 editor, templates (blank / resume / report / letter / research paper), DOCX + PDF export (html-docx-js, jsPDF, html2canvas), documents saved in `word.docs`.
- **PDF Toolkit.** Tabs found in the markup: merge, split, compress, reorder, page numbers (`pgnum`), watermark (`wm`), image-to-PDF (`img2pdf`), PDF-to-image (`pdf2img`), OCR, E-Sign (`sign`), organise. Uses pdf-lib, jsPDF, mammoth, Tesseract-style OCR references in copy.
- **Image Toolkit.** Tabs: compress, resize, convert, batch, watermark, EXIF stripper, QR generator.
- **Smart helpers.** Citation Generator (APA/MLA/Harvard/Chicago/IEEE/Vancouver), Quick Cite, Note Summarizer (short/medium/long, offline), Text Compare, Word & Character Counter, Chart Generator (Bar/Line/Pie/Doughnut/Radar, PNG/JPG/PDF/CSV export + embed snippet).
- **Constitution library.** Constitution (1999) from `nigeria-constitution@main`, chapter TOC with search filter, sticky sidebar; the "Legal & Civic Library" hub promises "Constitution, statutes & civic docs" but only the Constitution viewer is implemented in the template.
- **Profile (today).** Fields: name, institution, course, theme (light/dark), accent colour picker, skin (default + "Duolingo" skin), avatar = initials in an accent circle, achievements row, Device ID display + copy, license box, backup export/import (JSON of all `mst_`/`MST_` keys, licence fields scrubbed, device keys excluded), "Wipe all data" (deletes profile, CGPA, exams, lectures, documents, CBT history and the Premium activation on the device). **No photo upload, no bio, no email, no password, no social fields.** Saving a profile silently attempts the admin `/auth` check described in §2.
- **Home dashboard.** Greeting + date + license pill, countdown to next exam, stat cards, category tiles, "Latest on MyStudy" blog feed, install/notification prompts.

## 6. Design system

- **Name:** v15 "Quiet Confidence" — "Single source of truth for colour, type, space, radius, elevation and motion" (lines 721–726).
- **Colours (light, `:root` lines 727–818):** primary `#5b57e8` (hover `#4a45d9`, dark `#3d38bd`, light `rgba(91,87,232,0.10)`), brand-2 `#0b95e0`, accent (gold) `#f0a020`, secondary (teal) `#0f8073`, success `#0f9d6e`, danger `#e2504f`, warning `#f0a020`, info `#0b84d6`; surfaces bg-body `#fbfbfd`, bg-card `#ffffff`, bg-secondary `#f4f5f8`; ink text-primary `#0e1116`, text-sub `#4c5462`, text-muted `#8b93a3`; border `#e6e8ef`; glass `rgba(255,255,255,0.78)`; theme-color meta `#5b57e8`.
- **Dark theme** (`[data-theme="dark"]`, lines 820–~870): "neutral graphite, not navy" — bg-body `#0c0d11`, bg-card `#15171d`, text-primary `#e9ebef`, primary lightens to `#8b87ff`, accent `#f7b84b`. Toggled from Profile (`profile.theme` light/dark).
- **Fonts:** Inter (body), Plus Jakarta Sans (display/headings), JetBrains Mono (code/Device ID) via Google Fonts (line 664); Fraunces (Georgia serif) is used for post titles/H2 in the native reader (lines 4310–4315) — loaded where? Fraunces is referenced in CSS but does **not** appear in the Google Fonts links in `<head>` (only Inter, Plus Jakarta Sans, JetBrains Mono, Nunito, Baloo 2 are linked), so it falls back to Georgia. Nunito + Baloo 2 power the Duolingo skin.
- **Type scale:** `--fs-xs 0.75rem` → `--fs-3xl clamp(1.85rem, 1.15rem + 3vw, 2.7rem)`; headings use `--font-display`, letter-spacing −0.02 em.
- **Radius:** 8 / 12 / 16 / 22 px + 999 px pill. **Space:** 8 pt rhythm (4–56 px). **Motion:** 180 ms, `cubic-bezier(0.32,0.72,0,1)`, spring variant for emphasis. **Shadows:** near-invisible at rest (`--shadow`), lifting on intent.
- **Layout:** sidebar `--v3-sidebar: 248px` (210–222 px in some overrides), content full-width; cards 16 px radius with 1 px border; tool tiles, glass panels, pill badges; mobile breakpoints collapse the sidebar and stack grids.
- **Skins:** default skin + a "Duolingo" skin (`html[data-skin="duolingo"]`, selectable in Profile as `mst_skin`): primary becomes Duolingo green `#58CC02`, display font switches to Nunito/Baloo 2, chunkier shadows, yellow `#FFC800` premium tier. No other skins are defined.
- **Accent picker:** Profile offers preset accent colours; `applyAccent()` rewrites the primary tokens at runtime.

## 7. Top gaps (evidence-based — what the file does not contain)

1. **No accounts / auth at all.** No registration, login, password, Google sign-in, QR, security questions, roles, or per-user data. Profile is three text fields in localStorage. The only "admin" is the `/auth` name+institution check (§2).
2. **No payments.** Paystack: 0 hits. Premium is a manual ₦2,000 bank transfer + WhatsApp key. No webhook, no verification on payment, no subscription/expiry.
3. **Premium enforcement is client-side and reversible** (§2, last row). A server-verified entitlement is the single biggest rebuild requirement.
4. **Learn Hub is a shell over Blogger labels.** Past Questions / Syllabus / Tutorials have no embedded content; year+subject tiles render even when nothing exists behind them. Keypoints exist only as a 165-topic registry pointing at external JSON files (existence not verified here).
5. **Missing subjects/topics.** Keypoints: CRS, IRS, Civic, History, Computer, Further Math have `available: false` and zero topics; no JSS topics; no Yoruba/Hausa/Igbo in Learn Hub (CBT only). CBT has no CRS/IRS/Civic/History/Computer/Further-Math question files referenced beyond the subject list — and no question file at all is inside the template.
6. **Blog has no editor, no SEO fields, no admin posting.** Posts are Blogger posts; the theme only reads labels/author/date. No category/tag management UI, no image upload, no draft/schedule, no "News" concept (it is a general Blog).
7. **Dead/broken references in the template itself:** the `#cbt-count` input is never read; Fraunces is used in post CSS but never loaded; the setup copy promises a "Scientific calc" for WAEC/NECO but only one calculator toggle was traced; Privacy/Terms pages are linked from the 404 page but no such routes exist in the template (`/p/privacy.html`, `/p/terms.html` — not in the `/p/` list, §0).
8. **No offline question bank.** Every CBT/Quiz/Keypoints/Dictionary/Constitution payload is fetched from jsDelivr/GitHub at runtime and cached in localStorage/sessionStorage; first use needs internet despite the "offline-ready" copy.
9. **No moderation, reporting, or user-generated content controls** beyond Blogger comments (with a moderation note in copy only).
10. **Profile is not customisable** beyond name/institution/course/theme/accent/skin — no avatar photo, bio, email, school level, exam target, or notification preferences (only a boolean `settings.notifications`).

## Appendix A — Keypoints topic registry (165 topics, verbatim titles)

Extracted from `TOPICS` (lines 10373–10635). Format: subject → level → topics (`slug` — title).

### Accounting

**SSS 1** (2):
- `intro-principles` — Introductory Principles of Accounting (History, users, concepts, and the fundamental accounting equation)
- `bookkeeping-records` — Bookkeeping Records and Trial Balance (Double-entry, journals, cash books, and trial balance preparation)

**SSS 2** (3):
- `final-accounts-sole-trader` — Final Accounts of a Sole Trader (Trading, Profit &amp; Loss Account, Balance Sheet, and adjustments)
- `reconciliations-control-accounts` — Reconciliations and Control Accounts (Bank reconciliation, control accounts, error correction, and suspense accounts)
- `special-accounts` — Special Accounts (Single entry, incomplete records, and non-profit organization accounts)

**SSS 3** (3):
- `partnership-company-accounts` — Partnership and Company Accounts (Partnership appropriation, goodwill, admission, company shares, and debentures)
- `industrial-organizational-accounts` — Industrial and Organizational Accounts (Departmental, branch, manufacturing, and consignment accounts)
- `government-accounting` — Government Accounting (Public sector revenue sources, capital/recurrent funds, and private comparisons)


### Commerce

**SSS 1** (3):
- `intro-occupation` — Introduction and Occupation (Meaning of commerce, division of occupations, production, and utility)
- `home-trade` — Home Trade (Retail, wholesale, middlemen, and trade documents)
- `business-formation-protection` — Business Formation &amp; Protection (Sole proprietorship, partnership, and consumer protection agencies)

**SSS 2** (3):
- `business-ownership-bodies` — Business Ownership and Trade Bodies (Limited liability companies, public corporations, cooperatives, and trade associations)
- `international-trade` — International Trade (Differences from home trade, balance of payments, and shipping documents)
- `ancillaries-to-trade` — Ancillaries to Trade (Transportation, communication, warehousing, and advertising)

**SSS 3** (3):
- `insurance` — Insurance (Insurance principles, types of policies, and reassurance)
- `financial-system` — The Financial System (Banking systems, Central Bank of Nigeria, and the stock exchange)
- `business-administration` — Business Administration and Legal Aspects (Capital structures, business management, and trade laws)


### Mathematics

**SSS 1** (8):
- `number-bases` — Number Bases (Bases, conversions, arithmetic)
- `modular-arithmetic` — Modular Arithmetic (Working modulo n)
- `indices` — Indices (Laws &amp; exponential equations)
- `logarithms` — Logarithms (Tables, characteristic, mantissa)
- `sets` — Sets (Venn diagrams &amp; word problems)
- `algebraic-processes` — Algebraic Processes (Expansion, factorisation, equations)
- `plane-geometry` — Plane Geometry &amp; Mensuration (Angles, area, sectors)
- `statistics` — Statistics (Data, charts, frequency tables)

**SSS 2** (6):
- `logarithms-2` — Logarithms (Part II) (Logs of numbers &lt; 1)
- `algebraic-processes-2` — Algebraic Processes (Part II) (Simultaneous &amp; quadratic equations)
- `circle-theorems` — Circle Theorems (Angles, cyclic quads, tangents)
- `mensuration-solids` — Mensuration of Solids (Volume &amp; surface area)
- `trigonometry` — Trigonometry (Ratios, elevation, bearings)
- `statistics-2` — Statistics (Part II) (Dispersion, ogive, quartiles)

**SSS 3** (6):
- `surds` — Surds (Simplification &amp; rationalisation)
- `sequences-series` — Sequences and Series (AP, GP, sum to infinity)
- `matrices` — Matrices &amp; Determinants (Operations, inverse, Cramer)
- `coordinate-geometry` — Coordinate Geometry (Distance, gradient, line eqn)
- `calculus` — Introductory Calculus (Differentiation &amp; integration)
- `probability` — Probability (Sample space, laws, trees)


### English

**SSS 1** (5):
- `grammar-structure` — Grammar and Structure (Nouns, pronouns, verbs, adjectives, punctuation)
- `vocabulary-development` — Vocabulary Development (Synonyms, antonyms, registers (Agriculture, Sports, Law))
- `comprehension-summary` — Comprehension & Summary (Skimming, scanning, topic sentences)
- `continuous-writing` — Continuous Writing (Narrative, descriptive essays, informal letters)
- `oral-english` — Oral English (Vowels, consonants, word stress)

**SSS 2** (5):
- `grammar-structure` — Grammar and Structure (Phrases, clauses, concord, tenses, adverbs)
- `vocabulary-development` — Vocabulary Development (Homophones, idioms, registers (Medicine, Science, ICT))
- `comprehension-summary` — Comprehension & Summary (Figures of speech, inference, argumentative summaries)
- `continuous-writing` — Continuous Writing (Argumentative, expository, formal letters)
- `oral-english` — Oral English (Diphthongs, clusters, intonation)

**SSS 3** (5):
- `grammar-structure` — Grammar and Structure (Reported speech, complex concord, syntax)
- `vocabulary-development` — Vocabulary Development (Advanced idioms, proverbs, registers (Aviation, Maritime, Banking))
- `comprehension-summary` — Comprehension & Summary (Past-paper practice, word-limit summaries)
- `continuous-writing` — Continuous Writing (Articles, speeches, reports, minutes, business letters)
- `oral-english` — Oral English (Stress shift, transcription, rhyme, exam practice)


### Physics

**SSS 1** (4):
- `introduction-measurement` — Introduction & Measurement (Quantities, units, dimensional analysis, errors)
- `kinematics` — Kinematics (Scalars, vectors, motion graphs, equations of motion)
- `dynamics` — Dynamics (Newton\)
- `properties-of-matter` — Properties of Matter (Kinetic theory, pressure, elasticity, Hooke\)

**SSS 2** (3):
- `heat-energy` — Heat Energy (Thermometers, expansivity, gas laws, latent heat)
- `waves` — Waves (Transverse, longitudinal, sound, wave properties)
- `optics` — Optics (Reflection, refraction, lenses, optical instruments)

**SSS 3** (3):
- `electricity-magnetism` — Electricity &amp; Magnetism (Electrostatics, Ohm\)
- `ac-circuits` — AC Circuits (RMS, reactance, impedance, resonance)
- `modern-physics` — Modern Physics (Atomic models, radioactivity, semiconductors)


### Chemistry

**SSS 1** (4):
- `introduction-matter` — Introduction &amp; Matter (Scientific method, safety, states of matter, separation techniques)
- `atomic-structure` — Atomic Structure (Dalton, sub-atomic particles, isotopes, orbitals, periodic table)
- `chemical-bonding` — Chemical Bonding (Ionic, covalent, dative, metallic and intermolecular forces)
- `stoichiometry-gas-laws` — Stoichiometry &amp; Gas Laws (Mole concept, formulae, Boyle, Charles, Graham, ideal gas)

**SSS 2** (4):
- `acids-bases-salts` — Acids, Bases and Salts (Arrhenius, Br\u00f8nsted, Lewis, pH, titration, salts)
- `water-solubility` — Water and Solubility (Water treatment, hardness, solutions, solubility curves)
- `physical-chemistry` — Physical Chemistry (Rates, equilibrium, energetics, redox, electrochemistry)
- `non-metals-part-1` — Non-Metals and their Compounds I (Non-metal properties, carbon allotropes, oxides, trioxocarbonates)

**SSS 3** (4):
- `non-metals-part-2` — Non-Metals and their Compounds II (Nitrogen, ammonia, sulphur, Contact process, halogens)
- `metals-compounds` — Metals and their Compounds (Activity series, extraction of Al, Fe, Cu, Sn, alloys, corrosion)
- `organic-chemistry` — Organic Chemistry (Hydrocarbons, alkanols, acids, esters, soaps, polymers)
- `environmental-chemistry` — Environmental Chemistry (Air and water pollution, global warming, waste management)


### Biology

**SSS 1** (5):
- `concept-classification` — Concept and Classification of Living Things (Characteristics of life, binomial nomenclature &amp; five kingdoms)
- `cell-structure-biophysics` — Cell Structure and Biophysics (Cell theory, organelles, diffusion, osmosis &amp; active transport)
- `nutrition-digestion` — Cellular Nutrition and Digestion (Photosynthesis, heterotrophs, mineral nutrition &amp; digestive systems)
- `respiration-excretion` — Respiration and Excretion (Glycolysis, Krebs cycle, surfaces, products &amp; organs)
- `basic-ecology` — Basic Ecology (Biomes, biotic/abiotic factors, food chains &amp; energy flow)

**SSS 2** (4):
- `transport-support` — Transport and Support Systems (Transpiration, blood, skeletal systems &amp; muscles)
- `coordination-control` — Coordination and Control (Nervous &amp; endocrine systems, hormones &amp; sensory organs)
- `reproduction` — Reproduction (Mitosis, meiosis, plant/animal reproduction &amp; family planning)
- `ecology-part2` — Ecology (Part II) (Nutrient cycles, succession, populations &amp; conservation)

**SSS 3** (4):
- `genetics` — Genetics (Chromosomes, DNA/RNA, protein synthesis &amp; Mendelian laws)
- `variation` — Variation (Continuous/discontinuous variation, mutations &amp; forensics)
- `evolution-adaptation` — Evolution and Adaptation (Theories of evolution, fossils &amp; structural adaptations)
- `public-health` — Public Health (Disease vectors, waste disposal, pathogens &amp; immunization)


### Economics

**SSS 1** (4):
- `intro-to-economics` — Introduction to Economics (Definitions, methodology, scarcity, choice, and opportunity cost)
- `production-business` — Production and Business (Factors of production, division of labor &amp; business units)
- `market-forces` — Market Forces (Theory of demand and supply, equilibrium, and price controls)
- `systems-population` — Economic Systems and Population (Economic frameworks, demographic transition, and population structure)

**SSS 2** (4):
- `elasticity-utility` — Elasticity and Utility (Elasticity measurements, utility concepts, and consumer equilibrium)
- `cost-revenue-markets` — Cost, Revenue, and Markets (Cost curves, revenue curves, and market structures)
- `sectoral-studies` — Sectoral Studies (Distributive trade, agriculture, industrialization &amp; policies)
- `national-income` — National Income (GDP, GNP, measurement methods, double counting &amp; limitations)

**SSS 3** (4):
- `money-financial-institutions` — Money and Financial Institutions (Barter, functions of money, commercial and central banking)
- `public-finance-inflation` — Public Finance and Inflation (Taxation systems, budgets, inflation causes and control)
- `international-economics` — International Economics (International trade theories, balance of payments &amp; global institutions)
- `economic-planning` — Economic Planning (Growth vs development, planning frameworks &amp; unemployment)


### Government

**SSS 1** (8):
- `basic-concepts-govt` — Basic Concepts and Definitions of Government (Government as an institution, a process, and an academic study)
- `state-nation-society` — The State, Nation, and Society (Characteristics of a State, differences from nation, and social structures)
- `power-authority-sovereignty` — Power, Authority, Legitimacy, and Sovereignty (Sources of political power, validation of authority, and state sovereignty)
- `political-culture-socialization` — Political Culture and Socialization (Shared political values, beliefs, and agents of political learning)
- `forms-of-government` — Classical and Modern Forms of Government (Monarchy, aristocracy, oligarchy, autocracy, and democratic structures)
- `political-ideologies` — Major Political Ideologies and Systems (Socialism, capitalism, feudalism, communalism, and fascism)
- `constitutions-constitutionalism` — Constitutions and Constitutionalism (Sources, written vs unwritten, rigid vs flexible frameworks)
- `rule-of-law-powers` — Rule of Law, Separation of Powers, and Human Rights (Executive, legislative, and judicial boundaries; checks and balances)

**SSS 2** (8):
- `citizenship-rights-duties` — Citizenship, Human Rights, and Civic Duties (How citizenship is acquired/lost; rights, duties, and state obligations)
- `franchise-electoral-systems` — Franchise and Electoral Systems (History of voting, types of electoral frameworks, and delimitation)
- `political-parties-systems` — Political Parties and Party Systems (Functions of political parties, party systems, and manifestos)
- `pressure-groups-public-opinion` — Pressure Groups and Public Opinion (Influence of interest groups, public opinion polling, and mass media)
- `civil-service-public-admin` — The Civil Service and Public Administration (Administrative structure, civil service neutrality, and public organs)
- `public-corps-privatization` — Public Corporations and Privatization (Management of state enterprises, public utility challenges, and economic reforms)
- `local-govt-reforms` — Local Government and the 1976 Reforms (Grassroots administration, local finance, and modern local councils)
- `precolonial-political-systems` — Pre-Colonial Nigerian Political Systems (Traditional governance: Hausa-Fulani, Yoruba, and Igbo societies)

**SSS 3** (8):
- `colonial-administration-systems` — Colonial Administration Systems (Indirect Rule, Assimilation, Association, and their structural legacies)
- `early-constitutions` — Early Nigerian Constitutions (1922–1954) (Clifford, Richards, Macpherson, and Lyttelton constitutional progress)
- `post-independence-constitutions` — Post-Independence Constitutions (1960–1999) (1960 Independence, 1963 Republican, 1979, and 1999 frameworks)
- `nationalism-independence-road` — Nationalism and the Road to Independence (Nationalist movements, pioneer leaders, early press, and trade union activism)
- `military-rule-nigeria` — Military Rule and Democratic Transitions (Causes of military coups, supreme military councils, and return to civil rule)
- `nigeria-foreign-policy` — Principles of Nigeria’s Foreign Policy (Basic principles, national interest, determinants, and non-alignment)
- `regional-integration-africa` — Regional and Continental Organizations (Study of ECOWAS and the African Union (AU))
- `global-organizations` — Global Organizations (UN, Commonwealth, OPEC) (Objectives, organs, achievements, and Nigeria\)


### Literature

**SSS 1** (3):
- `intro-to-genres` — Introduction to Genres (Meaning, functions, prose, drama, poetry &amp; comparative writing)
- `literary-terms-devices` — Literary Terms and Devices (Figures of speech, structural devices, and narrative elements)
- `foundational-appreciation` — Foundational Literary Appreciation (Analyzing unseen prose passages, short poems, and settings)

**SSS 2** (3):
- `prescribed-drama` — Prescribed African and Non-African Drama (Act-by-act analysis of selected WAEC/NECO 2026-2030 plays)
- `prescribed-prose` — Prescribed African and Non-African Prose (Exploring selected 2026-2030 novels, styles, and themes)
- `prescribed-poetry` — Prescribed African and Non-African Poetry (Rhyme, meter, imagery, and style of selected syllabus poems)

**SSS 3** (3):
- `advanced-text-studies` — Advanced Prescribed Text Studies (WAEC/NECO drama and prose revision, subplots, and thematic connections)
- `advanced-poetry-studies` — Advanced Prescribed Poetry Studies (Socio-political context and stylistic analysis of remaining syllabus poems)
- `test-literary-appreciation` — Test of Literary Appreciation (Critical analysis techniques, structural analysis, and unseen passages)


### Agric

**SSS 1** (8):
- `meaning-scope-importance` — Meaning, Scope and Importance of Agriculture (Definitions, historical development, and national importance of farming)
- `developmental-problems-solutions` — Problems of Agricultural Development (Challenges facing West African farming and their structural solutions)
- `agricultural-programmes` — Agricultural Development Programmes (Analysis of government initiatives: OFN, Green Revolution, and ADP)
- `land-tenure-systems` — Land Tenure Systems in West Africa (Communal, inheritance, state-allocated, and tenant farming systems)
- `agro-allied-forestry` — Forestry and Agro-allied Industries (Forest reserves, economic products, and processing inter-relationships)
- `farm-tools-equipment` — Farm Tools and Equipment (Classification, usage, and maintenance of hand tools and implements)
- `agricultural-ecology` — Agricultural Ecology (Biotic and abiotic factors shaping West African crop and animal zones)
- `soil-formation-profile` — Soil Formation and Soil Profile (Physical, chemical, and biological weathering; soil horizons)

**SSS 2** (8):
- `soil-properties-ph` — Physical and Chemical Properties of Soil (Soil texture, structure, porosity, temperature, and pH management)
- `soil-fertility-fertilizers` — Soil Fertility and Plant Nutrition (Organic manures, chemical fertilizers, and crop rotation schedules)
- `farm-power-mechanization` — Farm Power and Mechanization (Sources of power, advantages, and limitations of farm mechanization)
- `tillage-machinery` — Tillage and Farm Machinery (Tractors, disc and mouldboard ploughs, harrows, and planters)
- `farm-surveying-layout` — Farm Surveying and Layout (Survey equipment, measurement principles, and farm design layouts)
- `irrigation-drainage` — Irrigation and Drainage Systems (Types, planning, maintenance, and soil water control mechanisms)
- `crop-classification-requirements` — Classification of Crops (Botanical, life-cycle, and economic groupings; growth requirements)
- `crop-husbandry` — Crop Husbandry and Management (Agronomic practices for selected cereals, legumes, and cash crops)

**SSS 3** (8):
- `weed-science` — Weed Science (Classification, reproduction, dispersal, and integrated control methods)
- `crop-pests-diseases` — Crop Pests and Diseases (Life cycles of insect pests, pathogens, symptoms, and control)
- `animal-anatomy-physiology` — Animal Anatomy and Physiology (Anatomical systems of ruminants and non-ruminants compared)
- `animal-nutrition-ration` — Animal Nutrition and Ration Formulation (Feed classification, balanced diets, and Pearson square calculations)
- `livestock-husbandry-management` — Livestock Husbandry and Management (Practical management of poultry, cattle, pigs, sheep, and goats)
- `animal-health-diseases` — Animal Health and Parasitology (Newcastle, anthrax, trypanosomiasis, ticks, and liver flukes)
- `aquaculture-fisheries` — Aquaculture and Fisheries (Fish pond construction, species selection, feeding, and preservation)
- `agric-economics-marketing-extension` — Agricultural Economics and Extension (Diminishing returns, records, marketing channels, and extension agencies)


### Geography

**SSS 1** (2):
- `physical-geography` — Physical Geography (The solar system, earth movements, rock cycle, and denudation)
- `practical-geography-basics` — Practical Geography Basics (Map scales, distance measurement, and grid reference systems)

**SSS 2** (4):
- `geomorphology` — Geomorphology (Denudational processes and landforms of water, wind, waves, and ice)
- `climatology-hazards` — Climatology and Environmental Hazards (Weather elements, Koppen\)
- `human-geography` — Human Geography (Population dynamics, settlement patterns, and world economic activities)
- `practical-relief-contours` — Practical Relief and Contours (Contour representation, cross-sections, intervisibility, and drainage)

**SSS 3** (3):
- `regional-geography-nigeria` — Regional Geography of Nigeria (Location, geology, relief, climate, soils, agriculture, and industries)
- `west-africa-world-studies` — West Africa and World Studies (ECOWAS features, industrial regions, and global agricultural belts)
- `advanced-mapwork` — Advanced Mapwork and Interpretation (Map reduction, enlargement, and drainage/landuse interpretation)



## Appendix B — External repos / services referenced

| Reference | Used for |
|---|---|
| `cdn.jsdelivr.net/gh/ola1de/Exam-Questions-Data@main/json/` | CBT question JSON (`<EXAM>_<file>_<year>.json`) |
| `cdn.jsdelivr.net/gh/ola1de/English-Quiz@main/` | English Quiz category JSON |
| `cdn.jsdelivr.net/gh/ola1de/mystudy-textbooks` | Keypoints topic JSON (`<folder>/<file_prefix>-<level>-<slug>.json`) |
| `cdn.jsdelivr.net/gh/ola1de/vocabulary-database@main` (+ raw.githubusercontent fallback) | Vocabulary data |
| `cdn.jsdelivr.net/gh/ola1de/mystudy-dic@main/data/` | Dictionary `<letter>.json` |
| `cdn.jsdelivr.net/gh/ola1de/nigeria-constitution@main/` | Constitution text + `manifest.json` |
| `cdn.jsdelivr.net/gh/ola1de/mystudy-pwa@main/sw.js` | Service worker |
| `https://mystudy-licensing.mystudysuite.workers.dev/{check,auth,make}` | Licensing + admin key generation |
| `https://bot.mystudysuite.workers.dev/chat/json` | Study Assistant chatbot |
| `https://raw.githubusercontent.com/ola1de/random-quotes/main/Quotes.txt` | Quotes (fetched by an unspecified widget) |
| `wa.me/2348100259673` | Premium receipt + support WhatsApp |
| `mystudyacademicsuite@gmail.com` | Support email (About/Contact) |
| Blogger blog ID `5334759134063131007` | Comments iframe, feed |

## Appendix C — localStorage / sessionStorage keys found

| Key | Purpose |
|---|---|
| `MST_APP_DATA` | Main blob: `profile{name,institution,course,theme,license}`, `cgpa`, `exams`, `lectures`, `studySessions`, `feynman`, `word{docs,activeId}`, `cbtHistory`, `budget{limit,expenses}`, `settings{notifications, aiProctor}` (+ cookie fallback if < 3500 chars) |
| `_sys_dev_id` | Device ID (`Mxxx-xxxx` / `Dxxx-xxxx`) |
| `_sys_core_auth_v2` | Premium unlock token (reversible transform of Device ID — see §2) |
| `MST_CBT_RESUME` | In-progress CBT exam state |
| `MST_EQ_HIST` / `MST_EQ_RESUME` | English Quiz history (≤100) / in-progress quiz |
| `MST_EQ_CACHE_<id>` | English Quiz question cache (sessionStorage) |
| `MSE_<EXAM>_<file>_<year>` / `MSE_PRI_<file>` | Cached CBT question JSON |
| `mst.textbook.v1` | Keypoints progress per topic (`modulesDone`, `bestScore`, `avgScore`, `tests`) |
| `MST_TB_HIST` / `MST_TB_STREAK` / `MST_TB_LAST_DAY` | Keypoints test history / streak |
| `mst.vocab.v1` / `MST_VOCAB_HIST` / `MST_VOCAB_LEARNED` / `MST_VOCAB_STREAK` / `MST_VOCAB_LAST_DAY` | Vocabulary progress |
| `mst_bookmarks` | Saved posts/pages |
| `mst_profile` | Legacy profile key (referenced; main profile lives in `MST_APP_DATA`) |
| `mst_skin` | Selected skin (default / duolingo) |
| `MST_VISIT_COUNT` | Visit counter (Profile achievements) |
| `msa_chat_v4` | Study Assistant history (last 60) |
| `mst_app_installed`, `mst_cookie_ack` / `mst_cookie_ok`, `mst_notif_decided`, `mst_last_backup`, `mst_backup_nudge`, `mstBuddyPos` | PWA install, cookie consent, notification choice, backup nudge, assistant button position |

---
*Method note: counts were produced by parsing, not by running the theme. "Available" in the Keypoints registry means the template lists the subject as available; it does not verify the JSON file exists in the linked repo. Question counts (5/40) are the hard-coded slice limits, not the size of any question bank.*
