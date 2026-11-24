# MyStudy repo audit — 24 Nov 2026

**Scope:** the 8 public repos under `ola1de` referenced in the Blogger template
`~/workspace/user/files/theme-5334759134063131007__8__0_xo41.xml` (1.7 MB, 24,438 lines).
Template mentions: Exam-Questions-Data ×1, English-Quiz ×1, mystudy-dic ×1,
mystudy-pwa ×1, mystudy-textbooks ×1, nigeria-constitution ×1,
vocabulary-database ×2, random-quotes ×1. All are loaded at runtime from
jsDelivr (`cdn.jsdelivr.net/gh/ola1de/<repo>@main/…`), except vocabulary-database
and random-quotes, which the template fetches from `raw.githubusercontent.com`.

**Method:** shallow `git clone --depth 1` of each repo into `/tmp/mystudy-repos/<name>`
on 24 Nov 2026. No push, commit, or change was made on GitHub. No repo code was
executed — no `.py`/`.js`/workflow in the repos was run. Counts were produced by
my own read-only parser scripts (`/tmp/audit.py`, `/tmp/audit2.py`) that only
parsed JSON/TXT data files. "Expanded" question counts unpack passage blocks:
a `{"type":"passage","content":…,"questions":[…]}` block counts as its inner
questions, not as 1. "Blocks" = top-level array length.

**Headline:** the data is much better than the live site suggests, but it is
uneven. JAMB is the only exam with 5 usable years. WAEC/NECO are effectively
2-year banks (2024–2025), and 11 of their 2024 science/math files are corrupt.
190 of 389 exam files are 1-question placeholders. There are **no** topic,
year, subject or exam fields inside any question file — that metadata lives
only in the filename. JAMB and Primary have **zero** explanations.

---

## 1. Summary table

| Repo | Exists? | Default branch | Non-git files | Non-git size | Format | What it holds |
|---|---|---|---|---|---|---|
| Exam-Questions-Data | Yes | `main` | 404 (389 JSON + 14 TXT + 1 README) | 2.5 MB | JSON + TXT | JAMB/WAEC/NECO/Primary question banks |
| English-Quiz | Yes | `main` | 18 JSON | 541 KB | JSON | English quiz, 9 topics, current + `Old*` duplicates |
| mystudy-dic | Yes | `main` | 34 (26 data JSON + 2 processed JSON + 3 PY + README + LICENSE + workflow) | 71.8 MB | JSON | English dictionary, ~121k headwords (merged) |
| mystudy-pwa | Yes | `main` | 1 (`sw.js`) | 1.6 KB | JS | Service worker only — no manifest, no app code |
| mystudy-textbooks | Yes | `main` | 166 JSON | 2.7 MB | JSON | SSS 1–3 textbooks, 12 subjects, 503 modules, 4,630 quiz Qs |
| nigeria-constitution | Yes | `main` | 11 JSON | 523 KB | JSON | 1999 Constitution, Ch. I–VIII (227 sections) + preamble + schedules |
| vocabulary-database | Yes | `main` | 25 JSON (24 data + index) | 1.3 MB | JSON | 24 vocab categories × 100 words = 2,400 words |
| random-quotes | Yes | `main` | 1 (`Quotes.txt`) | 24 KB | TXT | 271 quotes |

Total across all 8 repos (non-git): ~653 files, ~79 MB, of which mystudy-dic
alone is ~72 MB (91%).

---

## 2. Exam-Questions-Data — the question bank

### 2.1 Layout

- Root: 14 plain-text banks, one per subject (see §2.5).
- `json/`: 389 files, named `<EXAM>_<Subject>_<Year>.json`, plus an empty
  `json/README.md` (1 byte, no content).
- Exams present: JAMB, WAEC, NECO (each 21 subjects × 2020–2025 = 126 files),
  plus PRI (Primary, 11 subjects × 2026 only = 11 files). **No file is missing
  from the grid** — every expected `<exam>_<subject>_<year>` file exists.
- Subjects in the grid (21): Accounting, Agric, Biology, CRS, Chemistry,
  Civic, Commerce, Computer, Economics, English, FurtherMath, Geography,
  Government, Hausa, History, IRS, Igbo, Literature, Mathematics, Physics,
  Yoruba.
