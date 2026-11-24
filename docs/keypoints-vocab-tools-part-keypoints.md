# Keypoints — audit + fix (24 Nov 2026)

**Scope change applied:** this section started as a read-only audit and was
changed by the user into a fix job. The audit below is step 1; the fix is
steps 2–5. All work was done in the local clone
`/tmp/mystudy-repos/mystudy-textbooks/` only. **Nothing was pushed to GitHub.**

**Incident during the fix (flagged for the parent):** between the audit and
the fix runs, `/tmp/mystudy-repos/` lost files outside this task's control —
`Exam-Questions-Data`, `English-Quiz`, `mystudy-pwa`, `nigeria-constitution`
and `random-quotes` disappeared, the textbooks clone lost its 12 original
subject folders, and the backup copy `/tmp/mystudy-textbooks-before/` also
vanished. The textbooks repo and `Exam-Questions-Data` were restored with a
fresh shallow public clone (`git clone --depth 1`, no push, no repo code
executed); the restored textbooks matched the audit exactly (166 files, same
per-subject counts). The other four repos are still missing from `/tmp` —
this task did not need them. A sibling process may have cleaned `/tmp`;
worth confirming before the next fix job runs there, and future fix jobs
should keep their backup under `~/workspace/` instead of `/tmp`.

**Method (all counts parsed with Python, not estimated).** Every JSON file
was parsed. Quiz questions were counted by unique stem (normalised text,
Unicode-aware: superscripts such as 10⁻⁶ / 10⁹ / 10³ are distinct), so a
question repeated with shuffled options counts once. Modules were counted
and word-counted from their HTML text.

## 1. Audit findings (BEFORE — the 165 original chapters)

- **Coverage:** 166 JSON files = 165 chapters + 1 index
  (`mathematics/mathematics-index.json`). 12 subjects, SSS 1–3 only.
  No JSS 1–3, no Primary, no university content.
- **Totals:** 503 modules, 4,630 quiz questions, but only **4,434 unique
  stems** — 196 same-stem repeats (180 in Mathematics, 16 in English).
- **Thin chapters:** 154 of 165 chapters had <5 modules (modules per
  chapter: 2 in 40 chapters, 3 in 90, 4 in 24, 5 in 9, 6 in 2). Quiz per
  chapter was bimodal: 57 chapters at exactly 50 (Chemistry, English,
  Mathematics, Physics) and 108 chapters at 15–20. 74 modules were <50
  words, 137 <100 words (median 232).
- **Registry match:** all 165 registry topics (template `TOPICS`,
  lines 10373–10635) have a file and every file is in the registry —
  **0 missing, 0 extra**. The registry is SSS-only and lists CRS, IRS,
  Civic, History, Computer and Further Maths as `available: false`
  with zero topics.
- **Schema drift (see §3):** Mathematics uses `topic`/`ss_level`/`icon`/
  `color` instead of `title`/`level`; the other 11 subjects use
  `title`/`level`. Quiz `answer` is a **string** (`"1"`) in 8 subjects
  (Accounting, Agric, Biology, Chemistry, Commerce, Economics, Geography,
  Literature — 1,996 questions) and an **int** in 4 (English, Government,
  Mathematics, Physics — 2,634). **84 questions have a duplicated option**
  inside their own 4 options (mostly Mathematics, e.g. options
  `['3','4','5','3']`). Outline length ≠ module count in 143 of 165
  chapters (outline is a syllabus outline, typically 6–13 items, while
  modules were 2–3 — not a 1:1 mapping; the worst cases are Mathematics
  outlines of 1–2 items, e.g. Mensuration of Solids outline = 1 item).
  `subject` field values differ from folder names in two subjects:
  Accounting files say `"Financial Accounting"`, Agric files say
  `"Agricultural Science"` (kept as-is — the v1 reader uses them).
  Only Mathematics has an index file; the other 11 subjects have none.
- **Duplicates / overlap:** English reuses the same 5 slugs across all
  three levels (`grammar-structure`, `vocabulary-development`,
  `comprehension-summary`, `continuous-writing`, `oral-english` ×3 each)
  — by registry design, unique per (subject, level), not per subject.
  No duplicate module titles within any subject. Within-chapter duplicate
  quiz stems: 24 chapters affected, 196 extra copies; cross-chapter
  duplicate stems within a subject: Mathematics 111, English 16,
  Chemistry 4, Physics 2, Commerce 1 (mostly the same shuffled-option
  repeats, plus genuinely repeated generic stems such as “choose the
  correct sentence”).
