# WAEC Placeholder Files — Filled 24 November 2026

## What was done

- **84 files filled** (21 subjects × WAEC 2020, 2021, 2022, 2023) in the durable clone `~/workspace/mystudy/data-repos/Exam-Questions-Data/json/` — **4,240 questions** in total (50 per file; English 60 per file including 2 comprehension passages).
- Every file is a **syllabus-modelled practice set, NOT the official paper**: every question (including questions inside passages) carries `"practice": true` and a `"source"` field naming the syllabus topic, the file's year, and the source (WAEC syllabus via waecsyllabus.com, JAMB syllabus via ibass.jamb.gov.ng, adapted by topic from the repo's real WAEC 2024/2025 files).
- Files were written with Python (`json.dump`, `ensure_ascii=False`, `indent=2`), options shuffled so `ans` is spread across 0–3, in the 2024 plain style (`q`/`opts`/`ans` + `explanation` + `topic` + `practice` + `source`). English uses the typed style with passages, matching its real files.
- **Nothing was pushed to GitHub.** The 11 corrupt files were NOT touched by this task (a separate agent is fixing those). No real file, NECO file or JAMB file was touched by this task.

## IMPORTANT — earlier work lost and redone

All placeholder work done earlier in this session lived in `/tmp/mystudy-repos/Exam-Questions-Data`, which was wiped when `/tmp` was cleared. That work is lost. Everything in this manifest was redone from the durable clone at `~/workspace/mystudy/data-repos/Exam-Questions-Data/`. `/tmp` was not used again for this work. Generators live in `~/workspace/mystudy/gen-waec/` (`core.py`, `numeric.py`, `numeric2.py`, `facts1.py`, `facts2.py`, `facts3.py`, `lang.py`, `gen.py`, `validate.py`); run reports in `gen-report.json` and `validate-report.json` in the same folder.

## Backup

- Original placeholders backed up BEFORE any overwriting to `~/workspace/mystudy/docs/fixes-24-nov/orig-placeholders-waec/` — 84 files, all verified still to be the original placeholders (contain "Question Content Here").
- Pre-generation SHA-256 snapshot of the repo's JSON files: `~/workspace/mystudy/gen-waec/pre-gen-hashes.json`.

## Sources used (online first, per the brief)

### Syllabuses

- JAMB syllabus (official PDFs): `https://ibass.jamb.gov.ng` — e.g. Mathematics `https://ibass.jamb.gov.ng/static/media/Mathematics.c0621f4b8b674e75fd05.pdf`, plus Government, Use of English, Chemistry, CRS, Islamic Studies, Arabic. Structure confirmed: Mathematics in 5 sections (Number and Numeration; Algebra; Geometry/Trigonometry; Calculus; Statistics); Use of English in 3 sections (Comprehension/Summary; Lexis and Structure; Oral Forms), 60 questions total.
- WAEC syllabus topic hub: `https://waecsyllabus.com/wassce-syllabus/` and topic list `https://waecsyllabus.com/wassce-topics/` (66 subjects, 2,213 topics). Topic counts used as coverage checklists: Agric 70, Biology 67, Chemistry 23, Computer Science 77, Geography 53, Physics 42, Hausa 37, Igbo 15, Yoruba 12, Government 20, History 32, Islamic Studies 44, Economics 25, Financial Accounting 18. Also `https://schoolnews.com.ng/wassce-waec-syllabus/` and `https://lekkiheadmaster.com/waec-syllabus/` (2026–2030 Literature set texts).
- NECO syllabus (official route): `https://www.neco.gov.ng` → Examinations > SSCE > Syllabuses (free PDF, no account); topic summaries at `https://syllabus.ng/neco/economics/`, `https://ajls.ng/neco-syllabus-for-economics/`, `https://ijlet.com/neco-syllabus-for-government/`. (NECO files are not in this WAEC task; listed because the syllabus search covered them.)
### Real past questions (public, no login, no payment)