- That covers all 14 subjects the task lists (English, Maths, Physics,
  Chemistry, Biology, Economics, Government, Literature, CRS/IRS, Geography,
  Commerce, Accounting, Agric, Further Maths) — plus Civic, Computer, Hausa,
  History, Igbo, Yoruba.

### 2.2 How many questions? (counted, expanded)

| Exam | Files | Blocks (top-level entries) | Expanded questions (passages unpacked) | Real questions* |
|---|---|---|---|---|
| JAMB | 126 | 5,194 | 5,263 | 5,241 |
| WAEC | 126 | 2,505 | 2,546 | 2,462 |
| NECO | 126 | 2,301 | 2,348 | 2,264 |
| PRI (Primary 2026) | 11 | 552 | 560 | 560 |
| **Total parseable** | **389** | **10,552** | **10,707** | **10,527** |

\* "Real" = expanded minus the 1-question placeholder files (see §2.3).
The 11 corrupt files (§2.4) are excluded from every count above — their
contents are unreadable, so the true total if they were repaired would be
roughly 700 higher.

Per-subject expanded totals (parseable files only):

| Subject | JAMB | WAEC | NECO | PRI |
|---|---|---|---|---|
| Accounting | 261 | 134 | 137 | — |
| Agric | 251 | 134 | 134 | 50 |
| Biology | 251 | 134 | 134 | — |
| CRS | 251 | 134 | 134 | — |
| Chemistry | 251 | 64 | 64 | — |
| Civic | 251 | 134 | 136 | 50 |
| Commerce | 261 | 134 | 134 | — |
| Computer | 251 | 134 | 64 | 50 |
| Economics | 251 | 134 | 134 | — |
| English | 260 | 146 | 139 | 60 |
| FurtherMath | 251 | 64 | 64 | — |
| Geography | 251 | 64 | 64 | — |
| Government | 251 | 134 | 134 | — |
| Hausa | 202 | 135 | 139 | — |
| History | 251 | 134 | 75 | — |
| IRS | 251 | 135 | 135 | — |
| Igbo | 262 | 134 | 136 | — |
| Literature | 252 | 132 | 131 | — |
| Mathematics | 251 | 134 | 64 | 50 (as "Math") |
| Physics | 251 | 64 | 64 | — |
| Yoruba | 251 | 132 | 124 | — |
| CurrentAffairs / Quant / Science / Social / Verbal / Vocational | — | — | — | 50 each |

### 2.3 Years — the placeholder problem

**190 of the 389 JSON files (49%) are 1-question placeholders**, all identical:

```json
[{"type":"std","q":"Question Content Here?","opts":["Option A","Option B","Option C","Option D"],"ans":0}]
```

Breakdown of placeholders:

- **JAMB: 22 files** — all 21 subjects for **2020**, plus Hausa 2023.
  JAMB 2021–2025 is real: mostly 50 questions per subject-year (Accounting
  and Commerce 2021 have 60; English/Literature/Igbo vary 38–61 blocks because
  of passage blocks).
- **WAEC: 84 files** — all 21 subjects for **2020, 2021, 2022, 2023**.
  Only 2024 (60–71 questions, with explanations) and 2025 (50–60, no
  explanations) are real — and 4 of the 2024 files are corrupt (§2.4).
- **NECO: 84 files** — all 21 subjects for **2020–2023**, same pattern as WAEC.
  Only 2024 (60–71, with explanations) and 2025 (50–60) are real — and 7 of
  the 2024/2025 files are corrupt.
- **PRI: 0 placeholders** — all 11 Primary 2026 files are real (50 each,
  English 60 with passages).

So in practice: **JAMB = 5 usable years (2021–2025); WAEC/NECO = 2 usable
years (2024–2025); nothing before 2020, nothing for 2026, no Post-UTME,
no BECE/JSS, no university-level bank.** A CBT that offers "JAMB 2020" or
"WAEC 2021" today serves the placeholder question.

### 2.4 Corrupt files — 11 JSON files fail to parse

