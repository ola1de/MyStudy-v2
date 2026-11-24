# Duplicates — correction report, 24 Nov 2026

Scope: the MyStudy repos cloned at `/tmp/mystudy-repos/`. Exam-Questions-Data **JSON** files were NOT touched (other agents own those — at the time of writing that clone shows the parallel corrupt/placeholder fix in progress: 11 JSON files modified plus `json/.orig-placeholders-*/` backup dirs).

Method: comparisons use normalised text — lowercase, HTML tags stripped, LaTeX `$` stripped, whitespace collapsed. A question is a "duplicate" only if its normalised question text + all 4 options + answer index all match. Question-text-only matches are reported separately, because two questions can share a stem with different options/answers.

Nothing was pushed to GitHub. All changes below are uncommitted in the local clones.

## 1. English-Quiz — Old* files archived, 0 questions merged

Result: **every Old file is a strict subset of its current counterpart — identical questions, only without explanations.** 0 Old-only questions exist, so 0 questions were merged.

| Old file | Old entries | Expanded Qs | Current file | Current expanded Qs | Old-only Qs | Difference |
|---|---|---|---|---|---|---|
| OldGeneral English Knowledge.json | 100 | 100 | General English Knowledge.json | 100 | 0 | Current adds `exp` to all 100 |
| OldGrammar.json | 100 | 100 | Grammar.json | 100 | 0 | Current adds `exp` to all 100 |
| OldLanguage Skills.json | 92 | 100 | Language Skills.json | 100 | 0 | Current adds `exp` to all 100 (90 std + 10 passage Qs) |
| OldListening Skills.json | 100 | 100 | Listening Skills.json | 100 | 0 | Current adds `exp` to all 100 |
| OldLiterature.json | 100 | 100 | Literature.json | 100 | 0 | Current adds `exp` to all 100 |
| OldParts of Speech.json | 100 | 100 | Parts of Speech.json | 100 | 0 | Current adds `exp` to all 100 |
| OldReading Comprehension.json | 10 | 100 | Reading Comprehension.json | 100 | 0 | Current adds `exp` to all 100 passage Qs |
| OldVocabulary.json | 100 | 100 | Vocabulary.json | 100 | 0 | Current adds `exp` to all 100 |
| OldWriting Skills.json | 100 | 100 | Writing Skills.json | 100 | 0 | Current adds `exp` to all 100 |

Action taken: all 9 Old files moved with `git mv` to `archive/` in the English-Quiz clone — history is preserved, nothing deleted. Verified after the move: `git diff --cached --stat` shows 9 renames, **0 insertions, 0 deletions** (pure moves, no content change), and all 18 files (9 current + 9 archived) still parse as JSON.

Remaining duplicate, NOT fixed (needs an owner decision): `Parts of Speech.json` contains the same question twice — entries #20 and #92, "In the sentence, 'They went there yesterday,' the underlined word is a/an:" — same options, same answer (adverb of place), but **different explanations**. It is a true duplicate (99 unique questions in a 100-question file), present in both the Old and the current file. The v2 importer dedups by content hash, so it will collapse to one entry; which explanation to keep is a content decision, so the file was left as-is. The same within-file duplicate does not occur in any other English-Quiz file.

## 2. vocabulary-database — index.json rebuilt: 14 → 24 categories

Before: `index.json` (version 1) listed 14 of 24 category files. Missing: admin-vocabulary, animal-habitats, capability-adjectives, environment, idioms, natural-phenomena, professions, proverbs, sensory-sounds, umbrella-terms.