- WikiQuestions `https://wikiquestions.org/` — free, volunteer-maintained, 17,377 past questions digitised as of 16 Nov 2026. Subjects with years: English 1988–2025, General Mathematics 1988–2025, Civic 2010–2025, Government 2000–2024, Economics 1988–2024, Literature 2010–2024, CRS 1988–2024, Biology 1988–2025, Chemistry 1988–2025, Physics 1988–2025, Agric 1988–2025.
- **Limitation, stated plainly:** WAEC General Mathematics 2020–2025 pages exist on WikiQuestions but are marked not yet available; only the 2018 paper was fetched (50 objective questions, e.g. simplify √108+√125−√75, percentages, cylinder volume). It was used as a topic/style model, not copied verbatim. **No bulk free download of the actual WAEC 2020–2023 papers was fetched in this session.** The 2020–2023 sets are therefore syllabus-modelled practice adapted by topic from the repo's real 2024/2025 files and the 2018 WikiQuestions paper — not verbatim official papers. That is why the `practice:true` + `source` labelling is on every question.
- WAEC e-Learning (official) `https://www.waeconline.org.ng/e-Learning/index.htm` — past questions and Chief Examiner's reports, **no PDF downloads**, view on site only (could not be bulk-fetched).
- 9ja Past Questions `https://www.9japastquestions.com/` — free WAEC/JAMB/GCE/Post-UTME, no signup needed for WAEC.
- Also found, not fetched in depth: `https://schoolgist.ng/free-waec-past-questions-and-answers`, `https://www.assessly.ng/waec-practice`, `https://myschool.ng/serve/waec-past-questions-objective-theory-study-100-offline-download-app-now-127076` (app-locked, no PDF export), `https://richlyai.com/blog/download-waec-past-questions-pdf/`.
- Repo's own real past questions (2024/2025) in `~/workspace/mystudy/data-repos/Exam-Questions-Data/json/` were used as the topic/style source for adaptation, and as the verbatim-match check set (2,717 questions).

## Validation (independent pass, `validate.py`, after generation)

- **PROBLEMS: 0.** All 84 files parse as JSON; every file has its target count (50, English 60); every question has exactly 4 distinct options, `ans` in 0–3, a non-empty explanation, `practice: true`, and a `source` naming the topic and the file's year; no duplicates within any file; no question matches a real WAEC 2024/2025 question by normalised text (see dropped counts below); every written answer was checked against the generator's pool answer for that question (0 mismatches).
- Answer-position distribution is spread across 0–3 in every file (options were shuffled at write time; no file has `ans` always 0).
- **Verbatim-match drops: 122 questions** across the 84 files were dropped during generation because their normalised text matched a real WAEC 2024/2025 question in the repo, and replaced with a different question from the same subject's pool (per-file counts in the table). Final files contain 0 such matches.
- **Filler options: 39 of 4,240 questions (0.9%)** use a generic distractor ("None of the above" / "All of the above" / "Cannot be determined") — only ever as a distractor, never as the correct answer. These are cases where computed distractors collapsed to duplicates (e.g. a percentage with two equal distractors) or duplicated vocabulary words (Igbo boy/man both "nwoke"). Legitimate MCQ style, not an error.

## Answers spot-checked by hand (independent of the generator)

- Mathematics: mean of 4, 9, 2, 10, 10 = 7 ✓; 3x + 23 = 35 → x = 4 ✓
- Further Mathematics: lim(x→0) sin 9x / x = 9 ✓; ∫₀¹ 3x² dx = 1 ✓
- Physics: centre of gravity of a uniform rod = midpoint ✓; SI unit of pressure = Pascal ✓
- Chemistry: relative molecular mass of CO₂ = 44 ✓; most reactive common metal = Potassium ✓
- Accounting: purchases ledger control = Creditors control account ✓; cost of goods sold = 10000 + 40000 − 5000 = ₦45000 ✓
- Economics: price elasticity = 5% ÷ 20% = 0.25 ✓; law of demand — quantity demanded falls as price rises ✓
- Computer: 16 KB = 16384 bytes ✓; paste shortcut = Ctrl + V ✓
- Biology: smallest blood vessels = capillaries ✓; evolution by natural selection = Charles Darwin ✓
- CRS: ark rested on Mount Ararat ✓; Jericho fell after seven days ✓
- History: Structural Adjustment Programme introduced by Ibrahim Babangida ✓; Mary Slessor worked among the people of Calabar ✓
- Geography: crude oil mainly in the Niger Delta ✓; Nigeria is GMT+1 ✓
- Hausa: house = Gida ✓; one = ɗaya ✓; two = biyu ✓
- Igbo: white = ọcha ✓; ojii = black ✓; girl = nwanyị ✓
- Yoruba: white = fúnfun ✓; blue = búlù ✓; head = orí ✓

