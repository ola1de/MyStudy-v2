# Placeholders filled — merged manifest, 24 Nov 2026

**Scope:** all 190 placeholder exam files in `~/workspace/mystudy/data-repos/Exam-Questions-Data/json/` (durable clone; the `/tmp` clone was wiped and all `/tmp` work was lost and redone from the durable clone).
**Result: 190 / 190 files filled, 8,580 practice questions added, 0 placeholders remaining.**
Nothing pushed to GitHub. The 11 corrupt files were fixed by a separate agent and are NOT part of this manifest — verified here: all 11 now parse.

## Totals (independently verified by the coordinator, reading only the written JSON)

| Group | Files | Questions | Answer distribution (A/B/C/D) | Verified |
|---|---|---|---|---|
| JAMB (2020 + Hausa 2023) | 22 | 900 | 900 / 0 / 0 / 0 | All parse; 4 distinct options; 0 bad ans; 0 missing practice/source; 0 internal dups |
| WAEC (2020–2023) | 84 | 4,240 | 1,034 / 1,113 / 1,050 / 1,043 | All parse; 0 bad ans; 0 missing practice/source/explanation; 0 internal dups |
| NECO (2020–2023) | 84 | 3,440 | 701 / 869 / 1,054 / 816 | All parse; 0 bad ans; 0 missing practice/source/explanation; 0 internal dups |
| **Total** | **190** | **8,580** | — | **0 placeholders remaining; 0 files with internal duplicates** |

Per-file manifests: [placeholders-jamb-24-nov.md](placeholders-jamb-24-nov.md), [placeholders-waec-24-nov.md](placeholders-waec-24-nov.md), [placeholders-neco-24-nov.md](placeholders-neco-24-nov.md).
Backups of all 190 originals: `orig-placeholders-jamb/` (22), `orig-placeholders-waec/` (84), `orig-placeholders-neco/` (84).
Generators: JAMB `jamb-gen/`; WAEC `~/workspace/mystudy/gen-waec/`; NECO `gen_base.py`, `gen_neco.py`, `gen_topup.py`, `run_neco.py`, `validation-neco-24-nov.json`.

## Counts per file

- JAMB: English 60 (3 passages + 40 std), Literature 40 (1 poem + 1 passage + 30 std), other 20 files 40 each.
- WAEC: 50 per file; English 60 per file incl. 2 original comprehension passages.
- NECO: 40 per file; English 60 per file (50 std + 2 passages of 5), Literature 40 per file (35 std + 1 poem passage of 5).

## Honest labelling (on every question)

Every question carries `"practice": true` and a `source` naming the syllabus topic plus adaptation provenance, e.g. "MyStudy Practice Set — modelled on the JAMB/WAEC/NECO syllabus for this subject, not the official <year> paper". These are **syllabus-modelled practice sets, NOT verbatim official papers**. No question was copied verbatim from the real 2021–2025 files (checked by normalised-text hash; JAMB 0 matches vs 104 real files / 4,642 hashes; WAEC 122 matches dropped and replaced; NECO 14 matches dropped vs 1,223 real 2024/2025 questions).

## Sources used (online first, per the user update)

- Official JAMB IBASS syllabus PDFs (MD5-verified via jambsyllabus.com, 9/9 overlaps), 478 syllabus topics across 19 subjects; WAEC syllabus sites; NECO syllabus via neco.gov.ng (no direct PDF fetchable — third-party summaries used).
- JAMB Master archive (12,166 real JAMB questions) and the repo's own real 2021–2025 files for topic coverage and style.
- **No bulk free download of the actual WAEC or NECO 2020–2023 papers was obtainable** (WAEC: WikiQuestions 2020–2025 Maths pages marked unavailable, WAEC e-Learning has no PDF downloads; NECO: 9japastquestions needs an account, ExamPadi/ExamCoach/TestaCBT free tiers capped). Recorded in the per-group manifests; fallback was repo past questions + syllabus topics.

## Verification

- All 190 files parse as JSON; every question has 4 distinct options, `ans` in 0–3, `practice: true`, a `source`, and an `explanation` (0 missing across all 8,580, per coordinator check).
- JAMB: 36/36 numeric spot-checks recomputed independently and passed.
- WAEC: 14 numeric + 14 fact/language answers hand-verified.
- NECO: all 3,440 written answers machine-checked against their source pool; 115 pool items with colliding distractors + 1 wrong correct value (density 4/5 fixed to 0.8) fixed at source and re-checked to 0 bad items. 6 apparent mismatches were same-text collisions across subjects with equivalent correct wordings — every written answer is correct for its own source item.
- No duplicates within any file; no question shared across the 4 years of a NECO subject (driver-checked).

## Shortfalls and open fixes (do NOT go live without the first one)

1. **JAMB answer position: correct answer is ALWAYS at index 0 (900/900).** Needs a shuffle pass randomising option order + `ans` before live use, or the CBT loader must shuffle at display time. WAEC is balanced; NECO is C-heavy (A 701, B 869, C 1,054, D 816) and should also be rebalanced in the same pass.
2. **WAEC cross-year overlap:** only Maths and English are fully disjoint across years; 17 subjects share 9–33 questions per year-pair (syllabus-fact pools of 77–129 are smaller than 4×50=200 slots). Fully disjoint sets need pools expanded to ~200 distinct questions per subject.
3. **Civic and Further Maths have no JAMB UTME syllabus** — built from the WAEC syllabus instead (recorded in the JAMB manifest).
4. **Hausa/Igbo/Yoruba:** full in-language sets in all three groups, spot-checked correct. WAEC sets have no comprehension passages (unlike real papers); literature coverage is a few well-known works only. The ambiguous Igbo ("tooth","eze") entry was deliberately not used.
5. **WAEC generic distractors:** 39/4,240 (0.9%) use "None of the above" etc., only as distractors.
6. Audit note: repo file count was 389 JSON at snapshot vs 390 counted earlier — unresolved, not one of the 190 files.
