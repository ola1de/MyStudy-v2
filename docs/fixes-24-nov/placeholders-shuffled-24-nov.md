# Placeholder answer-position fix — shuffle pass, 24 Nov 2026

## What was wrong (before)

In `~/workspace/mystudy/data-repos/Exam-Questions-Data/json/`, all 190 filled
placeholder files (`practice:true`, 8,580 real questions):

| Group | Files | Questions | Before (A / B / C / D) | Before % |
|---|---|---|---|---|
| JAMB 2020 + Hausa 2023 | 22 | 900 | 900 / 0 / 0 / 0 | 100 / 0 / 0 / 0 |
| WAEC 2020–2023 | 84 | 4,240 | 1,034 / 1,113 / 1,050 / 1,043 | 24.4 / 26.2 / 24.8 / 24.6 |
| NECO 2020–2023 | 84 | 3,440 | 701 / 869 / 1,054 / 816 | 20.4 / 25.3 / 30.6 / 23.7 |

JAMB was unusable as-is: the correct answer was always A. NECO was C-heavy.
WAEC was already roughly balanced but was shuffled anyway for exact per-file balance.

## Method

- Script: `~/workspace/mystudy/tools/shuffle-placeholders.py`
  (copy of `/tmp/shuffle_placeholders.py`).
- Seed: base string `mystudy-shuffle-v1`; per-file seed =
  SHA-256(`mystudy-shuffle-v1:<filename>`) truncated to 64 bits, fed to
  `random.Random` — deterministic, stable across runs and platforms.
- Scope: only the 190 files containing `practice:true` questions. Real
  (non-placeholder) files were not touched. The 11 corrupt-fixed files were
  not touched (only verified to still parse, see below).
- Per file, target answer counts are as equal as possible: 40 Qs → 10/10/10/10,
  50 Qs → 13/13/12/12 (the two +1s go to indices first in seeded order),
  60 Qs → 15/15/15/15. Targets are assigned to questions in seeded-shuffled
  order; each question's 4 options are then permuted with the correct option
  swapped into its assigned position. Distractor order is also shuffled.
- Only `opts` order and `ans` changed. Question text, explanations, `source`,
  `practice`, `type` and passage/poem content are untouched.

### Disclosure: the script ran twice

The first invocation was piped through `head` and `tail`, which ran it twice.
Both passes used the same seeded targets, so balance and correctness are
unaffected, but the final state is the result of two seeded shuffles, not one.
Single-pass reproducibility from the pre-shuffle filled files is not possible
because no backup of the filled pre-shuffle files exists — the
`orig-placeholders-*` directories in `docs/fixes-24-nov/` hold the original
1-question placeholders from git HEAD, not the filled files. Re-running the
script on the current files keeps the same balance and correctness (it is
idempotent for those properties) but produces a different option order.
This does not affect the validity of the result below, which was verified
independently of the shuffle script.

## After (verified independently)

| Group | Questions | After (A / B / C / D) | After % |
|---|---|---|---|
| JAMB | 900 | 225 / 225 / 225 / 225 | 25.0 / 25.0 / 25.0 / 25.0 |
| WAEC | 4,240 | 1,064 / 1,062 / 1,055 / 1,059 | 25.09 / 25.05 / 24.88 / 24.98 |
| NECO | 3,440 | 860 / 860 / 860 / 860 | 25.0 / 25.0 / 25.0 / 25.0 |
| **Total** | **8,580** | **2,149 / 2,147 / 2,140 / 2,144** | **25.05 / 25.02 / 24.94 / 24.99** |

Per-file: every one of the 190 files is balanced to within 1 question
(worst deviation 1 percentage point, on 50-question files with a 12/13 split).
Before-distributions per file are saved in
`shuffle-before-distributions.json` in this directory.

## Verification (independent check, after the shuffle)

- All 389 JSON files in `json/` parse.
- All 8,580 placeholder questions: 4 distinct options, valid `ans` (0–3),
  `practice:true`, `source` present, `explanation` present — **0 errors**.
- No duplicate question text within any file (normalised whitespace/case).
- Spot-check of 6 random questions across groups (Maths, Biology, Chemistry,
  Economics, English, Physics): the option at `ans` is factually correct in
  every case (e.g. sin 30° → 0.5; ethane → C₂H₆; F = ma = 20 N).
- The 11 corrupt-fixed files still parse (NECO Chemistry/Computer/FurtherMath/
  Geography/History 2025/Mathematics/Physics 2024; WAEC Chemistry/FurtherMath/
  Geography/Physics 2024) — 70 items each except WAEC FurtherMath (60) and
  NECO History 2025 (71 questions across 70 items).
- `git status` in the clone: 201 modified files = 190 placeholder files +
  the 11 corrupt-fixed files (modified before this task, not by it).
  No real (non-placeholder) file was modified.

## The "5 missing practice:true" — resolved, no fix needed

The parent check found 895/900 JAMB questions carrying `practice:true`.
There are no missing labels. The count was a counting artefact: the checker
counted the `poem` container block in `JAMB_Literature_2020.json` as a
question (it has no `ans`/`opts`, only nested `questions`), while its 5 nested
questions were not expanded. Correct count, expanding all passage/poem
containers: **900 real JAMB questions, 900 with `practice:true`, 900 with
`source` and `explanation`**. The container itself correctly carries no
`practice` flag — it is not a question, and none was added.

## The 389 vs 390 file count — resolved, no file missing

- Durable clone `json/` contains **389 `.json` files + 1 `README.md`** (empty)
  = 390 directory entries.
- The audit counted **389 JSON files** — exactly matching the durable clone.
- The "390" in the parent check was the directory-entry count including
  `README.md`. No exam file is missing: 190 placeholder + 199 real = 389.
  Root-level TXT banks (14) are also present in the repo.

## Still flagged (not in this task's scope)

- `NECO_Computer_2024.json` Q13 (corrupt-fixed file): 5 options, none
  containing `$` — still needs re-sourcing from the real NECO 2024 paper or
  dropping; the v2 importer must keep excluding non-4-option questions.
- Nothing was pushed to GitHub.