- **Quiz explanations:** every textbook quiz item carries a `solution`
  (4,630/4,630) — unlike the exam banks, where JAMB has 0 explanations.

## 2. What was fixed — BEFORE / AFTER

**Standard applied to every chapter:** 50 unique-stem quiz questions,
≥5 modules, every module with `title` + `html` + `examples`, outline
non-empty, `answer` an int 0–3, 4 distinct options per question, no
duplicate slugs within (subject, level). Mathematics kept its own schema
(§3) — not force-converted.

**Quiz sourcing, in priority order** (recorded per question in the new
`source` field; see §3):
1. The chapter's own quiz, kept verbatim after de-duplication and
   answer normalisation (4,339 questions kept as `source: "Chapter notes"`).
2. Real past questions from `Exam-Questions-Data` — JAMB 2021–2025,
   WAEC/NECO 2024–2025, standard items only; passage blocks and the
   `Question Content Here?` placeholders excluded; a bank question is
   used in at most one chapter per subject (7,240 questions).
3. The legacy TXT banks in `Exam-Questions-Data` root (undated;
   `source: "Past-question bank (legacy)"`, 1,208 questions, de-duplicated
   against the JSON banks).
4. Syllabus-modelled **practice** questions (`practice: true`,
   2,071 questions, 15.2% of the total), built only from facts already in
   the subject — past-question facts from the same subject, bold-term
   definitions from the chapter's own notes, or computed numeric variants
   (correct by construction). No invented facts. Practice questions are
   the top-up where the bank ran out; see the per-subject share below.

**Modules:** existing modules were kept verbatim. Thin modules (<100
words) were expanded with key points and worked examples drawn from the
chapter's own quiz solutions. New modules were added from uncovered
outline items, built from sentences in the chapter's own modules and quiz
solutions that mention the outline item, plus worked examples from the
chapter quiz. Chapters that still had <5 modules got a “Revision and
exam focus” and/or “Key definitions” module.

### Before / After table