| File | Error |
|---|---|
| NECO_Chemistry_2024.json | Invalid control character, line 9 col 29 |
| NECO_Computer_2024.json | Invalid control character, line 76 col 17 |
| NECO_FurtherMath_2024.json | Invalid control character, line 3 col 10 |
| NECO_Geography_2024.json | Invalid control character, line 210 col 33 |
| NECO_History_2025.json | Expecting `,` delimiter, line 94 col 14 |
| NECO_Mathematics_2024.json | Invalid control character, line 3 col 16 |
| NECO_Physics_2024.json | Invalid control character, line 6 col 43 |
| WAEC_Chemistry_2024.json | Invalid control character, line 14 col 18 |
| WAEC_FurtherMath_2024.json | Invalid control character, line 3 col 26 |
| WAEC_Geography_2024.json | Invalid control character, line 25 col 46 |
| WAEC_Physics_2024.json | Invalid control character, line 10 col 11 |

Pattern: 10 of 11 are 2024 files, and 8 of 11 are science/math subjects
(Chemistry, Computer, FurtherMath, Geography, Mathematics, Physics). Effect:
**WAEC/NECO 2024 is unreadable for Chemistry, FurtherMath, Geography and
Physics** (plus NECO Computer, NECO Mathematics), leaving only 2025 for those
subjects. All other 378 JSON files parse cleanly. No empty (0-byte) files were
found. All parsed questions validated: `ans` is always an `int` in range and
every question has exactly 4 options (10,707/10,707 checked).

### 2.5 Question structure — three incompatible schemas, no metadata

Schema A — standard question (the majority):

```json
{"type":"std","q":"Convert 231_4 to base 10.","opts":["45","46","47","48"],"ans":0}
```

Schema B — passage block (English, Literature, Igbo, and PRI English;
`content` is HTML, `questions` are Schema-A items without `type`):

```json
{"type":"passage","content":"<h3>Passage: The Impact of Social Media</h3><p>…</p>",
 "questions":[{"q":"…","opts":[…],"ans":1}]}
```

Schema C — 2024 WAEC/NECO only (no `type` field, adds `explanation`):

```json
{"q":"The basic unit of classification of living things is the _____.",
 "opts":["Genus","Species","Phylum","Kingdom"],"ans":1,
 "explanation":"Species is the lowest and most basic unit of classification…"}
```

Fields that exist **nowhere** in any question file: `topic`, `year`, `subject`,
`exam`, `id`, `difficulty`, `marks`, `source`. The only metadata is the
filename. Explanation coverage: **JAMB 0/5,263 (0%), PRI 0/560 (0%),
WAEC 1,203/2,546 (47.3%), NECO 999/2,348 (42.7%)** — i.e. only the 2024
WAEC/NECO files carry explanations.

### 2.6 The 14 root `.txt` banks (legacy / duplicate?)

Format: `Question: …` / `A) …` `B) …` `C) …` `D) …` / `Answer: C`, no year,
no explanations, no topic. Counts by `Question:` occurrences:

| File | Questions | | File | Questions |
|---|---|---|---|---|
| Accounting.txt | 250 | | English Language.txt | 250 |
| Agricultural Science.txt | 250 | | Geography.txt | 250 |
| Biology.txt | 137 | | Government.txt | 251 |
| Chemistry.txt | 250 | | Islamic Religious Knowledge (IRK).txt | 112 |
| Christian Religious Knowledge (CRK).txt | 250 | | Literature-in-English.txt | 190 |
| Commerce.txt | 250 | | Mathematics.txt | 51 |
| Economics.txt | 250 | | Physics.txt | 39 |

Total ≈ 2,780. Five files are clearly truncated vs the 250-question pattern
(Biology 137, IRK 112, Literature 190, Mathematics 51, Physics 39), and
Physics mixes `A.` and `A)` option markers and contains a visibly broken
option (`C)  m/s` — missing value). No evidence in the files themselves that
these TXT banks are the same questions as the JSON banks or different ones;
they must be de-duplicated against the JSON before any import, not blindly
added. The template was not observed (in the grep pass) loading these TXT
files — the CBT loads the `json/` files.

---

## 3. English-Quiz