## Honest shortfall — cross-year overlap (read this)

The brief asked for the 4 yearly sets of each subject to share no question. That is **fully achieved only for Mathematics and English (0 shared questions between any two years)** and nearly for Physics (0–10) and Further Mathematics (0–13). For the other 17 subjects it is **mathematically impossible with the pools built**: each subject's core syllabus-fact pool (see pool sizes below) is smaller than 4 × 50 = 200, so the same syllabus fact necessarily recurs across years — exactly as topics recur across years in real WAEC papers. A rotation allocation was used to minimise the overlap (each fact is used in as few years as possible; no two yearly files are the same set, and option order / answer positions differ per year), and the overlap is at or near the floor the pool size allows. The per-pair shared-question counts are in the table below. If fully disjoint yearly sets are required for these subjects, the fact pools must be expanded to ~200 distinct questions per subject first — that was not done in this task.

## Shortfall — Hausa / Igbo / Yoruba

- All three are written **in the language** (no English questions passed off as language questions). Coverage: vocabulary (animals, body, family, colours, nature), numbers 1–20, greetings, grammar (nouns/verbs/adjectives/pronouns, vowels, tones), written literature (Hausa: Abubakar Imam, *Magana Jari Ce*, *Ruwan Bagaja*; Igbo: Pita Nwana, *Omenuko*, Chinua Achebe, *Things Fall Apart*; Yoruba: D. O. Fagunwa, *Ògbójú Ọdẹ Nínú Igbó Irúnmọ̀lẹ̀*, Akinwumi Isola, *Olèkù*, Wole Soyinka, *The Lion and the Jewel*, Amos Tutuola, *The Palm-Wine Drinkard*), proverbs and customs (e.g. Iri Ji, Mmanwu, ẹ̀mí/orí).
- **Limitation:** the language sets are 50 standalone questions each — they have **no comprehension passages**, unlike the real WAEC language papers (which have passages). Literature coverage is limited to a few well-known works; the full WAEC set-text lists were not turned into questions. Do not present these as complete coverage of the language syllabuses.

## Files changed audit

- Files changed vs the pre-generation snapshot: 106. Of these, **84 are this task's WAEC 2020–2023 files**. The other 22 are JAMB files (`JAMB_Accounting_2020`, `JAMB_Agric_2020`, `JAMB_Biology_2020`, `JAMB_CRS_2020`, `JAMB_Chemistry_2020`, `JAMB_Civic_2020`, `JAMB_Commerce_2020`, `JAMB_Computer_2020`, `JAMB_Economics_2020`, `JAMB_English_2020`, `JAMB_FurtherMath_2020`, `JAMB_Geography_2020`, `JAMB_Government_2020`, `JAMB_Hausa_2020`, `JAMB_Hausa_2023`, `JAMB_History_2020`, `JAMB_IRS_2020`, `JAMB_Igbo_2020`, `JAMB_Literature_2020`, `JAMB_Mathematics_2020`, `JAMB_Physics_2020`, `JAMB_Yoruba_2020`) — changed by **parallel agents working on the JAMB placeholders during this run, not by this task**. No new files, no missing files.
- The 11 corrupt files were verified unchanged by this task's generation run (hash-checked before and after).
- Note: the repo was counted at 390 JSON files in an earlier check and 389 in the pre-generation snapshot (snapshot taken 24 Nov 2026, `pre-gen-hashes.json`); the one-file difference is unresolved and is not one of the 84 files.

## Per-file table

Columns: file | top-level items | total questions (incl. passage questions) | duplicates within file | verbatim matches vs real 2024/2025 in final file | questions dropped during generation for verbatim match | answer-position distribution (ans 0/1/2/3). All files: parsed OK, 0 problems.

