# MyStudy v2 — Keypoints, Vocabulary & ALL Tools: audit + fix

Date: 24 Nov 2026. Status: **audit + fix complete for keypoints and vocabulary; tools audit + rebuild plan complete.** Nothing pushed to GitHub — all fixes live in local clones under `/tmp/mystudy-repos/` (see the /tmp incident in §5; back them up under `~/workspace/` before any further work there).

Sources: template inventory (`template-inventory-24-nov.md`), repo audit (`repo-audit-24-nov.md`), and the three part reports below.

## Part reports (the full detail)

- Keypoints: [keypoints-vocab-tools-part-keypoints.md](sandbox://workspace/mystudy/docs/keypoints-vocab-tools-part-keypoints.md)
- Vocabulary: [keypoints-vocab-tools-part-vocab.md](sandbox://workspace/mystudy/docs/keypoints-vocab-tools-part-vocab.md)
- Vocabulary expansion manifest: [vocabulary-expansion-manifest-24-nov.md](sandbox://workspace/mystudy/docs/vocabulary-expansion-manifest-24-nov.md)
- Tools: [keypoints-vocab-tools-part-tools.md](sandbox://workspace/mystudy/docs/keypoints-vocab-tools-part-tools.md)

Scripts persisted: `~/workspace/mystudy/tools/vocab_audit.py`, `vocab_fix.py`, `vocab_build_new.py`, `vocab_new_1.py`–`vocab_new_5.py`; original vocabulary files backed up at `~/workspace/mystudy/tools/backup-24-nov-orig/`.

---

## 1. Keypoints — audit + fix (mystudy-textbooks)

**Before:** 165 chapters, 503 modules, 4,630 quiz questions (4,434 unique stems), 12 subjects, SSS 1–3 only. 154 of 165 chapters had <5 modules; quiz per chapter was bimodal (57 chapters at exactly 50, 108 at 15–20). 196 same-stem quiz repeats (180 Maths, 16 English); 84 questions had a duplicated option inside their own 4 options; quiz `answer` was a string (`"1"`) in 8 subjects (1,996 questions) and an int in 4. Outline length ≠ module count in 143 of 165 chapters.

**After (verified by re-counting the files: 274 JSON files, 1,482 modules, 13,650 quiz, 0 parse errors):** 273 chapters, 1,482 modules, **13,650 quiz questions — exactly 50 unique-stem questions per chapter**, every `answer` an int 0–3, every question with 4 distinct options, no duplicate slugs within (subject, level), Mathematics index updated.

### Before / After (chapters / modules / quiz)

| Subject | Before | After |
|---|---|---|
| Accounting | 8 / 20 / 129 | 8 / 47 / 400 |
| Agric | 24 / 76 / 375 | 24 / 138 / 1,200 |
| Biology | 13 / 39 / 208 | 13 / 78 / 650 |
| Chemistry | 12 / 49 / 600 | 12 / 72 / 600 |
| Commerce | 9 / 27 / 144 | 9 / 53 / 450 |
| Economics | 12 / 24 / 213 | 12 / 72 / 600 |
| English | 15 / 47 / 750 | 15 / 79 / 750 |
| Geography | 9 / 23 / 153 | 9 / 54 / 450 |
| Government | 24 / 65 / 384 | 24 / 135 / 1,200 |
| Literature | 9 / 22 / 174 | 9 / 53 / 450 |
| Mathematics | 20 / 64 / 1,000 | 20 / 103 / 1,000 |
| Physics | 10 / 47 / 500 | 10 / 58 / 500 |
| CRS / IRS / Civic / History / Computer / Further Maths / Hausa / Igbo / Yoruba (new) | 0 / 0 / 0 | 12 each / 60 each / 600 each |
| **Total** | **165 / 503 / 4,630** | **273 / 1,482 / 13,650** |

**Schema:** Mathematics keeps its own schema (`topic`/`ss_level`/`icon`/`color` vs `title`/`level` for the other 20 subjects) — not converted. New subjects use the standard schema; files keep the repo's existing per-subject schema so the v1 reader still works. Normalised v2 schema for the importer (in the part report): D1 tables `subjects`, `keypoint_topics`, `keypoint_modules`, `keypoint_questions`, unique key subject+level+slug (English slugs repeat across levels).

**Sourcing (no invented facts):** per-question `source` field — chapter notes kept 4,339; real past questions 7,240 (JAMB 2021–25, WAEC/NECO 2024–25, legacy TXT banks; passage blocks and placeholders excluded; each bank question used in at most one chapter per subject); **2,071 syllabus-modelled practice questions (15.2%, labelled `practice: true`)** built only from past-question facts in the same subject, chapter-note definitions, or computed numeric variants. Practice share is highest where the bank is smallest: Yoruba 50%, Hausa 43%, Computer/Further Maths 42%, History 40%, Civic 30%; CRS 0%.

**Not completed / flags:** JSS 1–3 and Primary keypoints still entirely missing. Literature chapters are still generic frameworks, not the actual WAEC/NECO prescribed texts. **2,071 practice questions need human subject review** before being presented as exam-grade; no full factual read-through of all 13,650 questions was done (structural validation + spot checks only). 107 modules remain <100 words (mostly formula-dense Maths/Physics), 5 Maths modules <50 words.

---

## 2. Vocabulary — audit + fix (vocabulary-database)

**Before:** 24 categories / 2,400 words / 2,400 quiz. Index v1 listed only 14 categories, no counts. Entry defects **98** (empty/missing fields, fragment definitions, definitions equal to the word, examples not containing the word). Quiz defects **120** (42 answer mismatches, 30 duplicate stems, 7 duplicate options, 41 "correct word not among options"). Duplicate words within a category: dietary-habits 10, obsessions 15, words-for-killing 5, forms-of-government 2, personality-types 1, philosophical-stances 1, proverbs 1, time-and-frequency 1. Global id collision: `ph-01`–`ph-50` used by both phobias and philosophical-stances. Wrong entries included dietary `dh-36` "Kaufmann" (a German surname, not a faster), obsessions "Dinomania" defined as "Compulsion to dance" (it is fascination with dinosaurs), baby-animals "Aleven" defined "Baby swan (variant)" (alevin is a newly hatched fish), words-for-killing "Feoticide" (misspelling of Foeticide, which already exists), phobias "Aerophobia (draft)" and "Ailurophobia (severe)" (editing notes left in the words).

**After (verified by re-counting the files: 44 files, 4,400 words, 4,400 quiz, 0 bad JSON; index v3, 44 categories):** **44 categories / 4,400 words / 4,400 quiz. Entry defects 98 → 0; quiz defects 120 → 0.**

**What was fixed in the 24 existing categories (249 entries changed, verified by diff against the original backup; all 2,400 quiz items regenerated):** duplicate words replaced with verified standard terms; wrong entries corrected (Kaufmann → Faster, Dinomania → dinosaurs, Aleven → Alevin, "A newly hatched fish, still carrying its yolk sac.", Crias → Cria, Feoticide removed in favour of Foeticide, Didaskaleinophobia for "Aerophobia (draft)", Athazagoraphobia for "Ailurophobia (severe)"); phobias ids `ph-01`–`ph-50` renamed → `pho-01`–`pho-50`, removing the collision; duplicate definitions disambiguated; fragment definitions expanded to full sentences; baby-animals `ba-053`–`ba-100` given full-sentence definitions.

**20 new categories × 100 words + 100 quiz (2,000 words):** mathematics, further-mathematics, physics, chemistry, biology, economics, government, geography, literature, commerce, accounting, agriculture, CRS, IRS, history, civic-education, computer-studies, plus Hausa, Igbo and Yoruba (100 common terms each with English glosses and a sentence in the language + English translation). Each follows the existing schema exactly: `{id, word, pos, definition, example}` + quiz `{id, question, options[4], answer (index), explanation}`.

**Dictionary verification (mystudy-dic merged.json, 121,340 entries):** original words 2,014/2,400 (84%) verified; new English single-word terms 1,086/1,208 (90%). The 122 unverified terms are standard specialist terms, proper names and abbreviations (listed grouped by category in the manifest), and language-category words are excluded from dictionary coverage by design. Cross-category shared words now 240 (26 same-sense, 214 different-sense) — legitimate by design, not de-duplicated.

**Index:** v3, 44 categories, count 100 each. `git status` in the vocabulary clone shows 24 modified files + 20 new files + index, ready for review and push.

---

## 3. ALL tools — v1 audit + v2 rebuild model

Full detail (34 tools, each with v1 behaviour grounded in template line numbers, flaws, v2 model, client/server split, one-line data model, free-tier out-of-scope): [keypoints-vocab-tools-part-tools.md](sandbox://workspace/mystudy/docs/keypoints-vocab-tools-part-tools.md).

**New findings from grepping the template (beyond the two source docs):**
- Citation Generator is a broken promise: copy advertises Chicago/IEEE/Vancouver, but `gen()` implements only APA/MLA/Harvard — "chicago" has 0 hits.
- Dictionary copy is false: tile claims "200,000+ words" and "native-speaker pronunciation" — repo has 121,340 merged entries and pronunciation is browser `speechSynthesis` TTS.
- OCR is real but heavy: Tesseract.js 5.0.4 lazy-loaded, ~12 MB first download; "handwritten text" promised in copy, Tesseract is poor at handwriting.
- Summarizer is extractive only: sentence-ranking, keywords = raw word frequency; no abstractive summary.
- Text Compare: no diff library/algorithm traced — unverifiable implementation.
- CBT: `#cbt-count` confirmed decorative; only one calculator toggle traced vs the promised "Scientific calc" for WAEC/NECO.

### Tool-by-tool rebuild model

| Tool | v1 flaw | v2 model | Client/Server |
|---|---|---|---|
| CGPA Calculator | Local-only; one hard-coded threshold table for all universities | Rule engine, per-university grading tables in D1, CSV import, retake modelling | Client calc + D1 |
| Graduation Predictor | One-shot arithmetic, no plan, not linked to CGPA | Scenario planner (best/expected/min) over real semesters, impossible-target flag | Client |
| GPA → Class | Bare threshold lookup, no inverse/context | Fold into CGPA engine as lookup + inverse solver + shareable link | Client + D1 |
| Admission Toolkit | Frozen 78-course table in the theme; unverified formulas; no O-Level grade check | D1 admission-rules DB (sourced, dated, admin-editable) + formula engine + checklist | Client calc + D1 |
| Flashcards | Crude 3-box Leitner, hand-typed decks only, no sync | SM-2 scheduler (FSRS later), ready-made decks from Keypoints/vocab banks, cloze + media | Client scheduler + D1 |
| Exam Planner | "Alarms" die when the tab closes (no working service worker) | Calendar-backed planner, Worker cron + Web Push reminders, ICS export | Client + Worker cron/push |
| Study Planner | Fixed 25:00 timer; Feynman = plain textarea | Adaptive focus sessions linked to topics; Feynman scored by Workers AI rubric | Client timer + Workers AI |
| Lecture Schedule | Dateless weekly grid, no exceptions, duplicates Timetable | Recurring calendar with semester range + exceptions, room/lecturer | Client + D1 |
| Class Timetable | Same data as Lecture Schedule, no clash detection, "share" = printout | Week-grid view of the same calendar, clash detection, shareable link + ICS | Client + D1 |
| Revision Timetable | Generator with no spacing algorithm traced | Spaced-repetition scheduler driven by exam dates + mastery data, regenerates on misses | Client + D1 |
| Deadline Planner | Bare list, no priorities/reminders | Priority-scored board (days × weight × effort), push reminders, ICS | Client + D1 + push |
| Note Outline Builder | No parsing or hierarchy validation | Outline engine: parse notes into a real tree, export to Word Office/PDF, optional AI gap check | Client (+ Workers AI) |
| Budget Tracker | One limit + flat list; no categories/trends; float money | Envelope budgeting, recurring costs, reports, integer kobo in D1 | Client + D1 |
| Study Streak & XP | Self-awarded, gameable, device-local, 3 disagreeing streaks | Server-verified XP (only real completed events earn points), one streak, opt-in leaderboard | Server-authoritative |
| Word Office | TinyMCE + lossy html-docx-js export; docs in localStorage blob | TipTap/ProseMirror, real `docx` library export, D1+R2 docs, autosave + versions | Client editor + D1/R2 |
| PDF Toolkit | Main-thread processing, no size guards, E-Sign = PNG not embedded signature | pdf-lib + pdf.js in Web Workers, chunked + cancellable, real compress, signature embedded via pdf-lib | Client (Web Workers) |
| Image Toolkit | Main-thread canvas, batch = loop, no HEIC/AVIF, all-or-nothing EXIF | OffscreenCanvas worker pool, target-KB binary search, WebP/AVIF out, granular EXIF, QR options | Client (Web Workers) |
| Word & Character Counter | Counts only | + Flesch readability, reading/speaking time, keyword density, word-goal meter, .docx/.pdf import | Client |
| Citation Generator | Only APA/MLA/Harvard implemented despite Chicago/IEEE/Vancouver copy | Real CSL engine (citeproc, 9,000+ styles) + DOI/ISBN lookup via Worker, .bib/RIS export | Client CSL + server lookup |
| Quick Cite | Same 3-style limit, disconnected from Citation Generator | Fast path into the reference library, in-text/narrative + pinpoint, inserts into Word Office + auto-bibliography | Client + D1 |
| Note Summarizer | Extractive sentence-ranking only; "key terms" = word frequency | Extractive baseline (offline) + Workers AI abstractive summary, labelled AI, editable, saved per topic | Client + Workers AI |
| Text Compare | No diff algorithm traced; side-by-side only | Word-level Myers diff (diff-match-patch), similarity %, accept/reject, export to Word Office | Client |
| Chart Generator | Hand-typed tables, no live data, no SVG, no saved charts | Live data binding (Budget/CBT/CGPA), Chart.js + ECharts, SVG/PNG 2×/PDF/CSV, insert into Word Office | Client |
| Dictionary | Per-letter multi-MB JSON fetch; 200k+ claim false (121,340); TTS sold as native audio | D1 FTS dictionary (merged.json import), prefix search API, honest TTS label, save-to-Vocabulary | Server API (D1) |
| Vocabulary | index.json lists 14/24 categories (10 unreachable); fixed 30-Q test, not adaptive | Adaptive SRS trainer over all 24 categories, cloze rounds, TTS, Dictionary add-word | Client + D1 |
| English Quiz | Client-side free cap; "Listening" has no audio; history capped at 100 | Server-gated sets + entitlement, per-topic mastery, real TTS listening mode, uncapped history | Client + server gate |
| CBT (brief) | Decorative Q-count input; scientific calc untraced; client-side premium; placeholder years served as real exams | Server-authoritative: canonical D1 question model, server scoring, Paystack-verified entitlement, only real years offered | Server-authoritative |
| Study Assistant | No retrieval, canned local fallback, no actions, 20 s timeout, no streaming | RAG over Keypoints/Constitution/Dictionary + student data, Workers AI, streaming, tool-aware actions | Server (Workers AI + D1) |
| Legal & Civic Library | Constitution viewer only; "statutes & civic docs" unbuilt; schedules unstructured; amendment status unstated | Versioned Constitution in D1 + FTS + structured LGA schedules + sourced statutes index | Server (D1) |
| Blog/News reader | No editor/SEO/upload; author shows "Unknown"; Fraunces never loaded; two disagreeing TOCs | React admin News module (editor, SEO, R2 images, scheduling) + D1 reader keeping the loved format | Server (D1/R2) |
| Bookmarks | Flat localStorage array, no folders/sync, posts only | Synced collections: bookmark anything (post/topic/section/word/question) + folders/tags/notes | Client + D1 |
| Profile & Settings | 3 text fields, no identity/recovery; admin `/auth` backdoor on save | Real account: TOTP + 3 security questions, avatar to R2, exam target, notification prefs, role-based admin | Server (D1/R2) |
| Home dashboard | Static, local blobs only, no weak-topic/due-review awareness | Server aggregates: next exam, due flashcards, weakest 3 topics, streak, one recommended action | Client + server aggregates |
| Unit Converter (bonus) | 6 categories, no currency/data/speed, no history | 12+ categories, daily cached FX rates in D1 (dated), offline factor tables, recent conversions | Client (+ rates API) |

**Free-tier honest outs:** heavy/multi-page OCR, server-side large-PDF processing, video, real-time video proctoring review, separate vector DB (FTS instead), SMS reminders, server-side image processing, AI upscaling, bank sync, live JAMB CAPS data. OCR stays client-side Tesseract.js for printed English only; handwriting OCR is OUT as a promised feature.

---

## 4. What still needs a human / the owner

- **Human subject review:** the 2,071 syllabus-modelled practice keypoint questions (15.2%) before they are presented as exam-grade; the 122 unverified vocabulary terms are listed in the manifest (standard specialist terms — spot-check, don't blindly trust).
- **Still missing:** JSS 1–3 and Primary keypoints; Literature prescribed texts (chapters are generic frameworks); Post-UTME / BECE banks (no repo data).
- **Push decisions (per-action approval still required):** vocabulary clone shows 24 modified + 20 new files; textbooks clone shows 166 modified + 108 new files. Neither is pushed. Review the diffs, then push each repo separately.

## 5. Incident — /tmp loss (flagged, do not ignore)

Mid-task, `/tmp/mystudy-repos/` lost Exam-Questions-Data, English-Quiz, mystudy-pwa, nigeria-constitution, random-quotes, the textbooks' 12 original folders, and a `/tmp` backup — outside this task's control. Textbooks + Exam-Questions-Data were restored with fresh shallow public clones; I re-cloned the other four repos afterwards, so all 8 are present again — **but the earlier unpushed fixes that lived only in those clones are gone from disk:** the 11 corrupt exam files are corrupt again and placeholders are back to 190 (reports survive, fixes are redoable, but must be redone, not assumed done); the English-Quiz duplicates fix is likewise gone (9 Old files back, no `archive/`). The keypoints and vocabulary fixes in this report survived because they live in the restored/current clones, verified by re-counting above. **Future fix jobs must keep backups under `~/workspace/`, not `/tmp`, and copy fixed files into `~/workspace/mystudy/` promptly.**
