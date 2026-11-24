# MyStudy v2 — Tool-by-Tool Audit & Rebuild Models

**Source:** Blogger template `~/workspace/user/files/theme-5334759134063131007__8__0_xo41.xml`
(1.7 MB, 24,438 lines, MyStudy Academic Suite v4, design system v15 "Quiet Confidence").
**Inventory refs:** `template-inventory-24-nov.md` (§1 tool inventory, §2 CBT, §5 other tools),
`repo-audit-24-nov.md` (§4 dictionary, §5 PWA, §6 textbooks, §7 constitution, §8 vocabulary, §9 quotes).
**Status:** read-only audit. Nothing in the template or any repo was edited; nothing was pushed.
**Rule applied:** no tool is "same as v1" — every tool gets a different/better v2 model.
**Free-tier frame (all tools):** Cloudflare Workers free — 100,000 requests/day, 10 ms CPU per
request, D1 + R2. Anything needing sustained CPU, large-file rendering, video, or a
long-running process cannot run on the Worker and must run in the browser (client-side,
optionally in a Web Worker) or be declared out of scope. Server-side is reserved for
things only a server can do: auth/entitlement, cross-device sync, shared data, payments,
and AI calls via Workers AI.

## Summary table

| # | Tool | v1 flaw (one line) | v2 model (one line) | Client / Server |
|---|---|---|---|---|
| 1 | CGPA Calculator | Local-only rows; hard-coded 4.0/5.0 thresholds; no verification | Rule-engine calculator with per-university grading tables in D1, versioned | Client calc + D1 tables |
| 2 | Graduation Predictor | One-shot arithmetic; no plan, no "what-if" | Monte-Carlo / scenario planner over remaining semesters | Client |
| 3 | GPA → Class | Bare threshold lookup, no context | Same engine as #1 exposed as a lookup API + "what GPA do I need" inverse | Client (+ D1 tables) |
| 4 | Admission Toolkit | Static 78-course table; unverified per-school formulas; no updates | D1 admission-rules DB, admin-editable, per-school formula engine + JAMB CAPS status checklist | Client calc + D1 rules |
| 5 | Flashcards (Leitner) | 3-box Leitner, user decks only, no bank, no sync, no media | SM-2/FSRS scheduler + shared decks generated from Keypoints/quiz banks | Client scheduler + D1 decks |
| 6 | Exam Planner | Countdowns + alarms that die when the tab closes | Calendar-backed planner with push reminders via scheduled Worker + push subscription | Client + Worker cron/push |
| 7 | Study Planner (Pomodoro + Feynman) | Fixed 25:00 timer; Feynman = plain text export | Adaptive focus sessions + Feynman explainer checked by Workers AI rubric | Client timer + Workers AI |
| 8 | Lecture Schedule | Weekly grid in localStorage, no recurrence exceptions | Real calendar (recurring events, exceptions, room + lecturer) synced to Google Calendar | Client + D1 (+ Google Cal) |
| 9 | Class Timetable | Printable grid only; no conflict detection | Constraint-checked timetable builder with clash detection + shareable link | Client + D1 |
| 10 | Revision Timetable | Generator with no spacing algorithm traced | Spaced-repetition-aware scheduler driven by exam dates + mastery data | Client + D1 |
| 11 | Deadline Planner | Bare list in app blob; no reminders, no priorities | Priority-scored deadline board with notifications + calendar export | Client + D1 + push |
| 12 | Note Outline Builder | Heading prompt tool; no structure validation | Outline engine that parses pasted notes into a real hierarchy + exports to Word Office | Client (+ Workers AI option) |
| 13 | Budget Tracker | Single monthly limit + expense log; no categories, no trends | Envelope budgeting with categories, recurring costs, ₦ reports + CSV export | Client + D1 |
| 14 | Study Streak & XP | Self-awarded XP, gameable, device-local | Server-verified XP: only real completed sessions/quizzes earn XP; leaderboards opt-in | Server-verified (D1) |
| 15 | Word Office | TinyMCE + html-docx-js lossy export; docs in localStorage blob | TipTap/ProseMirror editor, real `docx` library export, D1+R2 docs, autosave + versions | Client editor + D1/R2 |
| 16 | PDF Toolkit | 10 tabs, all in-browser; OCR is a 12 MB download; no file-size guard | Same tools, rebuilt on pdf-lib + pdf.js in Web Workers, chunked, with honest size caps | Client (Web Workers) |
| 17 | Image Toolkit | Canvas one-at-a-time; batch is a loop; no HEIC/AVIF, no real EXIF | `createImageBitmap` + OffscreenCanvas worker pipeline, real EXIF parse, AVIF/WebP output | Client (Web Workers) |
| 18 | Word & Character Counter | Regex counts, no readability, no goals | Counter + readability (Flesch, grade level) + keyword density + writing goals | Client |
| 19 | Citation Generator | Only APA/MLA/Harvard implemented despite Chicago/IEEE/Vancouver copy | CSL-based engine (citeproc) with 9,000+ real styles + DOI/ISBN lookup | Client CSL + server lookup |
| 20 | Quick Cite | Same 3-style formatter, inline only, no library | In-text citation picker wired to a personal reference library (D1) | Client + D1 |
| 21 | Note Summarizer | Extractive sentence-ranking only; no abstractive summary | Extractive baseline + Workers AI abstractive summary (Llama) with length control | Client extractive + Workers AI |
| 22 | Text Compare | Side-by-side compare; no diff library traced | Word-level Myers diff (diff-match-patch) + merge/export, plagiarism-style similarity score | Client |
| 23 | Chart Generator | Chart.js table→chart, static export | Chart.js + ECharts option, live data binding to Budget/CBT stats, embeddable + PNG/SVG | Client |
| 24 | Dictionary | Fetches per-letter JSON from jsDelivr; claims 200k+ words, repo has 121,340; "native-speaker pronunciation" is browser TTS | D1 full-text dictionary (merged.json import), prefix search API, real IPA + audio via TTS only where honest | Server API (D1) |
| 25 | Vocabulary | 30-Q test, 10 of 24 categories unreachable (index lists 14/24) | Adaptive vocab trainer: SRS + category-complete index + sentence cloze + audio | Client + D1 |
| 26 | English Quiz | 9×100 Qs, free cap 5 Qs/10 min, client-side gate | Server-gated quiz with per-topic mastery, explanations, timed exam mode | Client + server gate (D1) |
| 27 | CBT | Decorative Q-count input; promised scientific calc untraced; client-side premium; 190 placeholder files served as real years | Server-authoritative CBT: canonical question model, per-exam config, server-scored, Paystack-verified entitlement | Server-authoritative |
| 28 | Study Assistant chatbot | Remote Worker + local rule fallback; no RAG, no memory of user data | RAG assistant over MyStudy content (D1 vector-lite/FTS) + tool-aware actions, Workers AI | Server (Workers AI + D1) |
| 29 | Legal & Civic Library / Constitution | Constitution viewer only; "statutes & civic docs" promised, not built; schedules unstructured | Versioned Constitution in D1 with section-level search + a real statutes index (sourced, dated) | Server (D1) |
| 30 | Blog / News reader | Blogger-dependent; no editor, no SEO fields, author shows "Unknown" | React admin News module: editor, SEO fields, categories/tags, image upload to R2, scheduled publish | Server (D1/R2) |
| 31 | Bookmarks | `mst_bookmarks` array in localStorage; no folders, no sync | Synced bookmark collections with folders/tags + reading-list progress | Client + D1 |
| 32 | Profile & Settings | 3 text fields + theme/accent/skin; no avatar, bio, email, exam target; admin `/auth` backdoor on save | Real account: TOTP + security questions, avatar upload, exam targets, notification prefs | Server (D1/R2) |
| 33 | Home dashboard | Static greeting + countdown + tiles; stats read local blobs only | Personalised dashboard driven by server aggregates: next exam, streak, weak topics, due reviews | Client + server aggregates |
| 34 | Unit Converter | (Bonus — inventory §1 #46) plain factor table, 6 categories | Extended converter: 12+ categories incl. currency via live rates, offline factor cache | Client (+ rates API) |

**Cross-cutting v1 facts (all tools):** all user data lives in `localStorage` — main blob
`MST_APP_DATA` plus per-tool keys (inventory Appendix C). There is no sign-in, no password,
no Google auth, no Paystack anywhere in the file (Paystack: 0 hits). Premium is a manual
₦2,000 bank transfer + WhatsApp key, enforced only client-side
(`_sys_core_auth_v2 = reverse(btoa(deviceId + '_LOCAL_LIC_V1'))`, inventory §2).
Libraries loaded from CDN at runtime: pdf-lib 1.17.1, jsPDF 2.5.1, mammoth 1.6.0,
html2canvas (via html2pdf.js 0.10.1), TinyMCE 6.8.2, KaTeX, Chart.js, pdf.js 3.11.174,
Tesseract.js 5.0.4 (lazy, ~12 MB), html-docx-js, docx-preview, JSZip.

---

## 1. CGPA Calculator

**(a) v1 — what it does.** Route `?p=cgpa` (inventory §1 #11). 4.0/5.0 scales (5.0 adds grade E);
grade points A=5…F=0 on 5.0, A=4…F=0 on 4.0. Class thresholds hard-coded in `classOf`
(template L15984): 5.0 — ≥4.5 First, ≥3.5 Second Upper, ≥2.4 Second Lower, ≥1.5 Third,
≥1.0 Pass; 4.0 — ≥3.5 First, ≥3.0 Upper, ≥2.0 Lower, ≥1.0 Pass. Inputs: name, institution,
course (autocomplete from built-in `NIG_INST` / `NIG_COURSES` lists, L15969–15970), semester
name, per-course rows (title/code/units/grade). Outputs semester GPA, cumulative CGPA, class,
printable transcript (hidden iframe, watermark + logo). Draft auto-saves; semesters
save/edit/delete. Storage: `MST_APP_DATA.cgpa` (inventory Appendix C).

**(b) Flaws.** Local-only: lose the browser, lose every semester. One hard-coded threshold
table for all Nigerian universities — but grading/class boundaries genuinely differ by
institution (e.g. some use 4.5/3.5/2.5 cutoffs, some 4.0-scale variants), so the tool can
misclassify a real student's class. No import (no CSV, no result-sheet upload), no
carry-over/F-grade retake modelling, no "what grade do I need next semester" inverse, and
the printable transcript is a decorative iframe print, not a verifiable document.

**(c) v2 model.** Rule-engine calculator: the arithmetic stays client-side (instant, offline),
but grading tables live in D1 as versioned per-university rules
(`university_id, scale, grade_points JSON, class_thresholds JSON, source, verified_at`),
editable by admin and selectable by the student's institution. Add CSV import, retake/
carry-over simulation, and a "required GPA" solver. Transcript export becomes a real PDF
(jsPDF/pdf-lib) with the student's verified profile. **Data model:** `cgpa_semesters(id,
user_id, name, scale_id)` + `cgpa_courses(id, semester_id, code, title, units, grade)`.
**Client/server:** client computes; D1 serves grading tables + stores semesters (sync).

**(d) Out of scope (free tier).** Official transcript verification against a university
portal (no such API exists); issuing any document that claims to be an official transcript.

## 2. Graduation Predictor

**(a) v1.** Route `?p=predictor` (inventory §1 #12). Target class + semesters left → the exact
GPA required each semester. Pure computed output, no storage.

**(b) Flaws.** Single-point arithmetic with no uncertainty: it tells a student "you need 4.62
every semester" with no sense of whether that is plausible, no per-course plan for getting
there, no handling of retakes, dropped courses, or differing unit loads per semester, and
the result is not saved or linked to the CGPA tool — the two tools do not talk to each other.

**(c) v2 model.** Scenario planner built on top of the CGPA store: pull the student's actual
semesters, then compute required-GPA curves per remaining semester under three scenarios
(best/expected/minimum unit loads), flag mathematically impossible targets honestly
("no combination of remaining units reaches First Class — Second Upper is the ceiling"),
and let the student assign target grades per upcoming course to see the projected CGPA
move live. **Data model:** derived view over `cgpa_semesters` + `cgpa_courses` plus
`graduation_plans(id, user_id, target_class, semesters_left, plan JSON)`. **Client/server:**
client-side only; server only persists the plan.

**(d) Out of scope.** Any guarantee or prediction presented as an official university outcome;
admission/graduation advice beyond arithmetic.

## 3. GPA → Class of Degree

**(a) v1.** Route `?p=gpaclass` (inventory §1 #13). Type a CGPA, pick 4.0/5.0 scale, see the
class instantly. Same `classOf` thresholds as §1 (L15984).

**(b) Flaws.** Same hard-coded table problem as the CGPA tool, in a tool that looks
authoritative while knowing nothing about the student's university. No inverse ("what CGPA
do I need for Second Upper?"), no boundary warnings (e.g. 3.49 vs 3.50 is one hundredth of
a point), no explanation of what each class means for NYSC/employment/scholarships.

**(c) v2 model.** Do not rebuild it as a standalone page: fold it into the CGPA rule engine
as a lookup endpoint + inverse solver, and surface it as a widget inside CGPA, Predictor,
and Profile ("your current class"). The standalone route becomes a thin shareable page
(`?gpa=3.62&scale=5&uni=UNILAG`) that deep-links with the university pre-selected.
**Data model:** reuses the D1 grading tables from §1; no new tables. **Client/server:**
client lookup; D1 tables.

**(d) Out of scope.** Same as §1 — no official classification.

## 4. Admission Toolkit (UTME combo checker + Post-UTME aggregate predictor)

**(a) v1.** Routes `?p=admission`, `?p=admission-combo`, `?p=admission-agg` (inventory §1
#23–25, §5). Combo checker: 8 faculties, **78 courses**, each with 3 UTME subjects +
5 O-Level subjects (English + Maths usually compulsory) — `COURSES` (template ~L18959).
Aggregate predictor: JAMB/8 (out of 50) plus O-Level and Post-UTME components per university
formula; validates JAMB 0–400. Copy promises "UI, UNILAG, OAU, UNIBEN, polytechnics &
screening-only schools" (L8319).

**(b) Flaws.** A frozen table baked into a 1.7 MB theme: when JAMB changes a subject combination
or a university changes its aggregate formula, the only fix is editing and redeploying the
whole theme — and there is no source or date on any formula, so a wrong formula looks as
authoritative as a right one. No cutoff-mark data, no "does my O-Level satisfy this course"
check against actual results (it lists required subjects but never takes the student's
grades), no Post-UTME question bank behind the predictor (repo audit §10.3: no Post-UTME
content exists anywhere), and no link to JAMB CAPS / admission status.

**(c) v2 model.** D1 admission-rules database, admin-editable with `source_url`,
`effective_year`, `verified_at` on every row: `admission_courses(id, course, faculty,
utme_subjects[4], olevel_required[5])`, `aggregate_formulas(id, university, formula JSON,
components, max_score, year)`. The client runs the formula locally from the fetched rule;
the server owns the rules. Add: O-Level result entry (grades per subject) with a real
pass/fail check per course, previous-year cutoff marks (sourced, dated), and an admission
checklist (JAMB registration → Post-UTME → CAPS → acceptance). **Client/server:** client
calculates; D1 stores rules + the student's checklist.

**(d) Out of scope.** Live JAMB CAPS data (no public API — link out, don't fake it); real
cutoff marks presented without a source year; a Post-UTME mock until a question bank exists.

## 5. Flashcards (Leitner 3-box)

**(a) v1.** Route `?p=flashcards` (inventory §1 #10, §5). "3-box Leitner spaced-repetition
algorithm" (template L355–360). User-created decks/cards, review, promote/demote boxes.
No question bank embedded; decks are user-created. State lives inside `MST_APP_DATA`
(no dedicated key, Appendix C).

**(b) Flaws.** Leitner 3-box is the crudest scheduler: no ease factor, no interval growth
beyond box promotion, no lapse handling, no "due today" queue, no stats beyond the session.
Decks are typed by hand — the 4,630 textbook quiz questions and 2,400 vocabulary words
already in the repos are not offered as decks. No images, no cloze deletion, no audio, no
sync, no sharing; a phone wipe deletes every deck.

**(c) v2 model.** Replace Leitner with SM-2 (simple, proven, tiny) with FSRS as a later
upgrade path — same card model, better intervals. Ship ready-made decks generated from
existing data: one deck per Keypoints topic (from textbook `quiz[]`), one per vocabulary
category, one per English-Quiz topic. Add cloze cards, image cards (R2), and a daily due
queue with push reminder. **Data model:** `flashcards_decks(id, user_id, source, title)` +
`flashcards_cards(id, deck_id, front, back, media_url)` + `flashcards_reviews(id, card_id,
ease, interval_days, due_at, lapses)`. **Client/server:** scheduler runs client-side
(offline reviews); D1 syncs decks/reviews so progress survives device loss.

**(d) Out of scope.** Real-time collaborative decks; AI-generated card images (cost/quality);
FSRS parameter fitting per user until review volume justifies it.

## 6. Exam Planner

**(a) v1.** Route `?p=examplanner` (inventory §1 #14). Exam name/date countdowns + "alarms" +
study targets. Storage: `MST_APP_DATA.exams`. Title/meta promise "live countdowns, reminder
alarms and study targets" (L319–323).

**(b) Flaws.** The "alarms" only exist while the page is open — there is no service worker
with a fetch/notification path (repo audit §5: `sw.js` has no fetch handler and no cache
strategy), so an alarm set for an exam in 3 weeks will never fire. No link to the CBT
("practise this exam"), no study targets derived from actual weak topics, no calendar
export, no recurring exams.

**(c) v2 model.** Calendar-backed planner: exams are events with a countdown, a linked CBT
mode/subjects, and reminder offsets (1 week / 1 day / 1 hour). Reminders are delivered by a
scheduled Worker (cron trigger) + Web Push subscription — the Worker, not the browser tab,
owns the alarm. Add ICS export so the exam lands in Google Calendar even without push.
**Data model:** `exams(id, user_id, title, exam_type, date, subjects JSON, reminder_offsets
JSON, target_score)`. **Client/server:** client renders countdowns; Worker cron + push sends
reminders; D1 stores exams.

**(d) Out of scope.** SMS reminders (cost); reminders without the user granting notification
permission; a cron per user (one shared scheduled Worker fans out — free-tier trigger budget
is 5 account-wide, already exhausted per MEMORY.md).

## 7. Study Planner (Pomodoro + Feynman)

**(a) v1.** Route `?p=study` (inventory §1 #16, §5). Pomodoro focus timer (25:00 shown at
L7816, `StudyApp.startPom()` at L7832) + Feynman-style note revision; sessions in
`MST_APP_DATA.studySessions`, notes in `feynman` (Appendix C). Feynman notes export as a
`.txt` download (L16391). Tile copy: "Pomodoro sprints + a Feynman scratchpad" (L8845).

**(b) Flaws.** Fixed 25-minute timer with no custom lengths, no long-break cycle, no
distraction logging, and the timer dies if the tab closes — no background completion. The
"Feynman technique" is just a textarea: nothing checks whether the explanation is correct,
complete, or even on-topic. Sessions are logged but never analysed (no focus-time trends,
no link to what was studied).

**(c) v2 model.** Adaptive focus sessions: configurable focus/break lengths, session intents
linked to a Keypoints topic or CBT subject, and completion recorded server-side so it feeds
Streak/XP honestly. Feynman becomes a real exercise: the student writes an explanation of a
topic, and Workers AI scores it against the Keypoints module text with a rubric
(coverage, correctness, simplicity) and returns gaps to re-study — the AI never writes the
explanation for them. **Data model:** `study_sessions(id, user_id, started_at, minutes,
intent_topic, completed)` + `feynman_attempts(id, user_id, topic_id, text, rubric JSON,
score)`. **Client/server:** timer client-side (with Service Worker + Notification on
completion); Workers AI scores Feynman; D1 stores sessions.

**(d) Out of scope.** Continuous background timing on mobile without the app open (use
notifications, not a fake background timer); AI grading presented as an exam mark.

## 8. Lecture Schedule

**(a) v1.** Route `?p=lecture` (inventory §1 #15). Weekly lecture timetable with
"classroom-style reminders". Storage: `MST_APP_DATA.lectures`.

**(b) Flaws.** A weekly grid with no dates: no semester start/end, no holidays, no cancelled
or rescheduled lectures, no room/lecturer fields worth the name, no clash detection against
the Class Timetable (a separate tool holding the same data), and reminders suffer the same
dead-tab problem as the Exam Planner (§6).

**(c) v2 model.** Merge with §9 into one calendar: recurring weekly lectures with a semester
range, per-occurrence exceptions (cancelled/moved), room + lecturer + course code, and a
"what's next" widget on Home. One source of truth, two views (week grid + agenda). Optional
Google Calendar sync (one-way export first). **Data model:** `schedule_events(id, user_id,
title, course_code, weekday, start_time, end_time, room, lecturer, valid_from, valid_to)`
+ `schedule_exceptions(id, event_id, date, status)`. **Client/server:** client renders;
D1 stores; Worker cron sends "lecture in 30 min" push only if the user opts in.

**(d) Out of scope.** Automatic import from a university portal (no API); two-way Google
Calendar sync in v2.0 (one-way export first).

## 9. Class Timetable

**(a) v1.** Route `?p=timetable` (inventory §1 #17). Weekly class timetable builder,
"printable/shareable" (L374–378). Data in the app blob; no dedicated key.

**(b) Flaws.** Same data as Lecture Schedule, stored separately, with no conflict detection —
two classes can occupy the same slot silently. "Shareable" is a printout/screenshot, not a
link; there is no per-course colour, no free-period detection, no export to calendar.

**(c) v2 model.** Do not rebuild as a separate tool: make it the week-grid view of the §8
calendar, with clash detection (overlapping events highlighted, with a suggested fix),
free-period summary, colour per course, and a shareable read-only link
(`/timetable/<public_id>`) plus ICS export. **Data model:** reuses `schedule_events` (§8);
adds `timetable_shares(id, user_id, public_id, expires_at)`. **Client/server:** client
renders + clash-checks; D1 stores + serves the public link.

**(d) Out of scope.** Collaborative editing of one timetable by a whole class (v2.1 at
earliest); auto-generation from course lists without user input.

## 10. Revision Timetable Generator

**(a) v1.** Route `?p=revision` (inventory §1 #18). "Generates a revision timetable."
No spacing algorithm, interval rule, or generation logic was traced in the inventory;
data in the app blob.

**(b) Flaws.** A generator with no visible algorithm is a black box the student cannot trust
or adjust: it cannot know exam dates (Exam Planner), topic difficulty (CBT/Keypoints
history), or available hours (Study Planner) because none of those tools share data in v1.
The output is a static grid, not a living plan that adapts when a session is missed.

**(c) v2 model.** A real scheduler: inputs are exam dates (§6), topic mastery from CBT/
Keypoints/Flashcard reviews, and daily available hours; the algorithm is spaced repetition
— weakest topics first, interleaved, with review intervals (1d → 3d → 7d → 14d) — and the
plan re-generates when a session is missed or a mock score changes. Every generated slot
links to the material (topic reader / flashcard deck / CBT set). **Data model:**
`revision_plans(id, user_id, exam_id, generated_at, slots JSON)` derived from mastery
views; no new heavy tables. **Client/server:** client computes the plan from server
aggregates; D1 persists the plan.

**(d) Out of scope.** Guaranteeing a grade from following the plan; auto-blocking calendar
time without user confirmation.

## 11. Deadline Planner

**(a) v1.** Route `?p=deadline` (inventory §1 #19). "Deadline tracking/planning."
Bare list in the app blob; no priorities, reminders, or categories traced.

**(b) Flaws.** A list is not a planner: no priority scoring, no effort estimates, no
sub-tasks, no reminders (same dead-tab problem as §6), no distinction between assignment /
project / application / fee deadlines, and no connection to the calendar.

**(c) v2 model.** Priority-scored deadline board: each deadline has a type, effort estimate,
and dependencies; urgency is computed (days left × weight × effort) and the top 3 surface
on Home. Reminders via the same Worker cron + push as §6; ICS export per deadline.
**Data model:** `deadlines(id, user_id, title, type, due_at, effort_hours, weight,
status, subtasks JSON)`. **Client/server:** client boards; D1 stores; Worker cron reminds.

**(d) Out of scope.** SMS reminders; auto-import of deadlines from email or LMS.

## 12. Note Outline Builder

**(a) v1.** Route `?p=outline` (inventory §1 #20). "Builds structured note outlines."
Copy: "Turn rough notes into a clean academic outline with headings, bullets and revision
prompts" (L9534). Data in the app blob.

**(b) Flaws.** The output is only as structured as the input the student types — there is no
parsing, no hierarchy validation, no numbering, no export into Word Office, and no link to
the Keypoints modules the outline is presumably about.

**(c) v2 model.** Outline engine: paste notes (or import a Word Office doc / Keypoints
module) and get a real hierarchy — headings detected and normalised, bullets nested,
numbering applied, revision prompts generated per section — editable as a tree, exportable
to Word Office as a styled document and to PDF. Optional Workers AI pass that suggests
missing sections against the syllabus topic list. **Data model:** `outlines(id, user_id,
title, source_type, tree JSON, updated_at)`. **Client/server:** parsing client-side;
Workers AI suggestion optional, server-side.

**(d) Out of scope.** AI writing the notes themselves (the student writes; the tool
structures); handwriting input.

## 13. Budget Tracker

**(a) v1.** Route `?p=budget` (inventory §1 #21, §5). Monthly ₦ limit + expense log.
Storage: `MST_APP_DATA.budget` `{limit, expenses}` (Appendix C). Title: "log expenses &
limits" (L346–350).

**(b) Flaws.** One limit, one flat list: no categories (food/transport/books/data), no
recurring expenses, no per-category limits, no trends or month comparison, no overspend
warning until the money is gone, no CSV/PDF export, and amounts are plain numbers with no
kobo-safe handling (the LIFEOS brief in MEMORY.md insists money is Long minor units, never
float — this tool does not follow that).

**(c) v2 model.** Envelope budgeting: categories with individual limits, recurring expenses
(auto-posted monthly), running balance per category, month-on-month comparison, and a
simple report (spent by category, top expenses) with CSV export. Money stored as integer
kobo in D1, never float. **Data model:** `budgets(id, user_id, month, limit_kobo)` +
`budget_categories(id, budget_id, name, limit_kobo)` + `expenses(id, user_id, category_id,
amount_kobo, note, spent_at, recurring_rule)`. **Client/server:** client entry + charts;
D1 stores (sync across devices).

**(d) Out of scope.** Bank sync / Open Banking (no Nigerian open-banking integration on the
free tier); lending, savings, or investment features.

## 14. Study Streak & XP

**(a) v1.** Route `?p=streak` (inventory §1 #22, §5). Daily study streak + XP "for
consistency". Storage: `MST_APP_DATA.streak`, plus `MST_TB_STREAK` / `MST_VOCAB_STREAK`
(Keypoints/vocabulary streaks, Appendix C). Achievements row on Profile counts visits
(`MST_VISIT_COUNT`), streak, quizzes taken.

**(b) Flaws.** Self-awarded and device-local: XP is granted by client-side code the user can
edit, the streak is a date check in localStorage, and three separate streak counters
(app / Keypoints / vocabulary) disagree with each other. A streak can be "kept alive" by
opening the page. There is no definition of what counts as studying.

**(c) v2 model.** Server-verified XP: the server awards XP only for real completed events
(a finished CBT/quiz attempt, a completed Pomodoro, a flashcard review session, a Keypoints
module marked done) recorded in D1 — the client reports the event, the server decides the
points. One streak, computed server-side from event dates, with a 1-day grace rule stated
plainly. Opt-in leaderboard (username only, no real names). **Data model:**
`xp_events(id, user_id, kind, points, ref_id, created_at)` + streak derived from
`study_sessions` / quiz attempts; `xp_totals` as a materialised view. **Client/server:**
server-authoritative; client only displays.

**(d) Out of scope.** Prizes or money for XP; public leaderboards with real names; streak
freezes as a paid item in v2.0.

## 15. Word Office

**(a) v1.** Route `?p=word` (inventory §1 #26, §5). TinyMCE 6.8.2 A4 editor
(`tinymce.init`, L14307), templates (blank / resume / report / letter / research paper),
DOCX + PDF export via html-docx-js, jsPDF + html2canvas. Documents in
`MST_APP_DATA.word` `{docs, activeId}` — inside the localStorage blob, so large documents
risk the ~5 MB localStorage quota and there is no version history.

**(b) Flaws.** TinyMCE inside Blogger is heavy and its HTML→DOCX export (html-docx-js) is
lossy: tables, headers/footers, and page numbers degrade. No autosave to anywhere durable,
no versions, no collaboration, no comments, no offline conflict handling, no .docx import
round-trip (mammoth extracts raw text only, formatting lost), and documents die with the
browser.

**(c) v2 model.** TipTap (ProseMirror) editor — lighter, JSON document model, first-class
collaboration later — with real `docx` library export (builds a genuine .docx from the
document JSON, not an HTML conversion) and pdf-lib/jsPDF PDF export from the same model.
Documents stored in D1 (metadata + JSON) with file attachments in R2; autosave with
debounce + version snapshots on every named save. Templates become real starter documents
with styles, not pasted HTML. **Data model:** `documents(id, user_id, title, template,
content JSON, updated_at)` + `document_versions(id, document_id, content JSON, created_at)`.
**Client/server:** editor client-side; D1/R2 persistence; export client-side (docx/pdf-lib).

**(d) Out of scope.** Real-time collaborative editing in v2.0 (data model allows it later);
track-changes / comments in v2.0; rendering pixel-perfect Word pagination (browsers can't).

## 16. PDF Toolkit

**(a) v1.** Route `?p=pdf` (inventory §1 #27, §5). Tabs: merge, split, compress, reorder,
page numbers (`pgnum`), watermark (`wm`), image-to-PDF (`img2pdf`), PDF-to-image (`pdf2img`),
OCR, E-Sign (`sign`), organise. Libraries: pdf-lib 1.17.1 (L698), jsPDF 2.5.1 (L695),
pdf.js 3.11.174 (L9226), Tesseract.js 5.0.4 lazy-loaded (L17065–17068). OCR copy at L7463:
"Extract typed or handwritten text from PDFs and images. First use downloads tesseract.js
(~12 MB)" — the OCR worker is created at L17641 (`Tesseract.createWorker(lang, 1, …)`),
rendering PDF pages to canvas first. E-Sign draws a signature to canvas and downloads a
transparent PNG (L15963).

**(b) Flaws.** Everything runs on the main thread or in unguarded async code: a 50-page PDF
can freeze the tab, there is no file-size or page-count guard, no progress reporting beyond
the OCR progress bar, and "compress" in pdf-lib is mostly re-saving (no real image
downsampling control surfaced). OCR's 12 MB first download plus per-page render is slow on
low-end phones, and "handwritten text" is promised in copy while Tesseract on handwriting
is poor. E-Sign produces a PNG, not a signed PDF — the signature is not embedded into the
document. No history: processed files vanish on refresh.

**(c) v2 model.** Keep the same 10 tools but rebuild the engine: pdf-lib + pdf.js inside a
Web Worker (OffscreenCanvas where available), chunked page processing with progress and
cancellation, explicit guards (e.g. 50 MB / 200 pages per file, stated in the UI), real
compress (downsample embedded images via canvas before re-embedding), and E-Sign that
embeds the signature image into the PDF with pdf-lib at a chosen position. Job history
(file name, tool, pages, size, date) in D1; files themselves are never uploaded — they stay
in the browser and are discarded on close. **Data model:** `pdf_jobs(id, user_id, tool,
filename, pages, size_bytes, created_at)` — metadata only, no file bytes server-side.
**Client/server:** 100% client-side processing in Web Workers; server stores only job
metadata.

**(d) Out of scope (free tier).** Server-side PDF processing (a Worker cannot hold a 50 MB
PDF in memory or spend the CPU); OCR as a server service; handwriting OCR as a promised
feature — Tesseract.js stays, but only for printed English text, labelled honestly.
Heavy OCR (multi-page, multi-language) is OUT: it needs a paid OCR API or a dedicated
service, not the free tier.

## 17. Image Toolkit

**(a) v1.** Route `?p=image` (inventory §1 #28, §5). Tabs: compress (target KB), resize,
convert, batch, watermark, EXIF stripper, QR generator. Implementation is canvas +
`toBlob` (e.g. resize at L15906: `c.toBlob(…, 'image/jpeg', 0.92)`), QR canvas download at
L17386, batch via `ImageApp.batchConvert()` (L7583) and `ImageApp._batch` (L17094). Copy:
"Everything runs offline in your browser" (L7539).

**(b) Flaws.** Main-thread canvas work, one file at a time in practice (batch is a loop over
the same path), no HEIC/AVIF input, no WebP/AVIF output choice surfaced, no dimension or
aspect-ratio lock UI traced, EXIF stripping is all-or-nothing (no "keep orientation, strip
GPS" option), QR codes are plain (no logo/error-correction choice), and there is no
before/after size comparison.

**(c) v2 model.** Worker pipeline: `createImageBitmap` + OffscreenCanvas in a Web Worker,
one worker per file up to a small pool, with per-file progress, before/after sizes, target-KB
binary search on quality, format matrix (JPEG/PNG/WebP/AVIF out; HEIC via a wasm decoder
only if it proves stable, otherwise labelled unsupported), granular EXIF controls (strip
all / keep orientation / strip GPS only — real EXIF parse with `exifr`-style parsing, not a
re-encode guess), and QR with error-correction level + optional logo. **Data model:** no
server data; client-side only, files never leave the device. **Client/server:** 100%
client-side in Web Workers.

**(d) Out of scope.** Server-side image processing or storage (no need — the browser does it
better); HEIC encoding; AI upscaling/enhancement (needs a GPU service, not free tier).

## 18. Word & Character Counter

**(a) v1.** Route `?p=wordcount` (inventory §1 #29). Counts words/characters in pasted text;
title promises "reading time too" (L436).

**(b) Flaws.** Counts only: no readability score, no sentence/paragraph stats, no keyword
density, no reading/speaking time, no target (e.g. "500-word essay"), no handling of pasted
HTML or .docx (the Summarizer already has .txt/.docx/.pdf import — the Counter does not),
and no history.

**(c) v2 model.** Writing-stats panel: words, characters (with/without spaces), sentences,
paragraphs, average sentence length, Flesch Reading Ease + Flesch–Kincaid grade level,
reading time (200 wpm) and speaking time (130 wpm), keyword density top-10, and a word-goal
meter with a target the student sets (essay length). Reuse the Summarizer's file import
(mammoth/pdf.js) so .docx/.pdf can be counted too. **Data model:** client-side only; an
optional `writing_goals(id, user_id, target_words, deadline)` row if goals are saved.
**Client/server:** client-side.

**(d) Out of scope.** Grammar checking (needs a language model or paid API — a basic
Workers AI grammar pass is a v2.1 experiment, not a v2.0 promise); plagiarism checking.

## 19. Citation Generator

**(a) v1.** Route `?p=citation` (inventory §1 #30, §5). Full references; the tile promises
"APA 7, MLA 9 or Harvard" (L8857) and the inventory notes 66 hits for the style names
including Chicago, IEEE, Vancouver. But the actual generator (`gen()`, L9005+) implements
**only three branches** — `apa`, `mla`, and an `else` (Harvard). Chicago, IEEE and
Vancouver are advertised in copy/meta and implemented nowhere (0 hits for "chicago" in the
template). One source type only (author/year/title/publisher/extra); no DOI, ISBN, URL,
journal, or editor handling; "Anonymous" is silently substituted when no author is given.

**(b) Flaws.** The style gap is the headline: a student who picks Chicago gets Harvard output
with no warning. No validation (a 2-digit year passes), no hanging-indent formatting, no
bibliography sorting, no saved references, no import from DOI/ISBN.

**(c) v2 model.** Real CSL engine: `citeproc-js` (or `citation-js`) in the browser with the
official CSL style repository — 9,000+ real styles, so APA 7, MLA 9, Harvard, Chicago
17th (author-date + notes), IEEE and Vancouver are all genuinely implemented. Add
DOI/ISBN/URL lookup (Crossref + Open Library, server-side fetch to avoid CORS, cached in
D1) that auto-fills metadata, multi-source bibliographies with sorting and hanging indent,
and export to .bib / RIS / Word. **Data model:** `references(id, user_id, csl JSON, style,
created_at)`; CSL JSON is the canonical store, styles are render-time. **Client/server:**
CSL rendering client-side; DOI/ISBN lookup via a Worker (cached in D1).

**(d) Out of scope.** A paid citation database; PDF metadata extraction server-side (large
PDF parsing is client-side, §16).

## 20. Quick Cite

**(a) v1.** Route `?p=quickcite` (inventory §1 #31). Inline citations; style select offers
APA 7 / MLA 9 / Harvard only (L9448); copy button writes the citation to clipboard (L9467).

**(b) Flaws.** Same 3-style limit as §19, and it is disconnected from the Citation Generator:
a citation made here cannot be reused there, there is no library, no "cite while you write"
insertion into Word Office, and no page-number / pinpoint support for in-text cites.

**(c) v2 model.** Fold into the reference library: Quick Cite becomes the fast path — pick a
saved reference (or paste a DOI), pick in-text vs narrative form, get `(Achebe, 1958)` or
`Achebe (1958)` with optional page pinpoint, and insert directly into the Word Office
document at the cursor, appending the full reference to the document's bibliography
automatically. **Data model:** reuses `references` (§19) + `document_bibliographies`
derived per document. **Client/server:** client-side; D1 library.

**(d) Out of scope.** Footnote/endnote styles in v2.0 (CSL supports them; UI comes later);
integration with external reference managers (Zotero/Mendeley import is v2.1).

## 21. Note Summarizer

**(a) v1.** Route `?p=summarizer` (inventory §1 #32, §5). Paste notes → short/medium/long
bullet summaries, offline. Implementation is extractive: `summarize(text, n)` (L9153)
ranks sentences (`rank()`) and returns the top n in original order; modes short=3,
medium=5, long=9 bullets; keywords are raw word frequency (`keywords()`, L9161). File
import: .txt, .docx (mammoth 1.6.0, L9225), .pdf (pdf.js text layer, L9226). Needs ≥25
words or it refuses.

**(b) Flaws.** Extractive only: it can only repeat sentences that already exist, so it cannot
simplify, define terms, or produce a paragraph summary — and the "key terms" are just the
most frequent words (stopwords aside), not real key concepts. No length control in words,
no focus ("summarise only the causes"), no save, no link to the Keypoints topic the notes
are about.

**(c) v2 model.** Two-tier: keep the extractive ranker client-side as the instant offline
baseline (it is honest and free), and add an abstractive tier via Workers AI
(Llama 3.1 8B, already proven live on Proseforge per MEMORY.md) — paragraph summary,
bullet summary, and "explain like I'm 15" modes, with a word target and an optional focus
prompt. AI output is labelled as AI-generated and the student can edit it before saving;
summaries save against a topic or document. **Data model:** `summaries(id, user_id,
source_type, source_ref, mode, text, created_at)`. **Client/server:** extractive client;
abstractive via Workers AI (server), with a per-user daily cap to stay in free-tier AI
limits.

**(d) Out of scope.** Summarising scanned/image PDFs (needs OCR first, §16); long-document
summaries over ~8k tokens in one call (chunk + map-reduce is v2.1); guaranteed factual
accuracy of AI summaries.

## 22. Text Compare

**(a) v1.** Route `?p=textcompare` (inventory §1 #33). "Compare two drafts of the same
document side-by-side and see exactly what was added, removed or changed" (L8863). No diff
library or diff algorithm was traced in the template (no Myers/diff-match-patch reference
found); the implementation is a side-by-side view whose comparison logic is not evidenced.

**(b) Flaws.** Whatever the comparison is, it is unverifiable from the template, has no
word-level highlighting evidenced, no similarity percentage, no merge (accept/reject
changes), no export of the diff, and no way to compare a draft against a saved Word Office
version.

**(c) v2 model.** Real word-level diff with `diff-match-patch` (Myers) client-side: additions
green, deletions red strikethrough, unchanged grey; a similarity percentage; side-by-side
and inline views; accept/reject per change; export the merged result to Word Office or
download as .txt/.docx. Compare any two sources: pasted text, two saved documents, or a
document vs an earlier version (§15). **Data model:** client-side only; comparisons are
transient, merged output saves as a document version. **Client/server:** client-side.

**(d) Out of scope.** Plagiarism detection against the web (needs a paid index); semantic
("same meaning, different words") comparison.

## 23. Chart Generator

**(a) v1.** Route `?p=chart` (inventory §1 #47). Data table → Bar, Line, Pie, Doughnut,
Radar; export transparent PNG/JPG/PDF/CSV or embed snippet (inventory §1). Chart.js is
lazy-loaded (L707). Tile copy: "Bar · line · pie · PDF export" (L6223).

**(b) Flaws.** A standalone toy: data is typed by hand into a table, the chart is exported
and forgotten — it cannot pull live data from the student's own Budget, CBT stats, or CGPA
history, there is no saved chart, no chart-as-image insertion into Word Office (the
`WordApp.insertChart()` button at L7365 exists but the generator is a separate page), and
no SVG export (PNG/JPG only, so charts go blurry in print).

**(c) v2 model.** Chart builder with live data binding: pick a source (Budget by category,
CBT scores over time, CGPA by semester, study minutes by week) or paste a table; Chart.js
for standard charts plus ECharts for richer ones; export PNG (2× for print), SVG, PDF,
CSV, and one-click "Insert into Word Office" as an image block. Saved charts persist as
config JSON so they re-render when the underlying data changes. **Data model:**
`charts(id, user_id, title, source_type, source_ref, config JSON, updated_at)`.
**Client/server:** client renders; D1 stores configs; data comes from server aggregates.

**(d) Out of scope.** Real-time collaborative dashboards; server-side chart rendering.

## 24. Dictionary

**(a) v1.** Route `?p=dictionary` (inventory §1 #36; repo audit §4). Word lookup from
`mystudy-dic` per-letter files: `CDN = 'https://cdn.jsdelivr.net/gh/ola1de/mystudy-dic@main/data/'`
(L9911), entry shape `MEANINGS` / `SYNONYMS` / `ANTONYMS` (L9964), `lookup(word)` at
L10026. Tile copy claims "Search 200,000+ English words … and instant native-speaker
pronunciation" (L8864).

**(b) Flaws.** Three falsehoods in the copy: the repo has 121,340 merged entries, not
200,000+ (repo audit §4 — `data/` sums to 158,265 keys only because of case/duplicate
variants); "native-speaker pronunciation" is the browser's `speechSynthesis` TTS
(L9764), not recorded audio; and entries have no IPA, no part-of-speech at top level, and
no examples in most entries, with some entries being bare names ("D. h. lawrence"). Loading
a whole per-letter JSON (several MB for common letters) on every lookup is slow, and there
is no recent-search history persisted server-side, no word-of-the-day, and no "add to
vocabulary" link.

**(c) v2 model.** Server-side dictionary: import `merged.json` (121,340 entries, the canonical
file — not `data/` + `processed/` together) once into D1 with FTS5 full-text search and a
prefix index; the client calls `GET /api/dict?q=` and gets one entry, not a multi-MB file.
Add IPA where the data has it (and say so where it doesn't), real example sentences where
present, and honest TTS labelled "device voice", plus "save to Vocabulary" and recent
lookups. **Data model:** `dictionary_entries(headword PK, pos, definitions JSON, synonyms
JSON, antonyms JSON, ipa)` + `dictionary_lookups(id, user_id, headword, created_at)`.
**Client/server:** server API (D1 FTS); client renders.

**(d) Out of scope.** Recorded native-speaker audio for 121k words (needs a licensed audio
dataset); shipping the 72 MB dictionary to the browser (repo audit §10.4 — import
server-side, never ship all copies to the client).

## 25. Vocabulary

**(a) v1.** Route `?p=vocabulary` (inventory §1 #35; repo audit §8). Word learning with
streaks; 30-question test (`TEST_LEN = 30`, L11160). Data from `vocabulary-database`
(jsDelivr + raw.githubusercontent fallback): 24 categories × 100 words = 2,400 words,
clean uniform shape `{id, word, pos, definition, example}`. Storage:
`MST_VOCAB_HIST` / `MST_VOCAB_LAST_DAY` / `MST_VOCAB_LEARNED` / `MST_VOCAB_STREAK` /
`mst.vocab.v1` (Appendix C). (Tool behaviour only here — the data itself is another
agent's job.)

**(b) Flaws.** The category index is broken: `index.json` lists only 14 of the 24 categories,
so 10 categories (admin-vocabulary, animal-habitats, capability-adjectives, environment,
idioms, natural-phenomena, professions, proverbs, sensory-sounds, umbrella-terms) are
likely unreachable from the category list (repo audit §8). The 30-question test is a fixed
quiz, not adaptive — a word answered correctly 5 times keeps coming back as often as a word
never learned. No sentence-cloze mode, no audio, no link to the Dictionary (§24) or to
Flashcards (§5).

**(c) v2 model.** Adaptive trainer on the same 2,400 words (plus the fixed 24-category index):
each word carries an SRS state (SM-2, shared with Flashcards), the daily session mixes new
words + due reviews + a cloze-sentence round using the `example` field, and TTS pronounces
the word (labelled device voice). Categories are all 24, with per-category mastery bars.
"Add word" lets a student add a Dictionary lookup (§24) into their vocab deck.
**Data model:** `vocab_words(id, word, pos, definition, example, category)` (imported) +
`vocab_progress(id, user_id, word_id, ease, interval_days, due_at, correct, seen)`.
**Client/server:** client trains; D1 stores words + progress.

**(d) Out of scope.** New vocabulary content beyond the 2,400 words in v2.0 (content expansion
is a data task, not a tool task); recorded audio.

## 26. English Quiz

**(a) v1.** Route `?p=english` (inventory §1 #8, §5). 9 categories from
`English-Quiz@main` (L18455): Language Skills, Grammar, Vocabulary, Reading
Comprehension, Writing Skills, Listening Skills, Parts of Speech, Literature, General
English Knowledge. Full: 40 questions, 40 min; free: 5 questions, 10 min
(`Q_COUNT`/`DUR_MIN`, L18467–18470). Same runtime as CBT (tabs, flag, navigator, resume
`MST_EQ_RESUME`, corrections with explanations when present). History capped at 100
attempts (`MST_EQ_HIST`). Repo audit §3: 900 unique questions (9 × 100, all with `exp`),
plus 9 `Old*` duplicate files without explanations.

**(b) Flaws.** The free/premium cap is enforced client-side (same bypass problem as CBT §27).
"Listening Skills" has no audio — it is a text quiz with a listening label. No per-topic
mastery, no weak-area report, no timed exam mode matching a real test, and the 100-attempt
history cap silently drops old attempts.

**(c) v2 model.** Server-gated quiz: the server decides how many questions the user's
entitlement allows and serves the set; the client never sees the cap logic. Per-topic
mastery bars, explanations shown after every question (the data has them — use them), a
listening mode that actually plays TTS audio for the prompt (labelled as device voice,
listening comprehension of a spoken passage), and uncapped history in D1. Drop the `Old*`
files at import; import only the 9 current files. **Data model:** `english_questions(id,
category, question, options JSON, answer_index, explanation, passage_id)` +
`english_attempts(id, user_id, category, score, total, duration_s, created_at)`.
**Client/server:** server serves questions + enforces entitlement; client runs the quiz.

**(d) Out of scope.** Recorded listening audio (TTS only in v2.0); new question content
beyond the 900 (data task).

## 27. CBT (tool-level; main CBT design lives in the architecture doc)

**(a) v1.** Route `?p=cbt` (inventory §1 #7, §2). Timed mocks: JAMB/UTME, WAEC, NECO,
Post-UTME, Primary. Question JSON fetched per subject/year from
`cdn.jsdelivr.net/gh/ola1de/Exam-Questions-Data@main/json/` (L12959) and cached in
localStorage (`MSE_<EXAM>_<file>_<year>`). Free = 5 Qs/subject, premium = 40, hard-coded in
`processQuestions` (L13206–13208). Timer counts down, auto-submits at 00:00 (L13794).
Resume via `MST_CBT_RESUME`. AI Proctor optional: fullscreen, shortcut blocking, 3 strikes
= auto-submit (L13615–13633), webcam via `getUserMedia` with FaceDetector or a skin-tone +
motion fallback. Scoring 1 mark per correct answer, no negative marking; corrections show
explanations only if the JSON carries `exp` (L13744–13753).

**(b) Tool-level flaws (beyond the architecture doc).** (1) The "Questions per subject" input
(`#cbt-count`, value 40, min 5, L6806) is decorative — **no JavaScript reads it**
(inventory §2). (2) Setup copy promises "JAMB → Basic calc. WAEC/NECO → Scientific calc."
(L6788) but only one calculator toggle was traced (`CBT.toggleCalc()`, L13869) — the
scientific calculator is a broken promise. (3) The exam does not enforce JAMB's real format
(120 min / 180 questions); max is 4 subjects × 40 = 160. (4) English is not forced
compulsory in the picker, unlike the combo checker. (5) Premium is client-side and
reversible (§2 licensing table). (6) The bank itself: 190 of 389 files are the 1-question
placeholder "Question Content Here?" (repo audit §2.3) — the picker offers years (e.g. WAEC
2021) that serve that placeholder as a live exam; 11× 2024 science/math files are corrupt
(§2.4); JAMB and Primary have zero explanations (§2.5). (7) The AI Proctor's skin-tone +
motion fallback and speech-band analysis are fragile on low-end devices and can false-
positive a legitimate student.

**(c) v2 model (tool-level).** Server-authoritative CBT: the Worker serves a question set
for the chosen exam/subjects/year from the canonical D1 question model
(`exam, subject, year, topic, type, question, options[4], answer_index, explanation,
passage_id` — repo audit §10.1), enforces the entitlement (Paystack-verified, per the
brief "no cheating, no bypass"), and scores server-side from submitted answer IDs — the
client never holds answers. The Q-count input becomes real (bounded by the entitlement and
the bank size for that subject/year). One real calculator: a basic calculator for all
modes in v2.0, with a proper scientific calculator (client-side, `mathjs`-style expression
parser) as a named v2.1 item — no copy may promise it before it exists. Placeholder years
are never offered: the picker only lists (exam, subject, year) combinations with real
questions. Proctor: keep tab-switch/blur strikes server-logged; webcam proctoring becomes
an explicit opt-in with a plain-language explanation, and the skin-tone fallback is removed.
**Data model:** canonical `questions` + `cbt_attempts(id, user_id, exam, subjects JSON,
score, total, per_subject JSON, duration_s, created_at)` + `cbt_answers(id, attempt_id,
question_id, selected_index, correct)`. **Client/server:** server-authoritative; client is
a renderer + timer.

**(d) Out of scope (free tier).** Real-time video proctoring review (no human review pipeline);
server-side rendering of large question banks per request (serve paginated sets); Post-UTME
mocks until a bank exists (repo audit §10.3); BECE/JSS banks until sourced.

## 28. Study Assistant chatbot

**(a) v1.** No route; floating button. Tries `POST https://bot.mystudysuite.workers.dev/chat/json`
(message + last 12 history + deviceId + name, 20 s timeout), falls back to a local
rule-based answerer (`localAnswer`, L19516) that explains tools, CBT activation and the
Device ID. History in `msa_chat_v4` (last 60 messages). Hidden on CBT/quiz/Word views
(inventory §1, Assistant).

**(b) Flaws.** No retrieval: the bot cannot see the student's data, the Keypoints content, the
syllabus, or the question banks, so it can only chat in generalities or recite tool help.
The local fallback is a handful of canned rules. No memory beyond 60 messages, no actions
(it cannot open a tool, start a quiz, or set a reminder), and the 20 s timeout with no
streaming makes long answers feel dead.

**(c) v2 model.** RAG assistant on Workers AI (Llama 3.1 8B, same as Proseforge's verified
live model): retrieve from D1 — Keypoints modules (FTS), Constitution sections, Dictionary
entries, and the student's own data (next exam, weak topics, due flashcards) — then answer
with citations to the source material. Tool-aware: it can deep-link ("open your CBT
Government 2024 mock") and create a deadline or start a Pomodoro on confirmation.
Streaming responses, conversation history in D1 per user, and a clear "AI can be wrong —
check the source" label. **Data model:** `chat_threads(id, user_id, title)` +
`chat_messages(id, thread_id, role, text, sources JSON, created_at)`; retrieval over
existing FTS indexes (no separate vector DB on the free tier). **Client/server:** server
(Workers AI + D1 retrieval); client renders streamed markdown.

**(d) Out of scope.** A separate vector database / embeddings pipeline on the free tier
(FTS retrieval first; embeddings only if usage justifies a paid tier); the bot writing
essays or doing homework for the student (it explains and quizzes, it does not complete
assignments); voice input in v2.0.

## 29. Legal & Civic Library / Constitution

**(a) v1.** Route `?p=constitution` (inventory §1 #37, §5). Full 1999 Constitution — 8 chapters,
7 schedules — from `nigeria-constitution@main` (`manifest.json`, L15249); searchable,
chapter TOC with filter, sticky sidebar. The hub promises "Constitution, statutes & civic
docs" but only the Constitution viewer is implemented (inventory §5). Repo audit §7: 227
sections (Ch. I: 11, II: 5, III: 7, IV: 11, V: 48, VI: 68, VII: 50, VIII: 27);
`schedules.json` is flat paragraph strings, not structured LGA tables; amendment status is
not stated in the files.

**(b) Flaws.** One document pretending to be a library. No statutes, no civic documents, no
version/amendment note (presenting an undated text "as amended" without saying which
amendments is a legal-accuracy risk), schedules are unsearchable by state/LGA, and there is
no annotation, bookmarking of sections, or "what does this section mean" plain-language
layer.

**(c) v2 model.** Versioned Constitution in D1: `constitution_sections(id, chapter, number,
heading, body JSON, version, source_url, verified_at)` with section-level FTS search and a
plain-language summary field (clearly labelled as explanatory, not law) per section, plus
structured schedules (state → LGAs as rows, not flat text). The "Library" becomes a real
index: Constitution + a sourced list of key statutes/acts with links to the official
source (Federal Ministry of Justice / National Assembly), each row dated and sourced —
added only when the source text is verified, never scraped blindly. Section bookmarks sync
with §31. **Data model:** `constitution_sections` + `constitution_schedules(state, lga)` +
`civic_documents(id, title, type, source_url, verified_at, summary)`. **Client/server:**
server API (D1 FTS); client reader with TOC + search.

**(d) Out of scope.** Presenting the text as current law without verifying amendment status
against the official text (a named verification task, not a tool feature); legal advice;
any statute whose official text cannot be sourced.

## 30. Blog / News reader

**(a) v1.** Routes `?p=blog`, `?p=label`, `?p=post` (inventory §1 #38–40, §4). Posts are
Blogger posts rendered by the real Blog1 widget, then re-rendered by the theme (`inject()`,
L3805–3953; native path L3956+): eyebrow label, Fraunces title, meta row (author falls back
to blank — hence live posts show "Unknown"), featured image extracted from the first image
in the body (L3770–3786), TOC from h2/h3 (≥3 headings, shell path) or h2/h3/h4 (≥2,
Learn Hub path), tags, share bar, Blogger comments. Read time = words ÷ 220 (L3848).
There is **no in-template post editor, no SEO fields per post, no category/tag picker and
no image upload** (inventory §4) — posts are authored in Blogger; the theme only reads
labels. There is no "News" concept — it is a general Blog (inventory §7.6).

**(b) Flaws.** The author shows "Unknown" because the theme reads `post.author.name` and
Blogger leaves it blank; Fraunces is used in post CSS but never loaded (falls back to
Georgia, inventory §7.7); the two TOC implementations disagree (≥3 vs ≥2 headings,
open vs closed); and the admin story is "go to Blogger" — no drafts, scheduling, SEO
editor, or image upload inside MyStudy, which is exactly the admin gap the v2 brief
requires (admin-only News with full SEO editor).

**(c) v2 model.** React admin News module (per the 24 Nov brief): posts in D1 with title,
slug, body (TipTap JSON, shared with §15), excerpt, category, tags, featured image uploaded
to R2, SEO fields (meta title/description, OG image, canonical), status (draft/scheduled/
published), author (the signed-in admin, never blank), and scheduled publish via a Worker
cron. Public reader keeps the loved format — eyebrow, serif title, meta, featured image,
TOC (one implementation, ≥2 headings, closed by default), share bar — rendered from D1,
not Blogger. **Data model:** `posts(id, slug, title, excerpt, body JSON, category_id,
tags JSON, featured_image_url, author_id, seo JSON, status, published_at)` +
`post_categories(id, name, slug)`. **Client/server:** server (D1/R2); React admin + public
reader.

**(d) Out of scope.** Importing the Blogger archive automatically (a migration script, not a
tool feature — and only after the Blogger export is reviewed); comments in v2.0 (moderated
comments are v2.1; v2.0 ships without comments rather than with unmoderated ones).

## 31. Bookmarks

**(a) v1.** Route `?p=bookmarks` (inventory §1 #41). Saved posts/pages in `mst_bookmarks`
(localStorage array, L4014). Post pages wire a bookmark button
(`Bookmarks.wirePostButton`, L3917).

**(b) Flaws.** A flat array with no folders, tags, notes, or search; no sync (bookmarks die
with the browser); only posts/pages can be bookmarked — not a Constitution section, a
Keypoints topic, a vocabulary word, or a CBT question for review.

**(c) v2 model.** Synced bookmark collections: bookmark anything addressable (post, topic,
section, word, question) with a type + ref, organised into folders with tags and an
optional note, plus reading progress on posts. **Data model:** `bookmarks(id, user_id,
kind, ref_id, folder_id, tags JSON, note, created_at)` + `bookmark_folders(id, user_id,
name)`. **Client/server:** client toggles; D1 stores (sync).

**(d) Out of scope.** Offline bookmark sync conflict resolution beyond last-write-wins in
v2.0; sharing collections publicly.

## 32. Profile & Settings

**(a) v1.** Route `?p=profile` (inventory §1 #42, §5). Fields: name, institution, course,
theme (light/dark), accent colour picker, skin (default + "Duolingo" skin, `mst_skin`),
avatar = initials in an accent circle, achievements row, Device ID display + copy, license
box, backup export/import (JSON of all `mst_`/`MST_` keys, licence fields scrubbed),
"Wipe all data" (L8123). **No photo upload, no bio, no email, no password, no social
fields.** Saving a profile silently attempts the admin `/auth` check (name + institution as
credentials, inventory §2) — a backdoor that must not survive the rebuild.

**(b) Flaws.** It is not an account: three text fields in localStorage, no identity, no
recovery, no exam target, no notification preferences (only a boolean
`settings.notifications`). Backup export is a JSON dump the user must keep safe themselves.
The admin `/auth` trigger on profile save is a security smell — admin access must never
depend on matching a display name.

**(c) v2 model.** Real account (per the 24 Nov brief): register/sign-in with compulsory
TOTP (QR auto-generated + manual code copy), 3 dropdown security questions at registration
for password recovery, customisable profile (avatar photo to R2, bio, institution, course,
school level, exam target, notification preferences), and role-based admin (admin flag on
the user row, never inferred from a name). Settings include theme, accent, and per-user
dashboard theme choice (per the WORDLESS pattern the user already approved). Backup becomes
server-side: the account *is* the backup. **Data model:** `users(id, email, password_hash,
totp_secret, security_questions JSON, name, institution, course, exam_target, avatar_url,
theme, accent, role, created_at)` + `user_settings(id, user_id, key, value)`.
**Client/server:** server-authoritative (Rust Worker + D1); TOTP verified server-side.

**(d) Out of scope.** Social login in v2.0 (email + TOTP first; Google sign-in is a later
addition if the user asks); importing the v1 localStorage profile automatically (offer a
one-time import wizard instead — the v1 data has no verified identity).

## 33. Home dashboard

**(a) v1.** Route `?p=home` (inventory §1 #1, §5). Greeting ("Focus. Practice. Graduate
stronger."), date, license pill, countdown to next exam, stat cards, category tiles,
"Latest on MyStudy" blog feed, install/notification prompts. Stats read the local blobs
only (`MST_APP_DATA`, `MST_VISIT_COUNT`).

**(b) Flaws.** Static and local: the countdown reads the Exam Planner blob, the stats read
local history, and nothing on the page knows what the student is weak at, what is due
today, or what to do next. The license pill advertises a premium state that is client-side
and reversible. No personalisation beyond the name.

**(c) v2 model.** Personalised dashboard driven by server aggregates computed nightly (or on
read, cached): next exam + days left, today's due flashcards, weakest 3 topics from CBT/
quiz attempts, current streak, this week's focus minutes, and one recommended action
("Revise Government — 42% on your last mock"). Blog feed from D1 posts (§30). The license
pill becomes a real entitlement state from the server. **Data model:** no new tables —
aggregates over `cbt_attempts`, `english_attempts`, `flashcards_reviews`, `study_sessions`,
`exams`, `posts`. **Client/server:** client renders; server computes aggregates (a
`dashboard_summary` cached per user, refreshed on write + nightly cron).

**(d) Out of scope.** A fully customisable widget layout in v2.0 (fixed sections first, drag-
and-drop later); any "AI predicts your JAMB score" claim.

## 34. Unit Converter (bonus — inventory §1 #46)

**(a) v1.** Route `?p=convert`. Length, mass, temperature, area, volume, time. Factor-table
converter; no storage.

**(b) Flaws.** Six categories only — no currency (₦/$, the one conversion a Nigerian student
actually needs daily), no data (MB/GB), no speed, no pressure, no history of recent
conversions, and no offline factor cache versioning.

**(c) v2 model.** Extended converter: 12+ categories (add currency via a daily rates fetch
cached in D1 with the rate date shown, data storage, speed, pressure, energy, fuel
consumption), recent conversions saved per user, and a factor table bundled with the client
so non-currency conversion works fully offline. **Data model:** `fx_rates(id, pair, rate,
fetched_at)` (server cache) + client-side factor tables. **Client/server:** client converts;
server caches FX rates (one scheduled fetch per day).

**(d) Out of scope.** Live FX rates presented as real-time (daily cached rate, labelled with
its date); crypto rates in v2.0.

---

## Free-tier verdicts (honest list)

| Cannot run on Cloudflare Workers free tier | Why | Where it runs instead |
|---|---|---|
| Heavy / multi-page OCR | 10 ms CPU/request; Tesseract needs seconds–minutes + ~12 MB engine | Client-side Tesseract.js in a Web Worker, printed English only, or OUT |
| Large PDF rendering / processing server-side | Memory + CPU limits; a 50 MB PDF cannot be held per request | Client-side pdf-lib/pdf.js in Web Workers (§16) |
| Video (playback processing, transcoding) | No video pipeline on Workers | Not a MyStudy v2 feature; link to external video |
| Real-time video proctoring review | Needs human review + media storage + streaming | Tab/blur strikes logged server-side; webcam opt-in only (§27) |
| Separate vector DB / embeddings | Cost + a second service | D1 FTS retrieval for the chatbot (§28) |
| SMS reminders | Per-message cost | Web Push + ICS export (§6, §11) |
| Server-side image processing | Unnecessary — browser is faster and free | Client-side canvas workers (§17) |
| AI upscaling / AI image generation | GPU service, not free tier | Out of scope |
| Bank sync / Open Banking | No free Nigerian integration | Manual entry, integer kobo (§13) |
| Live JAMB CAPS data | No public API | Link out (§4) |

## What v1 got right (keep)

- The tool breadth is real: 55 views, and the inventory shows most tools do what their
  tile promises. The rebuild is a re-platform + honesty pass, not a feature cut.
- The design system (v15 "Quiet Confidence", inventory §6) is worth carrying over: primary
  `#5b57e8`, Inter / Plus Jakarta Sans / JetBrains Mono, 8 pt rhythm, 16 px cards.
- The post format (§4) is the format the user loves — keep eyebrow, serif title, featured
  image, TOC, share bar; fix only the author-blank and Fraunces-not-loaded bugs.
- The question banks are the strongest asset (repo audit §12): JAMB 2021–2025 (5,241 real
  Qs), WAEC/NECO 2024–2025, Primary 2026, English-Quiz 900, textbooks 503 modules /
  4,630 quiz Qs — all reusable after schema normalisation, not re-creation.

*Written 24 Nov 2026. Read-only audit — template and repos untouched, nothing pushed.*