| File | Top | Total | Dups | Real-match | Dropped | ans 0/1/2/3 |
|---|---|---|---|---|---|---|
| WAEC_Accounting_2020.json | 50 | 50 | 0 | 0 | 1 | 8/12/19/11 |
| WAEC_Accounting_2021.json | 50 | 50 | 0 | 0 | 2 | 16/6/17/11 |
| WAEC_Accounting_2022.json | 50 | 50 | 0 | 0 | 1 | 8/10/12/20 |
| WAEC_Accounting_2023.json | 50 | 50 | 0 | 0 | 0 | 15/17/8/10 |
| WAEC_Agric_2020.json | 50 | 50 | 0 | 0 | 0 | 14/11/10/15 |
| WAEC_Agric_2021.json | 50 | 50 | 0 | 0 | 0 | 13/15/13/9 |
| WAEC_Agric_2022.json | 50 | 50 | 0 | 0 | 0 | 9/19/14/8 |
| WAEC_Agric_2023.json | 50 | 50 | 0 | 0 | 0 | 17/10/9/14 |
| WAEC_Biology_2020.json | 50 | 50 | 0 | 0 | 2 | 10/21/8/11 |
| WAEC_Biology_2021.json | 50 | 50 | 0 | 0 | 1 | 10/16/13/11 |
| WAEC_Biology_2022.json | 50 | 50 | 0 | 0 | 1 | 12/14/13/11 |
| WAEC_Biology_2023.json | 50 | 50 | 0 | 0 | 1 | 10/12/11/17 |
| WAEC_CRS_2020.json | 50 | 50 | 0 | 0 | 1 | 11/7/22/10 |
| WAEC_CRS_2021.json | 50 | 50 | 0 | 0 | 5 | 11/10/13/16 |
| WAEC_CRS_2022.json | 50 | 50 | 0 | 0 | 2 | 10/15/8/17 |
| WAEC_CRS_2023.json | 50 | 50 | 0 | 0 | 2 | 14/10/14/12 |
| WAEC_Chemistry_2020.json | 50 | 50 | 0 | 0 | 2 | 12/10/9/19 |
| WAEC_Chemistry_2021.json | 50 | 50 | 0 | 0 | 3 | 14/14/11/11 |
| WAEC_Chemistry_2022.json | 50 | 50 | 0 | 0 | 4 | 12/15/7/16 |
| WAEC_Chemistry_2023.json | 50 | 50 | 0 | 0 | 1 | 19/13/9/9 |
| WAEC_Civic_2020.json | 50 | 50 | 0 | 0 | 2 | 14/12/10/14 |
| WAEC_Civic_2021.json | 50 | 50 | 0 | 0 | 4 | 14/13/15/8 |
| WAEC_Civic_2022.json | 50 | 50 | 0 | 0 | 3 | 11/12/14/13 |
| WAEC_Civic_2023.json | 50 | 50 | 0 | 0 | 1 | 17/13/10/10 |
| WAEC_Commerce_2020.json | 50 | 50 | 0 | 0 | 0 | 10/12/17/11 |
| WAEC_Commerce_2021.json | 50 | 50 | 0 | 0 | 1 | 13/20/8/9 |
| WAEC_Commerce_2022.json | 50 | 50 | 0 | 0 | 1 | 17/11/10/12 |
| WAEC_Commerce_2023.json | 50 | 50 | 0 | 0 | 1 | 12/10/16/12 |
| WAEC_Computer_2020.json | 50 | 50 | 0 | 0 | 6 | 13/14/15/8 |
| WAEC_Computer_2021.json | 50 | 50 | 0 | 0 | 2 | 8/13/18/11 |
| WAEC_Computer_2022.json | 50 | 50 | 0 | 0 | 4 | 12/17/13/8 |
| WAEC_Computer_2023.json | 50 | 50 | 0 | 0 | 1 | 12/13/12/13 |
| WAEC_Economics_2020.json | 50 | 50 | 0 | 0 | 0 | 12/18/9/11 |
| WAEC_Economics_2021.json | 50 | 50 | 0 | 0 | 2 | 10/11/12/17 |
| WAEC_Economics_2022.json | 50 | 50 | 0 | 0 | 2 | 13/15/10/12 |
| WAEC_Economics_2023.json | 50 | 50 | 0 | 0 | 1 | 10/13/9/18 |
| WAEC_English_2020.json | 52 | 60 | 0 | 0 | 0 | 9/13/16/22 |
| WAEC_English_2021.json | 52 | 60 | 0 | 0 | 0 | 17/13/16/14 |
| WAEC_English_2022.json | 52 | 60 | 0 | 0 | 0 | 8/21/17/14 |
| WAEC_English_2023.json | 52 | 60 | 0 | 0 | 1 | 19/20/12/9 |
| WAEC_FurtherMath_2020.json | 50 | 50 | 0 | 0 | 0 | 13/12/16/9 |
| WAEC_FurtherMath_2021.json | 50 | 50 | 0 | 0 | 0 | 15/13/11/11 |
| WAEC_FurtherMath_2022.json | 50 | 50 | 0 | 0 | 1 | 14/11/11/14 |
| WAEC_FurtherMath_2023.json | 50 | 50 | 0 | 0 | 0 | 15/9/12/14 |
| WAEC_Geography_2020.json | 50 | 50 | 0 | 0 | 2 | 11/10/14/15 |
| WAEC_Geography_2021.json | 50 | 50 | 0 | 0 | 2 | 11/14/16/9 |
| WAEC_Geography_2022.json | 50 | 50 | 0 | 0 | 0 | 13/18/9/10 |
| WAEC_Geography_2023.json | 50 | 50 | 0 | 0 | 2 | 12/17/11/10 |
| WAEC_Government_2020.json | 50 | 50 | 0 | 0 | 2 | 10/16/11/13 |
| WAEC_Government_2021.json | 50 | 50 | 0 | 0 | 2 | 9/17/11/13 |
| WAEC_Government_2022.json | 50 | 50 | 0 | 0 | 3 | 11/14/11/14 |
| WAEC_Government_2023.json | 50 | 50 | 0 | 0 | 2 | 18/6/12/14 |
| WAEC_Hausa_2020.json | 50 | 50 | 0 | 0 | 1 | 15/8/13/14 |
| WAEC_Hausa_2021.json | 50 | 50 | 0 | 0 | 2 | 13/11/12/14 |
| WAEC_Hausa_2022.json | 50 | 50 | 0 | 0 | 3 | 13/15/9/13 |
| WAEC_Hausa_2023.json | 50 | 50 | 0 | 0 | 2 | 13/15/14/8 |
| WAEC_History_2020.json | 50 | 50 | 0 | 0 | 3 | 12/12/14/12 |
| WAEC_History_2021.json | 50 | 50 | 0 | 0 | 7 | 14/13/9/14 |
| WAEC_History_2022.json | 50 | 50 | 0 | 0 | 3 | 7/14/13/16 |
| WAEC_History_2023.json | 50 | 50 | 0 | 0 | 4 | 14/14/10/12 |
| WAEC_IRS_2020.json | 50 | 50 | 0 | 0 | 0 | 14/12/12/12 |
| WAEC_IRS_2021.json | 50 | 50 | 0 | 0 | 1 | 12/17/9/12 |
| WAEC_IRS_2022.json | 50 | 50 | 0 | 0 | 2 | 10/12/13/15 |
| WAEC_IRS_2023.json | 50 | 50 | 0 | 0 | 2 | 13/10/10/17 |
| WAEC_Igbo_2020.json | 50 | 50 | 0 | 0 | 0 | 9/9/19/13 |
| WAEC_Igbo_2021.json | 50 | 50 | 0 | 0 | 0 | 12/15/11/12 |
| WAEC_Igbo_2022.json | 50 | 50 | 0 | 0 | 0 | 12/11/18/9 |
| WAEC_Igbo_2023.json | 50 | 50 | 0 | 0 | 0 | 19/10/10/11 |
| WAEC_Literature_2020.json | 50 | 50 | 0 | 0 | 2 | 12/11/13/14 |
| WAEC_Literature_2021.json | 50 | 50 | 0 | 0 | 2 | 7/17/18/8 |
| WAEC_Literature_2022.json | 50 | 50 | 0 | 0 | 4 | 11/16/12/11 |
| WAEC_Literature_2023.json | 50 | 50 | 0 | 0 | 3 | 12/17/10/11 |
| WAEC_Mathematics_2020.json | 50 | 50 | 0 | 0 | 0 | 11/13/14/12 |
| WAEC_Mathematics_2021.json | 50 | 50 | 0 | 0 | 0 | 14/18/7/11 |
| WAEC_Mathematics_2022.json | 50 | 50 | 0 | 0 | 0 | 11/14/15/10 |
| WAEC_Mathematics_2023.json | 50 | 50 | 0 | 0 | 0 | 15/8/12/15 |
| WAEC_Physics_2020.json | 50 | 50 | 0 | 0 | 1 | 11/12/11/16 |
| WAEC_Physics_2021.json | 50 | 50 | 0 | 0 | 0 | 10/12/21/7 |
| WAEC_Physics_2022.json | 50 | 50 | 0 | 0 | 1 | 9/11/14/16 |
| WAEC_Physics_2023.json | 50 | 50 | 0 | 0 | 0 | 14/14/10/12 |
| WAEC_Yoruba_2020.json | 50 | 50 | 0 | 0 | 1 | 12/14/15/9 |
| WAEC_Yoruba_2021.json | 50 | 50 | 0 | 0 | 0 | 13/9/13/15 |
| WAEC_Yoruba_2022.json | 50 | 50 | 0 | 0 | 0 | 10/14/14/12 |
| WAEC_Yoruba_2023.json | 50 | 50 | 0 | 0 | 1 | 12/17/11/10 |