18 JSON files, 568 KB total (non-git 541 KB). 9 current files + 9 `Old*` files.

| File (current) | Blocks | Expanded Qs | With `exp` | Old twin |
|---|---|---|---|---|
| General English Knowledge.json | 100 | 100 | 100 | OldGeneral English Knowledge.json (100, no `exp`) |
| Grammar.json | 100 | 100 | 100 | OldGrammar.json (100, no `exp`) |
| Language Skills.json | 92 | 100 | 100 | OldLanguage Skills.json (92 → 100, no `exp`) |
| Listening Skills.json | 100 | 100 | 100 | OldListening Skills.json (100, no `exp`) |
| Literature.json | 100 | 100 | 100 | OldLiterature.json (100, no `exp`) |
| Parts of Speech.json | 100 | 100 | 100 | OldParts of Speech.json (100, no `exp`) |
| Reading Comprehension.json | 10 passages | 100 | 100 | OldReading Comprehension.json (10 → 100, no `exp`) |
| Vocabulary.json | 100 | 100 | 100 | OldVocabulary.json (100, no `exp`) |
| Writing Skills.json | 100 | 100 | 100 | OldWriting Skills.json (100, no `exp`) |

- **Unique content: 900 questions** (9 topics × 100). The `Old*` files are
  byte-level the same questions without the `exp` (explanation) field — pure
  duplicates that double the repo for no benefit.
- Structure: `{"type":"std","q":…,"opts":[4],"ans":<int>,"exp":"…"}`; passage
  files use Schema B. Explanations are chatty/tutor-style
  ("My dear, the em dash is perfect for…") — usable but inconsistent in tone.
- No corrupt files. No topic/year metadata beyond the filename.

## 4. mystudy-dic (dictionary)

- `data/a.json` … `data/z.json` (26 files): headword → entry. Summed
  headword keys across a–z: **158,265**. `processed/merged.json`: 121,340
  entries; `processed/filtered.json`: 121,297 entries (43 fewer — the
  "kid-safe" filter). The data/ total exceeds merged, so data/ contains
  case/duplicate variants that merging collapses; merged.json is the
  canonical file to import, not data/.
- Entry shape: `{"MEANINGS": {"1": ["Noun", "definition", ["synonyms"], []]},
  "SYNONYMS": […], "ANTONYMS": […]}`. Some entries are bare names
  ("D. h. lawrence", "H. G. Wells", "J. d. salinger") — it is a general
  English dictionary, not a learner's dictionary; no pronunciation, no
  part-of-speech at top level, no examples in most entries.
- Source (per its README): derived from tusharlock10's Dictionary repo
  (Stack Overflow sourced). Licence file present. Three Python scripts
  (`merge.py`, `filter.py`, `Li0n-merge.py`) — **not run** in this audit.
- Size warning for v2: 69 MB non-git (merged.json alone ~21 MB, filtered
  ~21 MB, data/ ~28 MB). Do not ship all three copies to the client; import
  merged.json once into the database and serve lookups from the server.
- Template loads it from `cdn.jsdelivr.net/gh/ola1de/mystudy-dic@main/data/`
  (the per-letter files, not merged.json).

## 5. mystudy-pwa

- **One file only: `sw.js` (1,581 bytes).** No `manifest.json`, no icons,
  no app shell, no offline cache list.
- What `sw.js` does: `CACHE_NAME = 'mystudy-v3'`, `skipWaiting()` /
  `clients.claim()`, a `notificationclick` handler, and a `periodicsync`
  handler that fetches `/feeds/posts/default?alt=json&max-results=1` to
  check for new Blogger posts. It defines **no fetch handler and no cache
  strategy** — so despite the name, this file on its own makes nothing work
  offline. The template registers it by fetching it from jsDelivr and
  creating a Blob — a fragile pattern that must be replaced by a real
  same-origin service worker + manifest in v2.
- No README, no other files.

## 6. mystudy-textbooks

- 166 JSON files (165 chapter files + 1 index), 12 subjects, SSS 1–3 only.
  No JSS, no Primary, no university content.