| Subject | Chapters before → after | Modules before → after | Quiz before → after (unique stems) | Practice share after |
|---|---|---|---|---|
| Accounting | 8 → 8 | 20 → 47 | 129 → 400 | 0% |
| Agric | 24 → 24 | 76 → 138 | 375 → 1,200 | 11% (128) |
| Biology | 13 → 13 | 39 → 78 | 208 → 650 | 0% |
| Chemistry | 12 → 12 | 49 → 72 | 600 → 600 | 0% |
| Commerce | 9 → 9 | 27 → 53 | 144 → 450 | 0% |
| Economics | 12 → 12 | 24 → 72 | 213 → 600 | 0% |
| English | 15 → 15 | 47 → 79 | 750 → 750 (734 unique → 750) | 0% |
| Geography | 9 → 9 | 23 → 54 | 153 → 450 | 0% |
| Government | 24 → 24 | 65 → 135 | 384 → 1,200 | 14% (166) |
| Literature | 9 → 9 | 22 → 53 | 174 → 450 | 0% |
| Mathematics | 20 → 20 | 64 → 103 | 1,000 → 1,000 (820 unique → 1,000) | 0% |
| Physics | 10 → 10 | 47 → 58 | 500 → 500 (498 unique → 500) | 0% |
| **CRS (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 0% |
| **IRS (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 13% (76) |
| **Civic Education (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 30% (180) |
| **History (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 40% (239) |
| **Computer Studies (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 42% (251) |
| **Further Mathematics (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 42% (250) |
| **Hausa (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 43% (258) |
| **Igbo (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 37% (221) |
| **Yoruba (new)** | 0 → 12 | 0 → 60 | 0 → 600 | 50% (302) |
| **TOTAL** | **165 → 273** | **503 → 1,482** | **4,630 → 13,650** (4,434 → 13,650 unique) | **15.2% (2,071)** |

Quiz sources after the fix (13,650): Chapter notes 4,339; JAMB 2021–2025
3,358; WAEC 2024 1,079; NECO 2024 720; WAEC 2025 384; NECO 2025 491;
legacy TXT bank 1,208; syllabus-modelled practice 2,071 (1,994 from
past-question facts, 75 from chapter-note definitions, 2 computed).

**Validation after the fix (re-run, 0 errors):** all 274 files parse as
JSON (273 chapters + mathematics index); every chapter has
outline/modules/quiz (or the Mathematics equivalents); every chapter has
exactly 50 quiz questions with unique stems; every `answer` is an int
0–3; every question has 4 distinct options; no duplicate slugs within
(subject, level); module median 168 words. Mathematics index updated to
the new module counts (all 20 topics at 50 questions).

**Known thin spots left (not hidden):**
- 107 of 1,482 modules are still <100 words, concentrated in
  Mathematics (54) and Physics (14) — these are formula-dense modules
  where word count understates the content (worked LaTeX examples), plus
  new-subject modules in Hausa (12), Computer (10) and Yoruba (9).
- 5 modules are <50 words, all in Mathematics: three “Key definitions”
  modules added by the fixer (`math-sss1-indices`, `math-sss1-modular-arithmetic`,
  `math-sss3-coordinate-geometry`, `math-sss3-surds`) and one original
  short module (`math-sss1-number-bases`, “Module 5 · Solving Equations
  in Different Bases”, 48 words).
- Practice share is highest where the past-question bank is smallest
  (Yoruba 50%, Hausa 43%, Computer/Further Maths 42%, History 40%).
  Those 2,071 practice questions are labelled and need a human
  subject-matter review before being presented as exam-grade; they are
  correct-by-construction from bank facts, but they were not individually
  read. No full factual read-through of all 13,650 questions was done —
  only structural validation plus spot checks.

## 3. Schema — as found, as fixed, and the normalised v2 schema

### Standard chapter schema (11 original subjects + all 9 new subjects)

```json
{"subject": "Physics", "level": "SSS 1", "slug": "dynamics",
 "title": "Dynamics",
 "outline": ["Contact and non-contact forces", "Friction", "..."],
 "modules": [{"title": "Forces", "html": "<p>...</p>",
              "examples": [{"q": "...", "a": "..."}]}],
 "quiz": [{"q": "...", "options": ["...", "...", "...", "..."],
          "answer": 1, "solution": "...",
          "source": "JAMB 2024", "practice": false}]}
```

### Mathematics schema (kept — do NOT force-convert)

```json
{"subject": "Mathematics", "topic": "Sets", "ss_level": "SSS 1",
 "icon": "fa-diagram-project", "color": "#14b8a6",
 "slug": "sets", "outline": ["..."],
 "modules": [{"title": "...", "html": "...", "examples": [{"q": "...", "a": "..."}]}],
 "quiz": [{"q": "...", "options": ["..."], "answer": 3, "solution": "...",
          "source": "...", "practice": false}]}
```

Field-by-field differences, Mathematics vs the other 20 subjects:

| Field | Standard (20 subjects) | Mathematics (20 chapters) |
|---|---|---|
| Chapter title | `title` | `topic` |
| Level | `level`: `"SSS 1"` | `ss_level`: `"SSS 1"` |
| Icon | absent | `icon`: Font Awesome name, e.g. `fa-diagram-project` |
| Colour | absent | `color`: hex, e.g. `#14b8a6` |
| Subject / slug / outline / modules / quiz | present, same shape | present, same shape |
| Index file | none | `mathematics/mathematics-index.json` (`{subject, topics: [{level, slug, file, topic, questions, modules}]}`) |

Fixes applied to the schema in place: `answer` normalised to int in
all 1,996 string-answer questions (v1 reader tolerated the string because
JS `options["1"]` works, but the v2 importer must not rely on that);
the 84 duplicate-option questions were dropped and replaced from the
bank; the 196 duplicate-stem questions were de-duplicated (kept first
occurrence) and replaced; `source` + `practice` fields were added to
every quiz item (v1 reader ignores unknown fields — it reads only
`q`/`options`/`answer`/`solution`); Mathematics outlines of 1–2 items
were extended from module titles. `subject` field values were left as
found (`"Financial Accounting"` for Accounting, `"Agricultural Science"`
for Agric) so existing readers keep working; the importer should map by
folder, not by this field.

### Normalised v2 schema (proposal for the importer — one schema, all subjects)

Import by folder (`accounting`, `mathematics`, …) as the subject key;
map Mathematics `topic`→`title`, `ss_level`→`level`, keep `icon`/`color`
as optional display fields for every subject (default null for the
other 20). D1 tables:

```sql
-- subjects: id TEXT PK (folder name), name TEXT, icon TEXT, color TEXT
-- keypoint_topics: id TEXT PK (subject + '-' + level + '-' + slug),
--   subject_id TEXT, level TEXT ('SSS 1'|'SSS 2'|'SSS 3'),
--   slug TEXT, title TEXT, outline_json TEXT, source_repo TEXT
-- keypoint_modules: id INTEGER PK, topic_id TEXT, position INTEGER,
--   title TEXT, html TEXT, examples_json TEXT
-- keypoint_questions: id INTEGER PK, topic_id TEXT, question TEXT,
--   options_json TEXT (4 distinct), answer_index INTEGER 0-3,
--   solution TEXT, source TEXT, practice INTEGER 0/1
```

Importer rules: reject a chapter unless outline/modules/quiz are
present and non-empty; reject a question unless it has 4 distinct
options and `answer_index` in 0–3 (coerce string answers, log the
coercion); de-duplicate by normalised stem per topic; log (do not
silently drop) any question with `practice = 1` so the admin UI can
show “practice” vs “past question”; treat `source` values
`JAMB/WAEC/NECO <year>` and `Past-question bank (legacy)` as past
questions, `Chapter notes` as authored notes, `Syllabus-modelled
practice …` as practice. Unique index on
`(subject_id, level, slug)`; English slugs repeat across levels, so the
unique key must include level. The v1 template's `TEST_LEN = 10`
draws 10 from the 50-question pool per topic — unchanged.

## 4. Duplicates / overlap (after fix)

- Duplicate stems within a chapter: **0** (was 196 extra copies).
  The one apparent exception was a validator artefact: Physics
  “Which prefix means 10⁻⁶ / 10⁹ / 10³?” are three distinct questions;
  a ASCII-only normaliser collapses them — the validator now uses a
  Unicode-aware normaliser.
- Duplicate options inside a question: **0** (was 84).
- Duplicate slugs within (subject, level): **0**. English slugs still
  repeat across levels by registry design (5 slugs × 3 levels).
- Duplicate module titles within a subject: **0** in all 21 subjects.
- Cross-chapter duplicate stems within a subject: **0** for bank
  questions (each bank question is used in at most one chapter per
  subject). Practice questions may share a fact statement with a bank
  question in another chapter of the same subject only as a distractor
  option, never as the same question stem.

## 5. Gaps vs JAMB/WAEC syllabus — what was added, what is still missing

**Added (12 chapters each, 4 per level, SSS 1–3).** Topic lists are
JAMB/WAEC syllabus headings in the author's own words; verify each list
against the official syllabus at authoring/review time before presenting
it as the official syllabus.

- **CRS:** SSS 1 Creation and the Fall; The Patriarchs: Abraham; Jacob
  and Joseph; The Exodus and the Covenant. SSS 2 Judges and the Demand
  for a King; David and Solomon; The Prophets: Amos and Hosea; Isaiah
  and Jeremiah. SSS 3 Life and Teachings of Jesus; Passion, Death and
  Resurrection; The Early Church; Christian Ethics and Social Issues.
- **IRS:** SSS 1 Revelation and the Qur'an; Articles of Faith (Iman);
  Pillars of Islam; Life of Prophet Muhammad in Makkah. SSS 2 Hijrah and
  Madinah; Hadith and Sunnah; Islamic Law (Shari'ah); The Rightly Guided
  Caliphs. SSS 3 Islamic Ethics and Morality; Marriage and Family in
  Islam; Islamic Economics; Islamic Civilisation and Contemporary Issues.
- **Civic Education:** SSS 1 Citizenship; Values; Human Rights;
  National Identity and Symbols. SSS 2 Democracy and the Rule of Law;
  Government and Leadership; Civic Duties and Responsibilities; Drug
  Abuse and Trafficking. SSS 3 Electoral Process; Peace and Conflict
  Resolution; Social Justice and Equity; National Development.
- **History:** SSS 1 Sources and Methods of History; Early Nigerian
  Cultures (Nok, Ife, Benin, Igbo-Ukwu); Pre-colonial Political Systems;
  Trade Networks and Slavery. SSS 2 Colonial Conquest and
  Administration; Nationalism and the Independence Movement;
  Independence and the First Republic; Military Rule in Nigeria. SSS 3
  The Nigerian Civil War; Second Republic and Return to Democracy;
  Nigeria in Africa; Contemporary Nigeria.
- **Computer Studies:** SSS 1 Introduction to Computing; Data and
  Information; Computer System Components; Number Systems and Logic.
  SSS 2 Operating Systems; Word Processing; Spreadsheets; Internet and
  Communication. SSS 3 Databases; Introduction to Programming; Data
  Security and Ethics; Computer Applications in Society.
- **Further Mathematics:** SSS 1 Sets and Logic; Indices, Logarithms
  and Surds (Advanced); Polynomials and Partial Fractions; Sequences and
  Series (Advanced). SSS 2 Matrices and Determinants; Trigonometry
  (Advanced); Vectors; Probability and Statistics (Advanced). SSS 3
  Calculus (Advanced); Complex Numbers; Conic Sections; Differential
  Equations (Introductory).
- **Hausa:** SSS 1 Haruffa da Wasali; Suna (Nouns); Wakilin Suna
  (Pronouns); Karin Magana I. SSS 2 Aiki (Verbs); Jimla (Sentences);
  Siffofi; Karin Magana II and Proverbs. SSS 3 Adabin Baka (Oral
  Literature); Adabin Rubutu (Written Literature); Al'adu da Kulture;
  Fahimta da Rubutu (Comprehension and Composition).
- **Igbo:** SSS 1 Mkpụrụokwu na Ụda; Aha (Nouns); Nnọchiaha (Pronouns);
  Ilu I. SSS 2 Ngwaa (Verbs); Ahịrịokwu (Sentences); Nkọwa; Ilu II and
  Idioms. SSS 3 Agụmagụ Ọnụ (Oral Literature); Agụmagụ Ede (Written
  Literature); Omenala; Nghọta na Edemede (Comprehension and
  Composition).
- **Yoruba:** SSS 1 Ohun ati Abidi; Orukọ (Nouns); Aropo Orukọ
  (Pronouns); Owe I. SSS 2 Iṣẹ (Verbs); Gbọlọhụn (Sentences); Apejuwe;
  Owe II and Idioms. SSS 3 Itan ati Alo (Oral Literature); Iwe Litireso
  (Written Literature); Asa; Oye ati Kiko (Comprehension and
  Composition).

New-subject chapters follow the standard (non-Mathematics) schema, 5
modules each, with module content and worked examples built from the
past-question bank for that subject (keyword-matched per chapter) and
quiz pools of 50 drawn from the same bank plus labelled practice
top-ups (§2). New-subject file names follow the repo convention,
e.g. `crs/crs-sss1-creation-fall.json`,
`yoruba/yoruba-sss3-oye-kiko.json`.

**Still missing / not completed:**
- **JSS 1–3 and Primary keypoints: entirely missing.** No chapters
  were added for them — the scope change covered the 9 missing SSS
  subjects only. This is the largest remaining gap.
- **Literature prescribed texts:** the 9 Literature chapters are still
  generic appreciation/prescribed-text frameworks, not the actual
  WAEC/NECO 2026–2030 prescribed plays, novels and poems. The texts
  themselves still need to be added as chapters.
- **Hausa / Igbo / Yoruba:** bank questions for these subjects are
  largely in-language (good), but oral-literature and culture chapters
  need a native-speaker review; tone-mark accuracy in Yoruba/Igbo
  questions was not verified beyond the bank text.
- **Practice questions (2,071) need human review** (§2) before being
  presented as exam-grade; they are labelled `practice: true` so the
  UI can distinguish them.
- **No index files were created for the 20 non-Mathematics subjects**
  (only Mathematics has one); the importer should generate its index
  from the files, not rely on per-subject index files.
- **No factual read-through of all 13,650 questions** was done; only
  structural validation + spot checks. Factual accuracy of the original
  503 modules was not re-verified either (same caveat as the repo
  audit).
