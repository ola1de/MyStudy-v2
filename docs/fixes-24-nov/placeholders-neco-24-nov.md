# NECO Placeholder Files — Filled 24 November 2026

## What was done

All **84 NECO placeholder files** (21 subjects x 2020, 2021, 2022, 2023) in the durable clone
`~/workspace/mystudy/data-repos/Exam-Questions-Data/json/` were filled with syllabus-modelled
practice sets. Nothing was pushed to GitHub. The 11 corrupt files were **not** touched
(a separate agent is fixing those), and no WAEC or JAMB file was touched.

> **/tmp loss — redo note:** the first version of this work was done in the clone at
> `/tmp/mystudy-repos/Exam-Questions-Data/`, which disappeared when `/tmp` was wiped.
> All placeholder work done there was lost and has been **redone from scratch** in the
> durable clone above. The original generator (`/tmp/gen_neco.py`, expansion pools only)
> survived and was copied to `gen_neco.py` here; the base pools were rebuilt as
> `gen_base.py`, a top-up pool was added as `gen_topup.py`, and the driver is `run_neco.py`.
> Original placeholders were backed up **before** overwriting to
> `~/workspace/mystudy/docs/fixes-24-nov/orig-placeholders-neco/` (84 files).

## Honest labelling

These are **NOT the official NECO papers**. Every question (including questions inside
passages) carries `"practice": true` and
`"source": "MyStudy Practice Set — modelled on the NECO syllabus for this subject, not the official <year> paper"`
with the file's actual year, plus a `topic` (syllabus topic) and an `adapted_from` field
naming the source. Every question also has a short correct `explanation`.

## Sources (fetched online first, 24 November 2026)

- JAMB official syllabus PDFs via IBASS: https://ibass.jamb.gov.ng
  (e.g. Mathematics https://ibass.jamb.gov.ng/static/media/Mathematics.c0621f4b8b674e75fd05.pdf ;
  Government, History, Computer Studies, Principles of Accounting, Agriculture PDFs).
- JAMB syllabus mirror (byte-for-byte, checked 21 Nov 2026): https://jambsyllabus.com/
- WAEC syllabus PDFs/topic lists: https://lekkiheadmaster.com/waec-syllabus/ and https://waecsyllabus.com
  (including Literature set texts 2026-2030).
- JAMB topic lists: https://allschool.ng/jamb-topics-for-all-subjects/
- NECO syllabus: official route https://www.neco.gov.ng > Examinations > SSCE > Syllabuses.
  No direct NECO syllabus PDF URL could be fetched; third-party summaries used:
  https://myuniguide.com/neco-syllabus/ ,
  https://masterneco.com.ng/neco-syllabus-2026-2027-is-out-for-all-subjects/ ,
  https://syllabus.ng/neco/economics/ , https://myedutrend.com.ng/neco-gce-syllabus-for-all-subjects-pdf/