| Subject | Files | Modules | Quiz questions |
|---|---|---|---|
| Accounting | 8 | 20 | 129 |
| Agric | 24 | 76 | 375 |
| Biology | 13 | 39 | 208 |
| Chemistry | 12 | 49 | 600 |
| Commerce | 9 | 27 | 144 |
| Economics | 12 | 24 | 213 |
| English | 15 | 47 | 750 |
| Geography | 9 | 23 | 153 |
| Government | 24 | 65 | 384 |
| Literature | 9 | 22 | 174 |
| Mathematics | 21 | 64 | 1,000 |
| Physics | 10 | 47 | 500 |
| **Total** | **166** | **503** | **4,630** |

- Chapter shape (all except Mathematics):
  `{"subject","level":"SSS 1","slug","title","outline":[…],
  "modules":[{"title","html":…,"examples":[{"q","a"}]}],"quiz":[…]}`
  Content is HTML strings (`<h4>`, `<table class="tb-table">`, LaTeX-style
  `$…$` in Maths). Quiz counts per chapter vary widely (English 50/chapter,
  Maths 50/chapter, Accounting ~16/chapter) — no uniform chapter length.
- Mathematics files use a **different schema**:
  `{"topic","ss_level","icon","color","outline","modules","slug","subject","quiz"}`
  — `topic` instead of `title`, `ss_level` instead of `level`, plus `icon`
  and `color`. Only Mathematics has an index file
  (`mathematics/mathematics-index.json`, listing topics with question counts);
  the other 11 subjects have no index.
- Subjects **missing** vs the JAMB grid: CRS, IRS, Civic, Computer,
  Further Maths, History, Hausa, Igbo, Yoruba. Literature chapters are
  generic appreciation/prescribed-text frameworks, not the JAMB prescribed
  texts themselves.
- No corrupt files (all 166 parse). Quality spot-check was structural only;
  factual accuracy of the 503 modules was **not** verified in this audit.

## 7. nigeria-constitution

- 11 JSON files, 532 KB. `manifest.json` lists Preamble + Chapters I–VIII +
  Schedules; source stated as "Federal Republic of Nigeria — 1999
  Constitution (as amended)".
- Chapters I–VIII: **227 sections total** — Ch. I: 11, Ch. II: 5, Ch. III: 7,
  Ch. IV: 11, Ch. V: 48, Ch. VI: 68, Ch. VII: 50, Ch. VIII: 27.
- Section shape: `{"number","heading","paragraphs":[],"items":[{"label":"(1)",
  "text":…,"items":[…]}]}` — nested sub-items preserved.
- `schedules.json` (First Schedule etc.) is stored as large flat paragraph
  strings rather than structured LGA tables — usable for reading, poor for
  search/filter by state/LGA.
- No corrupt files. Amendment status / which amendments are included is not
  stated in the files — verify against the official text before presenting
  it as current law in v2.

## 8. vocabulary-database

- 24 data files × 100 words = **2,400 words**, plus `index.json`.
- Word shape: `{"id":"ad-001","word":"Agenda","pos":"noun",
  "definition":"…","example":"…"}` — clean, uniform, the best-structured
  dataset in the audit.
- Categories (24): admin-vocabulary, animal-habitats, baby-animals,
  branches-of-study, capability-adjectives, collective-nouns, dietary-habits,
  environment, forms-of-government, idioms, measurement-instruments,
  medical-specialists, natural-phenomena, obsessions, one-word-substitutions,
  personality-types, philosophical-stances, phobias, professions, proverbs,
  sensory-sounds, time-and-frequency, umbrella-terms, words-for-killing.