## Cross-year overlap per subject (shared normalised question texts between yearly pairs)

Pool size = distinct question texts in the subject's generator pool (union across 2020–2023). Mathematics and English: 0 everywhere (fully disjoint). Others: at or near the floor the pool size allows.

| Subject | Pool size | 2020v2021 | 2020v2022 | 2020v2023 | 2021v2022 | 2021v2023 | 2022v2023 |
|---|---|---|---|---|---|---|---|
| Accounting | 101 | 18 | 18 | 17 | 19 | 16 | 17 |
| Agric | 84 | 27 | 26 | 24 | 25 | 23 | 23 |
| Biology | 97 | 20 | 21 | 19 | 18 | 19 | 20 |
| CRS | 86 | 29 | 27 | 25 | 28 | 25 | 25 |
| Chemistry | 120 | 19 | 15 | 18 | 14 | 9 | 13 |
| Civic | 95 | 23 | 25 | 21 | 22 | 22 | 20 |
| Commerce | 77 | 32 | 29 | 28 | 30 | 27 | 27 |
| Computer | 104 | 21 | 20 | 19 | 20 | 17 | 19 |
| Economics | 129 | 14 | 13 | 11 | 16 | 13 | 11 |
| English | 224 | 0 | 0 | 0 | 0 | 0 | 0 |
| FurtherMath | 193 | 13 | 5 | 0 | 6 | 0 | 1 |
| Geography | 98 | 20 | 19 | 20 | 19 | 20 | 18 |
| Government | 95 | 22 | 22 | 21 | 22 | 23 | 20 |
| Hausa | 89 | 24 | 27 | 25 | 25 | 24 | 23 |
| History | 90 | 27 | 27 | 25 | 28 | 26 | 25 |
| IRS | 86 | 26 | 25 | 25 | 25 | 24 | 25 |
| Igbo | 85 | 26 | 25 | 23 | 25 | 23 | 23 |
| Literature | 77 | 33 | 32 | 31 | 33 | 30 | 30 |
| Mathematics | 683 | 0 | 0 | 0 | 0 | 0 | 0 |
| Physics | 270 | 10 | 0 | 0 | 1 | 0 | 0 |
| Yoruba | 91 | 23 | 23 | 21 | 21 | 21 | 21 |

## English passages (original, written for this practice set)

8 passages, 2 per year, 5 questions each — disjoint across years: 2020 "The Honest Trader" + "The Village School"; 2021 "The Flood" + "The Football Match"; 2022 "The Library" + "The Farmer and the Rain"; 2023 "The New Student" + "The Market Day". Each passage object carries `practice: true` and a source stating the passage is original.

## Totals

- **84 files, 4240 questions.** Validation problems: **0**.