- Past questions online: JAMB Master https://jamb-master.web.app/ (12,166 real JAMB questions
  1983-2020, free, no account); MySchoolGist JAMB past-question PDFs (e.g.
  https://www.myschoolgist.com/wp-content/uploads/2024/11/JAMB-Economics-Past-Questions-and-Answers.pdf ).
- Repo past questions: JAMB 2021-2025 and NECO 2024-2025 files in the durable clone, used for
  topic coverage and style. Questions were **adapted** (reworded, new numbers/names/option sets),
  never copied verbatim — checked by normalised-text hash against all real NECO 2024/2025
  questions (1223 questions from 42 files);
  any match was dropped (see per-subject table).

> **Fallback note:** no free downloadable NECO 2020-2023 paper PDF was found (9japastquestions.com
> needs a free account; ExamPadi / ExamCoach / TestaCBT free tiers are capped at 20-30 questions/day;
> ExamBuddie is Telegram-based and capped). Those sources were **not** used. The sets are therefore
> syllabus-modelled practice sets built from the syllabus topics above plus the repo's real past
> questions, and are labelled as such. They must not be presented as the official 2020-2023 papers.

## Counts

- Files filled: **84**
- Total questions added: **3440**
- Per subject: 40 questions x 4 years = 160, except English 60 x 4 = 240
  (50 standard + 2 passages of 5 questions) and Literature 40 x 4 = 160
  (35 standard + 1 original poem passage of 5 questions).

## Per-subject build table

| Subject | Pool items | Duplicates removed | Dropped (real-file match) | Unique kept | Questions written |
|---|---|---|---|---|---|
| Accounting | 169 | 0 | 0 | 169 | 160 |
| Agric | 177 | 7 | 0 | 170 | 160 |
| Biology | 192 | 1 | 1 | 190 | 160 |
| CRS | 166 | 1 | 3 | 162 | 160 |
| Chemistry | 162 | 0 | 0 | 162 | 160 |
| Civic | 170 | 0 | 0 | 170 | 160 |
| Commerce | 167 | 0 | 0 | 167 | 160 |
| Computer | 188 | 0 | 0 | 188 | 160 |
| Economics | 213 | 0 | 0 | 213 | 160 |
| English | 224 | 20 | 0 | 204 | 240 |
| FurtherMath | 166 | 0 | 0 | 166 | 160 |
| Geography | 173 | 0 | 0 | 173 | 160 |
| Government | 174 | 0 | 2 | 172 | 160 |
| Hausa | 191 | 0 | 1 | 190 | 160 |
| History | 182 | 6 | 1 | 175 | 160 |
| IRS | 164 | 0 | 0 | 164 | 160 |
| Igbo | 167 | 0 | 0 | 167 | 160 |
| Literature | 185 | 23 | 6 | 156 | 160 |
| Mathematics | 168 | 1 | 0 | 167 | 160 |
| Physics | 166 | 0 | 0 | 166 | 160 |
| Yoruba | 182 | 0 | 0 | 182 | 160 |

## Per-file validation

Every file: parses as JSON; question count as listed; no duplicate questions within the file;
no question shared between the 4 yearly sets of the same subject; no question matching a real
NECO 2024/2025 question by normalised text; every question has exactly 4 distinct options,
`ans` in 0-3, `practice: true`, a `source` naming its year, a `topic`, an `explanation` and an
`adapted_from` note. Validation errors: **0**.

| File | Items | Questions | Passages |
|---|---|---|---|
| NECO_Accounting_2020.json | 40 | 40 | 0 |
| NECO_Accounting_2021.json | 40 | 40 | 0 |
| NECO_Accounting_2022.json | 40 | 40 | 0 |
| NECO_Accounting_2023.json | 40 | 40 | 0 |
| NECO_Agric_2020.json | 40 | 40 | 0 |
| NECO_Agric_2021.json | 40 | 40 | 0 |
| NECO_Agric_2022.json | 40 | 40 | 0 |
| NECO_Agric_2023.json | 40 | 40 | 0 |
| NECO_Biology_2020.json | 40 | 40 | 0 |
| NECO_Biology_2021.json | 40 | 40 | 0 |
| NECO_Biology_2022.json | 40 | 40 | 0 |
| NECO_Biology_2023.json | 40 | 40 | 0 |
| NECO_CRS_2020.json | 40 | 40 | 0 |
| NECO_CRS_2021.json | 40 | 40 | 0 |
| NECO_CRS_2022.json | 40 | 40 | 0 |
| NECO_CRS_2023.json | 40 | 40 | 0 |
| NECO_Chemistry_2020.json | 40 | 40 | 0 |
| NECO_Chemistry_2021.json | 40 | 40 | 0 |
| NECO_Chemistry_2022.json | 40 | 40 | 0 |
| NECO_Chemistry_2023.json | 40 | 40 | 0 |
| NECO_Civic_2020.json | 40 | 40 | 0 |
| NECO_Civic_2021.json | 40 | 40 | 0 |
| NECO_Civic_2022.json | 40 | 40 | 0 |
| NECO_Civic_2023.json | 40 | 40 | 0 |
| NECO_Commerce_2020.json | 40 | 40 | 0 |
| NECO_Commerce_2021.json | 40 | 40 | 0 |
| NECO_Commerce_2022.json | 40 | 40 | 0 |
| NECO_Commerce_2023.json | 40 | 40 | 0 |
| NECO_Computer_2020.json | 40 | 40 | 0 |
| NECO_Computer_2021.json | 40 | 40 | 0 |
| NECO_Computer_2022.json | 40 | 40 | 0 |
| NECO_Computer_2023.json | 40 | 40 | 0 |
| NECO_Economics_2020.json | 40 | 40 | 0 |
| NECO_Economics_2021.json | 40 | 40 | 0 |
| NECO_Economics_2022.json | 40 | 40 | 0 |
| NECO_Economics_2023.json | 40 | 40 | 0 |
| NECO_English_2020.json | 52 | 60 | 2 |
| NECO_English_2021.json | 52 | 60 | 2 |
| NECO_English_2022.json | 52 | 60 | 2 |
| NECO_English_2023.json | 52 | 60 | 2 |
| NECO_FurtherMath_2020.json | 40 | 40 | 0 |
| NECO_FurtherMath_2021.json | 40 | 40 | 0 |
| NECO_FurtherMath_2022.json | 40 | 40 | 0 |
| NECO_FurtherMath_2023.json | 40 | 40 | 0 |
| NECO_Geography_2020.json | 40 | 40 | 0 |
| NECO_Geography_2021.json | 40 | 40 | 0 |
| NECO_Geography_2022.json | 40 | 40 | 0 |
| NECO_Geography_2023.json | 40 | 40 | 0 |
| NECO_Government_2020.json | 40 | 40 | 0 |
| NECO_Government_2021.json | 40 | 40 | 0 |
| NECO_Government_2022.json | 40 | 40 | 0 |
| NECO_Government_2023.json | 40 | 40 | 0 |
| NECO_Hausa_2020.json | 40 | 40 | 0 |
| NECO_Hausa_2021.json | 40 | 40 | 0 |
| NECO_Hausa_2022.json | 40 | 40 | 0 |
| NECO_Hausa_2023.json | 40 | 40 | 0 |
| NECO_History_2020.json | 40 | 40 | 0 |
| NECO_History_2021.json | 40 | 40 | 0 |
| NECO_History_2022.json | 40 | 40 | 0 |
| NECO_History_2023.json | 40 | 40 | 0 |
| NECO_IRS_2020.json | 40 | 40 | 0 |
| NECO_IRS_2021.json | 40 | 40 | 0 |
| NECO_IRS_2022.json | 40 | 40 | 0 |
| NECO_IRS_2023.json | 40 | 40 | 0 |
| NECO_Igbo_2020.json | 40 | 40 | 0 |
| NECO_Igbo_2021.json | 40 | 40 | 0 |
| NECO_Igbo_2022.json | 40 | 40 | 0 |
| NECO_Igbo_2023.json | 40 | 40 | 0 |
| NECO_Literature_2020.json | 36 | 40 | 1 |
| NECO_Literature_2021.json | 36 | 40 | 1 |
| NECO_Literature_2022.json | 36 | 40 | 1 |
| NECO_Literature_2023.json | 36 | 40 | 1 |
| NECO_Mathematics_2020.json | 40 | 40 | 0 |
| NECO_Mathematics_2021.json | 40 | 40 | 0 |
| NECO_Mathematics_2022.json | 40 | 40 | 0 |
| NECO_Mathematics_2023.json | 40 | 40 | 0 |
| NECO_Physics_2020.json | 40 | 40 | 0 |
| NECO_Physics_2021.json | 40 | 40 | 0 |
| NECO_Physics_2022.json | 40 | 40 | 0 |
| NECO_Physics_2023.json | 40 | 40 | 0 |
| NECO_Yoruba_2020.json | 40 | 40 | 0 |
| NECO_Yoruba_2021.json | 40 | 40 | 0 |
| NECO_Yoruba_2022.json | 40 | 40 | 0 |
| NECO_Yoruba_2023.json | 40 | 40 | 0 |

## Answer spot-checks (re-read after writing)

One question per subject was sampled from the 2021 file and checked by hand; all were correct,
including computed items (price index 140 for N150 -> N210; GP sum 15 for a=1, r=2, n=4;
3rd GP term 27 for a=1, r=3; V = IR = 20 V for 20 ohms at 1 A). In addition, **all 3,440**
written questions were machine-checked against their source pool item's correct answer:
3,434 matched directly; the remaining 6 are the same question text appearing in two subjects
with the same fact worded differently (e.g. "Addis Ababa" vs "Addis Ababa, Ethiopia";
"bankers' bank" for the Central Bank of Nigeria; 4!/2! = 12) — in each case the written answer
is the correct answer for that file's own source item. No wrong answer was found.

During the build, a pre-flight check found 115 pool items whose generated distractors collided
(duplicate options), e.g. repeated authors in the Literature author table, repeated "processing"
in Computer device types, and arithmetic distractor collisions in Maths/Physics/Accounting.
All were fixed at source (deduplicated distractor lists, corrected distractor formulas) and the
check re-run to 0 bad items before any file was written. One genuinely wrong correct value was
also caught and fixed: density items that used integer division (4 kg / 5 m^3 = 0) now use the
true value (0.8 kg/m^3).

## Shortfalls

- **None by subject.** All 21 subjects were filled to the full target count, including Hausa,
  Igbo and Yoruba, which are written in the language itself (vocabulary, numbers, greetings,
  grammar, literature and culture). No English questions were used to pad them.
- Igbo: the ambiguous `("tooth", "eze")` entry was deliberately **not** used (`eze` is also "king").
  Verified: no "tooth" question appears in any Igbo file.
- Literature poem passages and English comprehension passages are original texts written for this
  practice set, not real NECO passages.

## Files

- Generator: `~/workspace/mystudy/docs/fixes-24-nov/gen_base.py` (base pools),
  `gen_neco.py` (expansion pools), `gen_topup.py` (top-up pools), `run_neco.py` (driver + validator).
- Original placeholders backup: `~/workspace/mystudy/docs/fixes-24-nov/orig-placeholders-neco/` (84 files).
- Machine validation report: `~/workspace/mystudy/docs/fixes-24-nov/validation-neco-24-nov.json`.
- Filled files: `~/workspace/mystudy/data-repos/Exam-Questions-Data/json/NECO_<Subject>_<2020-2023>.json`
  (84 files; confirmed by `git status` — exactly these 84 NECO 2020-2023 files changed by this task).