- **Gap: `index.json` lists only 14 of the 24 categories.** Unindexed (and
  therefore likely unreachable from the template's category list):
  admin-vocabulary, animal-habitats, capability-adjectives, environment,
  idioms, natural-phenomena, professions, proverbs, sensory-sounds,
  umbrella-terms.
- No corrupt files.

## 9. random-quotes

- One file, `Quotes.txt`, 24 KB, 271 non-empty lines, **271 quotes** matching
  `Quote: "…" — Author`. Template parses lines containing `Quote:`.
- No categories, no authors list, no deduplication check done. Smallest
  repo; trivially importable as a quotes table.

---

## 10. Cross-cutting findings for the v2 rebuild

1. **Four different question schemas, zero shared metadata.** JAMB/WAEC/NECO
   JSON (A/B/C), English-Quiz (A + `exp`), textbook `quiz` arrays, and TXT
   banks all need normalising into one canonical question model
   (`exam, subject, year, topic, type, question, options[4], answer_index,
   explanation, passage_id`) before any import. Filenames are currently the
   only source of exam/subject/year — a v2 importer must parse filenames
   and reject the placeholder files, not import them as real questions.
2. **No syllabus / keypoints / topic data exists in any repo.** The template
   advertises Syllabus, Keypoints and Tutorials, but no repo contains them.
   Those must be authored (or sourced) new — they cannot be "migrated".
3. **No Post-UTME, BECE, JSS or 2026 content anywhere.** The only
   non-JAMB/WAEC/NECO bank is Primary 2026 (560 Qs). If v2 promises
   Post-UTME mocks, that bank must be built from scratch.
4. **Dictionary is the only oversized asset** (72 MB, 91% of all repo bytes).
   Everything else combined is ~7 MB. Import merged.json server-side; never
   ship data/ + processed/ to the browser.
5. **mystudy-pwa is not a PWA.** One 1.6 KB service worker with no fetch
   handler, no manifest, no icons. Offline support must be built new in v2,
   not "upgraded" from this file.

## 11. The 5 biggest gaps for the v2 rebuild

1. **WAEC/NECO are hollow: 2020–2023 are placeholders and 11× 2024
   science/math files are corrupt.** Only 2024–2025 are real, and for
   Chemistry/FurtherMath/Geography/Physics only 2025 survives. The v2 CBT
   must either source real WAEC/NECO 2020–2024 papers or stop advertising
   those years — shipping the "Question Content Here?" placeholder as a
   live exam would be worse than showing nothing.
2. **Zero explanations for JAMB (5,263 Qs) and Primary (560 Qs), and no
   topic tags anywhere.** A JAMB-like CBT needs per-question explanations
   and topic-wise practice; both must be authored. Topic tagging cannot be
   inferred from the files — every question needs a `topic` assigned.
3. **Textbooks cover only 12 of 21 subjects and SSS only.** CRS, IRS,
   Civic, Computer, Further Maths, History, Hausa, Igbo and Yoruba have no
   textbook chapters at all; there is no JSS or Primary textbook content.
   Mathematics also uses a different file schema from the other 11 subjects.
4. **No syllabus, keypoints, tutorials, Post-UTME, or BECE content exists
   in any repo** — these are advertised features with no underlying data.
5. **Supporting data is incomplete in small, fixable ways that will break
   the UI if imported blindly:** English-Quiz is 50% duplicate `Old*`
   files; vocabulary `index.json` omits 10 of 24 categories; the TXT banks
   are truncated for 5 subjects (Maths 51, Physics 39, IRK 112, Biology
   137, Literature 190 vs the 250 pattern) and Physics has a broken option;
   the Constitution schedules are unstructured text; the dictionary has
   three overlapping copies (158k keys in data/, 121k merged, 121k filtered).

## 12. What is reusable as-is

- JAMB 2021–2025 JSON (5,241 real questions) — the strongest asset; needs
  schema normalisation + explanations + topics, not re-creation.
- WAEC/NECO 2024 (with explanations, where parseable) + 2025.
- Primary 2026 (560 Qs).
- English-Quiz current 9 files (900 Qs with explanations) — delete the
  `Old*` twins.
- Textbooks: 166 chapters / 503 modules / 4,630 quiz Qs for 12 subjects.
- Dictionary merged.json (121,340 entries), vocabulary 2,400 words,
  Constitution 227 sections, 271 quotes — all importable after a format
  pass.
- `mystudy-pwa/sw.js`: reusable only as a reference for the notification /
  periodic-sync intent, not as a working service worker.

---

*Audit completed 24 Nov 2026 from shallow clones at `/tmp/mystudy-repos/`.
Nothing was pushed, committed or modified on GitHub. Question counts were
counted from the files, not estimated; where a file could not be parsed its
questions are excluded and the file is listed in §2.4.*