After: `index.json` rewritten as **version 2**, same `{version, categories}` shape plus a `count` field per category (word count, counted from each file's `words` array). Verified: every listed file exists, every `.json` file in the repo is listed, slugs are unique, total 2,400 words.

| Slug | Title | File | Words | Quiz |
|---|---|---|---|---|
| one-word-substitutions | One-Word Substitutions | one-word-substitutions.json | 100 | 100 |
| phobias | Phobias | phobias.json | 100 | 100 |
| medical-specialists | Medical Specialists | medical-specialists.json | 100 | 100 |
| dietary-habits | Dietary Habits | dietary-habits.json | 100 | 100 |
| forms-of-government | Forms of Government | forms-of-government.json | 100 | 100 |
| branches-of-study | Branches of Study | branches-of-study.json | 100 | 100 |
| words-for-killing | Words for Killing | words-for-killing.json | 100 | 100 |
| obsessions | Obsessions & Manias | obsessions.json | 100 | 100 |
| baby-animals | Baby Animals | baby-animals.json | 100 | 100 |
| time-and-frequency | Time and Frequency | time-and-frequency.json | 100 | 100 |
| measurement-instruments | Measurement Instruments | measurement-instruments.json | 100 | 100 |
| collective-nouns | Collective Nouns | collective-nouns.json | 100 | 100 |
| personality-types | Personality Types | personality-types.json | 100 | 100 |
| philosophical-stances | Philosophical Stances | philosophical-stances.json | 100 | 100 |
| admin-vocabulary | Administrative Vocabulary | admin-vocabulary.json | 100 | 100 |
| animal-habitats | Where Animals Are Kept | animal-habitats.json | 100 | 100 |
| capability-adjectives | Capability Adjectives | capability-adjectives.json | 100 | 100 |
| environment | Environment & Ecology | environment.json | 100 | 100 |
| idioms | Idioms | idioms.json | 100 | 100 |
| natural-phenomena | Natural Phenomena | natural-phenomena.json | 100 | 100 |
| professions | Professions | professions.json | 100 | 100 |
| proverbs | Proverbs | proverbs.json | 100 | 100 |
| sensory-sounds | Sensory Sounds | sensory-sounds.json | 100 | 100 |
| umbrella-terms | Umbrella Terms | umbrella-terms.json | 100 | 100 |

(The original 14 keep their original order; the 10 added ones follow alphabetically. Titles and slugs are taken from each file's own `title` / `category` fields, not invented.)

Duplicate notes for vocabulary (reported, not edited — no vocabulary entries were changed):
- Every file has exactly 100 words and 100 quiz questions, no duplicate ids.
- Same word appearing twice **within** one file is usually a different sense, not a copy: e.g. obsessions has 15 repeated words, but 14 of them carry different definitions (egomania, melomania, etc. listed twice with different senses). Only **3 exact duplicates** (same word + same definition) exist in the whole set, all in dietary-habits.json (ravenous, peckish, abstemious). Those 3 should be removed at import time, not by hand-editing the file here.
- 51 words appear in more than one category (e.g. "quorum" in admin-vocabulary and one-word-substitutions, "referendum" in three categories). That is legitimate cross-category reuse, not duplication — the importer should key words per category.
- 2,311 distinct words across the 24 files, out of 2,400 entries.
- Quiz-question text repeats within some files (baby-animals 22, collective-nouns 12, phobias 3, dietary-habits 3, time-and-frequency 2, capability-adjectives 1, measurement-instruments 1, obsessions 1) — mostly the same definition stem asked twice. Flagged for the quiz importer to dedup; files left as-is.

## 3. mystudy-dic — which file the v2 importer should use

No file was deleted or changed (deletion needs the owner — the three copies total ~71 MB). Verified counts and subset relations:

| Copy | Keys | Shape of MEANINGS |
|---|---|---|
| `data/a.json` … `data/z.json` (26 raw files) | **158,265** distinct keys (sum = distinct, no overlap between letter files) | Dict: `{"1": [...], "2": [...]}` |
| `processed/merged.json` | **121,340** | List: `[[...], [...]]` (converted by `merge.py`) |
| `processed/filtered.json` | **121,297** | List, kid-safe filtered |

Subset relations (verified key-by-key): `filtered ⊂ merged ⊂ data`. Filtered is merged minus 43 words, plus some meanings/synonyms/antonyms stripped by `filter.py`. Merged is a strict subset of the raw data keys — **36,925 keys present in `data/` are missing from `merged.json`**, so the shipped `merged.json` is stale relative to the raw files (it was generated from an older/smaller data set, not from the current `data/`). Values also differ in shape only: merged converts each word's MEANINGS dict into a list, so a key-by-key value comparison against `data/` does not match literally, but the content is the same entries re-shaped.

**Importer instruction: use `processed/merged.json` (121,340 keys) as the single dictionary source, server-side only — never ship it to the browser.** Do not import all three copies; that would triple-load the same words. Do not use `filtered.json` unless the kid-safe version is wanted (it drops 43 words and strips some meanings). If full 158,265-key coverage is wanted, re-run the repo's own `merge.py` against the current `data/` instead of trusting the stale `merged.json` — but note `filter.py` cannot run as shipped: it reads `data/filter_words.txt`, which does not exist in the repo, so the filtered build is not reproducible until that file is restored.

Source note: the README states these are the output files of tusharlock10's dictionary repo (via Dropbox/Stack Overflow) — the raw `data/` files are upstream data, not the user's own writing.

## 4. Exam-Questions-Data TXT banks — mostly NEW content, not duplicates

The 14 root `*.txt` files were **not edited**. Parsed with a parser accepting both `A)` and `A.` option markers (Physics uses `A.` for most questions — a `A)`-only parser finds just 2 of its 39 questions).

| File | Blocks | Parsed | Unparsed | Within-file dups (full key) | In JSON bank (full key) | In JSON bank (question text only) | Unique new question texts |
|---|---|---|---|---|---|---|---|
| Accounting.txt | 250 | 250 | 0 | 0 | 0 | 1 | 248 |
| Agricultural Science.txt | 250 | 249 | 1 | 0 | 0 | 1 | 248 |
| Biology.txt | 137 | 137 | 0 | 0 | 0 | 0 | 137 |
| Chemistry.txt | 250 | 250 | 0 | 0 | 0 | 3 | 247 |
| Christian Religious Knowledge (CRK).txt | 250 | 249 | 1 | 0 | 0 | 0 | 249 |
| Commerce.txt | 250 | 249 | 1 | 0 | 0 | 0 | 249 |
| Economics.txt | 250 | 250 | 0 | 0 | 0 | 2 | 248 |
| English Language.txt | 245 | 244 | 1 | 0 | 0 | 0 | 244 |
| Geography.txt | 250 | 250 | 0 | 0 | 0 | 0 | 250 |
| Government.txt | 250 | 249 | 1 | 0 | 0 | 1 | 248 |
| Islamic Religious Knowledge (IRK).txt | 112 | 112 | 0 | 0 | 0 | 0 | 112 |
| Literature-in-English.txt | 190 | 190 | 0 | 2 (qtext) | 0 | 0 | 188 |
| Mathematics.txt | 50 | 50 | 0 | 5 | 0 | 1 | 44 |
| Physics.txt | 39 | 39 | 0 | 0 | 0 | 1 | 38 |
| **Total** | **2,773** | **2,768** | **5** | **8** | **0** | **10** | **2,750** |

Conclusion: the TXT banks are **essentially new content, not duplicates of the JSON banks** — 0 of 2,768 parsed questions match a JSON question exactly (same stem + options + answer), and only 10 share even the same question stem. They add **2,750 unique new question texts**. They must be imported (after the fixes below), not discarded as duplicates. Per the user's rule (24 Nov), all questions must come from past questions and the syllabus — these TXT banks are unattributed practice-style banks, so the importer should tag them `practice: true` with source `txt-bank`, exactly like the syllabus-modelled practice sets filling the placeholder files, and never present them as verbatim official papers.

### Truncated subjects — verified counts
- **Mathematics: 50 blocks, 45 unique** (5 questions repeated verbatim: simple interest on ₦4,000 at 5% for 2 years; (1/2)^-2; range of 10, 15, 20, 25; "if a=2 and b=3, find a² + b"; "solve 0.2x = 4"). Also contains a malformed embedded fragment: "Simplify the square root of Question: Calculate the simple…" — one question stem swallowed the start of the next, which is why a naive `"Question:"` count gives 51.
- **Physics: 39** — confirmed. One broken option: "The escape velocity from Earth's surface is approx?" has option C as the empty string `C.  m/s` (the number is missing; correct answer is B, 11.2 km/s, so the question is usable only if option C is repaired or the question dropped).
- **IRK: 112** — confirmed.
- **Biology: 137** — confirmed (an earlier count of 136 missed the first question, which starts at file offset 0 with no preceding newline).
- **Literature-in-English: 190** — confirmed, with 2 within-file duplicate stems.

### The 5 unparsed blocks (fix or drop at import — files left untouched)
1. Agricultural Science, block 90: "What is the chemical formula for Urea?" — only option A given, and it is empty; Answer: A. Truncated question.
2. CRK, block 230: "The 'Alpha and Omega' means?" — only options A–C, option D missing; Answer: C.
3. Commerce, block 203: "SWOT stands for?" — only options A–C, option D missing; Answer: C.
4. English Language, block 83: "Identify the word with the primary stress on the first syllable." — option D is printed as `) Believe` (the letter D is missing); Answer: C.
5. Government, block 138: "The 1989 Constitution was never fully implemented…" — a True/False question with only 2 options; Answer: A. Valid as a 2-option question, but it does not fit the 4-option schema.

## Changes made (local clones only, not pushed)

- English-Quiz: 9 × `git mv` — Old* files → `archive/` (pure renames, 0 content changes).
- vocabulary-database: `index.json` rewritten (v1 → v2, 14 → 24 categories, `count` added per category).
- mystudy-dic: no changes. Exam-Questions-Data TXT files: no changes. Exam-Questions-Data JSON files: not touched.

## Left for the owner / importer

1. Parts of Speech duplicate (#20 vs #92) — pick which explanation to keep.
2. Vocabulary: 3 exact duplicate entries in dietary-habits.json; quiz-question repeats in 8 files (worst: baby-animals 22) — dedup at import.
3. Dictionary: decide merged (121,340) vs re-running `merge.py` for the full 158,265; restore `data/filter_words.txt` if the filtered build is ever needed again.
4. TXT banks: repair or drop the 5 unparsed blocks + the broken Physics option C, dedup the 8 within-file repeats, then import the remaining ~2,750 questions tagged `practice: true`, source `txt-bank`.
