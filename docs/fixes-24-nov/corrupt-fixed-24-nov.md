# Corrupt exam JSON files — fixed (24 Nov 2026)

Repo: `ola1de/Exam-Questions-Data` (local clone `/tmp/mystudy-repos/Exam-Questions-Data`,
shallow). Work done in the clone only — **nothing pushed to GitHub**.
Scope: the 11 corrupt files only. No other file was touched
(`git status` shows only these 11 modified; the untracked
`json/.orig-placeholders-*/` directories are from the parallel placeholder-filling
work, not this repair).

## Result

**11 / 11 files repaired and now parse with `json.loads`. 761 questions recovered
(760 fully valid + 1 flagged, see below). 761 / 761 have explanations.**
`"q":` counts are identical before and after for every file, and every answer index
is a valid 0–3 int.

## Method (lossless, syntax-only)

1. Read each file as bytes (no newline translation) and decoded UTF-8, so the
   files' CRLF line endings are preserved exactly.
2. Walked the text tracking in-string vs out-of-string state and escaped raw
   control characters found **inside** string values only (`\r` → `\\r`,
   `\n` → `\\n`, `\t` → `\\t`, other controls → `\\u00XX`). Structural CRLF
   line breaks outside strings were left untouched.
3. One targeted fix in `NECO_History_2025.json`: the passage content was wrapped
   in doubled quotes (`"content": ""The history ... oppressed.""`). The inner
   quotes were escaped (`"\"The history ... oppressed.\""`); no characters were
   removed.
4. No question text, option, answer index, or explanation was changed, added, or
   removed. Nothing was invented.

Why the diffs look large: the raw newlines inside string values were acting as
physical line breaks, so one question could span dozens of lines. Escaping them
merges those lines (e.g. Further Mathematics: 6,095 lines touched, mostly
deletions of phantom line breaks). The parsed content is unchanged — verified
below.

## Per-file report

| File | Original error | Fix applied | Questions recovered |
|---|---|---|---|
| NECO_Chemistry_2024.json | Invalid control character, line 9 col 29 | Escaped 3,635 raw control chars in strings | 70 |
| NECO_Computer_2024.json | Invalid control character, line 76 col 17 | Escaped 18 raw control chars in strings | 70 (1 flagged, see below) |
| NECO_FurtherMath_2024.json | Invalid control character, line 3 col 10 | Escaped 11,291 raw control chars in strings | 70 |
| NECO_Geography_2024.json | Invalid control character, line 210 col 33 | Escaped 60 raw control chars in strings (incl. a raw tab) | 70 |
| NECO_History_2025.json | Expecting ',' delimiter, line 94 col 14 | Escaped doubled quotes around passage content; 0 control chars | 71 (incl. 2 passage questions) |
| NECO_Mathematics_2024.json | Invalid control character, line 3 col 16 | Escaped 8,393 raw control chars in strings | 70 |
| NECO_Physics_2024.json | Invalid control character, line 6 col 43 | Escaped 4,211 raw control chars in strings | 70 |
| WAEC_Chemistry_2024.json | Invalid control character, line 14 col 18 | Escaped 5,081 raw control chars in strings | 70 |
| WAEC_FurtherMath_2024.json | Invalid control character, line 3 col 26 | Escaped 12,452 raw control chars in strings | 60 |
| WAEC_Geography_2024.json | Invalid control character, line 25 col 46 | Escaped 25 raw control chars in strings | 70 |
| WAEC_Physics_2024.json | Invalid control character, line 10 col 11 | Escaped 2,940 raw control chars in strings | 70 |

Total control characters escaped: 52,106. File sizes grew accordingly
(e.g. WAEC Further Mathematics 40,055 → 77,347 bytes) because each escaped
control character gains a backslash; content is unchanged.

## Verification

- Every file parses with strict `json.loads` (previously all 11 failed).
- `"q":` and `"opts"` counts identical before/after, per file.
- Every question has exactly 4 options and a valid `ans` (0–3) — **except one
  flagged question below**. Every question (761/761) has an `explanation`.
- **Lossless proof:** the originals were parsed with `json.loads(..., strict=False)`
  (which tolerates raw control chars) and compared value-by-value with the
  repaired strict parse — identical for NECO_Chemistry_2024, WAEC_FurtherMath_2024
  and NECO_Computer_2024 (the three files sampled, covering both error types).
  A spot check confirms repaired string values still contain the original CRLF
  characters (e.g. NECO Chemistry Q2 still reads `An atom of an element \r\n𝑋\r\nX\r\n has …`).
- `git diff --stat` (scoped to `json/`): only the 11 files changed.

## Flagged — one pre-existing content defect, NOT repaired by guessing

**NECO_Computer_2024.json, question 13 (index 12):**
"In Microsoft Excel, the absolute cell reference for cell A1 is written as _____."

- It has **5 options**, not 4: `A1`, `𝐴1`, `𝐴A1`, `A1`, `𝐴A1` (newlines omitted here
  for readability). None of the options contains a `$` sign — the whole file
  contains only one `$`, in the explanation ("The dollar signs ($) before the
  column letter and row number lock the reference…"). The intended options were
  almost certainly `$A$1` / `$A1` / `A$1` / `A1`, with the `$` signs lost when the
  file was generated.
- `ans` is 3, which is in range but points at an option that is not `$A$1`, so the
  question cannot be answered correctly as stored.
- This defect is in the source data (confirmed by parsing the original with
  `strict=False` — the 5 options are there before any repair). The question was
  preserved exactly as stored and is **not** silently fixed: the v2 importer /
  CBT must exclude any question without exactly 4 options, and this question
  needs its options re-sourced from the real NECO 2024 Computer paper (or
  dropped) rather than guessed.

## Notes for the rebuild

- The root cause is the generator that wrote these files: it embedded raw
  newlines (and unicode-plus-ASCII formula duplications such as `𝑋\r\nX\r\n`)
  inside JSON strings instead of escaping them. Any future regeneration must
  emit valid JSON (`json.dumps` with escaping) or the same corruption returns.
- The repaired files are ready for the v2 question importer. The importer must
  still skip the 1 flagged question above.
