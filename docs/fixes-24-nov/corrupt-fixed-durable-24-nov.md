# Corrupt exam JSON files — re-applied to the durable clone (24 Nov 2026)

Repo: `ola1de/Exam-Questions-Data`, durable clone at
`~/workspace/mystudy/data-repos/Exam-Questions-Data/` (fresh `--depth 1` clone
from GitHub, 24 Nov 2026). The user approved processing this clone on
24 Nov 2026. The earlier `/tmp/mystudy-repos` clone disappeared, so these
fixes were re-applied here from scratch — **nothing pushed to GitHub**.
Scope: the 11 corrupt files only. `git status` shows only these 11 modified;
no placeholder file was touched (another agent owns those).

## Result

**11 / 11 files repaired and now parse with strict `json.loads`.
761 questions recovered (760 fully valid + 1 flagged, see below).
761 / 761 have explanations.** `"q":` counts are identical before and after
for every file.

## Method (lossless, syntax-only — same as the first repair)

1. Read each file as bytes (no newline translation), decoded UTF-8, so CRLF
   line endings are preserved exactly.
2. Walked the text tracking in-string vs out-of-string state (honouring `\`
   escapes) and escaped raw control characters found **inside** string values
   only (`\r` → `\\r`, `\n` → `\\n`, `\t` → `\\t`, other controls → `\\u00XX`).
   Structural CRLF line breaks outside strings were left untouched.
3. One targeted fix in `NECO_History_2025.json`: the passage content was
   wrapped in doubled quotes (`"content": ""The history ... oppressed.""`).
   The inner quotes were escaped (`"\"The history ... oppressed.\""`); no
   characters were removed — the file grew by exactly 2 bytes (21,841 → 21,843).
4. No question text, option, answer index, or explanation was changed, added,
   or removed. Nothing was invented. Repair script: `/tmp/repair_corrupt.py`.

## Per-file report

| File | Original error | Fix applied | Questions |
|---|---|---|---|
| NECO_Chemistry_2024.json | Invalid control character, line 9 col 29 | Escaped 3,635 raw control chars in strings | 70 |
| NECO_Computer_2024.json | Invalid control character, line 76 col 17 | Escaped 18 raw control chars in strings | 70 (1 flagged) |
| NECO_FurtherMath_2024.json | Invalid control character, line 3 col 10 | Escaped 11,291 raw control chars in strings | 70 |
| NECO_Geography_2024.json | Invalid control character, line 210 col 33 | Escaped 60 raw control chars in strings (incl. a raw tab) | 70 |
| NECO_History_2025.json | Expecting ',' delimiter, line 94 col 14 | Escaped doubled quotes around passage content; 0 control chars | 71 (incl. 2 passage questions) |
| NECO_Mathematics_2024.json | Invalid control character, line 3 col 16 | Escaped 8,393 raw control chars in strings | 70 |
| NECO_Physics_2024.json | Invalid control character, line 6 col 43 | Escaped 4,211 raw control chars in strings | 70 |
| WAEC_Chemistry_2024.json | Invalid control character, line 14 col 18 | Escaped 5,081 raw control chars in strings | 70 |
| WAEC_FurtherMath_2024.json | Invalid control character, line 3 col 26 | Escaped 12,452 raw control chars in strings | 60 |
| WAEC_Geography_2024.json | Invalid control character, line 25 col 46 | Escaped 25 raw control chars in strings | 70 |
| WAEC_Physics_2024.json | Invalid control character, line 10 col 11 | Escaped 2,940 raw control chars in strings | 70 |

Total control characters escaped: **48,106**.

## Verification

- Every file parses with strict `json.loads` (previously all 11 failed).
- `"q":` counts identical before/after, per file; expanded total 761.
- Every question has exactly 4 options and a valid `ans` (0–3) — **except
  the one flagged question below**. Every question (761/761) has an
  `explanation`.
- **Lossless proof, stronger than the first repair:** the originals were parsed
  with `json.loads(..., strict=False)` (which tolerates raw control chars)
  and compared value-by-value with the repaired strict parse — **identical for
  all 10 control-character files**, not just the 3 sampled the first time.
  History cannot be checked that way (its doubled quotes fail even
  `strict=False`), but its file grew by exactly 2 bytes, i.e. only the two
  added backslashes.
- `git diff --stat`: only the 11 files changed — **1,026 insertions,
  24,859 deletions, identical to the first repair's diff stat**, confirming
  the same repair was reproduced.

## Two corrections to the first report's arithmetic

- The first report stated a total of 52,106 control characters escaped, but
  its own per-file table sums to 48,106. The per-file counts reproduce
  exactly here, so **48,106 is the correct total**; the first total was a
  mis-add.
- The first report stated WAEC Further Mathematics grew 40,055 → 77,347
  bytes. Escaping 12,452 controls adds exactly 12,452 bytes, so the correct
  size is 40,055 → 52,507 bytes, as measured here — and the lossless
  value-by-value check confirms the content is unchanged.

## Flagged — one pre-existing content defect, NOT repaired by guessing

**NECO_Computer_2024.json, question 13 (index 12), preserved exactly as-is:**
"In Microsoft Excel, the absolute cell reference for cell A1 is written as _____."

- It has **5 options**, not 4, and none contains a `$` sign. The intended
  options were almost certainly `$A$1` / `$A1` / `A$1` / `A1`, with the `$`
  signs lost when the file was generated.
- `ans` is 3, which is in range but points at an option that is not `$A$1`,
  so the question cannot be answered correctly as stored.
- The v2 importer / CBT must exclude any question without exactly 4 options,
  and this question needs its options re-sourced from the real NECO 2024
  Computer paper (or dropped) rather than guessed.

## Notes for the rebuild

- Root cause is the generator that wrote these files: it embedded raw
  newlines inside JSON strings instead of escaping them. Any future
  regeneration must emit valid JSON (`json.dumps` with escaping) or the same
  corruption returns.
- The repaired files in this durable clone are ready for the v2 question
  importer. The importer must still skip the 1 flagged question above.
- This durable clone lives under `~/workspace/` (not `/tmp`) so it will not
  disappear on a restart. It is still unpushed — pushing to GitHub needs a
  separate approval.
