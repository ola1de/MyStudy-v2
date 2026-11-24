# MyStudy v2 — Vocabulary (Part: Vocabulary)

Date: 24 November 2026. Repo: `ola1de/vocabulary-database` (worked on in
`/tmp/mystudy-repos/vocabulary-database/`, **not pushed to GitHub**).
Scripts (persisted): `~/workspace/mystudy/tools/vocab_audit.py`,
`vocab_fix.py`, `vocab_build_new.py`, `vocab_new_1.py` … `vocab_new_5.py`.
Original files backed up at `~/workspace/mystudy/tools/backup-24-nov-orig/`.

## 1. What the audit found (original 24 files, 2,400 words)

- 24 data files × 100 words = 2,400 words; 2,400 quiz questions.
- File shape: `{category, title, words: [{id, word, pos, definition, example}],
  quiz: [{id, question, options[4], answer (index), explanation}]}`.
  Quiz stems are all `Which word means: "<definition>"?`;
  explanations are `Word (pos) — definition`.
- **index.json was version 1 with 14 categories and no `count` field** — it did
  not list all 24 files. The 10 unlisted: admin-vocabulary, animal-habitats,
  capability-adjectives, environment, idioms, natural-phenomena, proverbs,
  professions, sensory-sounds, umbrella-terms.
- Entry defects: **98** (empty/missing fields, fragment definitions,
  definitions equal to the word, examples not containing the word).
  Quiz defects: **120** (42 answer mismatches, 30 duplicate stems,
  7 duplicate options, 41 "correct word not among options" — overlapping
  pairs per broken item).
- Duplicate words within a category: dietary-habits **10**, obsessions **15**,
  forms-of-government 2, personality-types 1, philosophical-stances 1,
  proverbs 1, time-and-frequency 1, words-for-killing 5.
- Global word-id collision: `ph-01`–`ph-50` used by both phobias and
  philosophical-stances.
- Wrong entries: dietary `dh-36` "Kaufmann" (a German surname, not a faster);
  obsessions `o-070` "Dinomania" defined as "Compulsion to dance" (it is
  fascination with dinosaurs); baby-animals `ba-051` "Aleven" defined
  "Baby swan (variant)" (alevin is a newly hatched fish); `ba-39` "Crias"
  (plural headword); words-for-killing `wfk-078` "Feoticide" (misspelling of
  Foeticide, which already exists); phobias `p-054` "Aerophobia (draft)" and
  `p-055` "Ailurophobia (severe)" (editing notes left in the words).
- Cross-category shared words: **51** (10 same-sense, 41 different-sense) —
  legitimate: the same word with a different sense in another category.
- Dictionary check (`mystudy-dic/processed/merged.json`, 121,340 entries):
  **2,014/2,400 (84%)** of original words verified. The 386 misses are
  overwhelmingly legitimate specialist terms the general dictionary lacks
  (e.g. Cattery, Biodiversity, Hepatologist, Multimeter, all -mania/-phobia/
  -cide terms). Standard adopted: verify against the dictionary where it
  covers the term; specialist terms kept only if standard, well-attested
  English. A dictionary miss alone does not make a word wrong.
- ID formats were inconsistent in the originals (e.g. `dh-01` vs `dh-067`;
  word-id prefixes differ per half in several files). Original files keep
  their ids (import must not assume a single prefix per file); all **new**
  files use consistent 3-digit ids.

## 2. What was fixed (all 24 existing categories)

- **249 entries changed** (verified by diff against the original backup) and
  **all 2,400 quiz items regenerated** (seeded `random.Random(category-slug)`;
  quiz[i] tests words[i]; 3 random distractors from the same file; answer =
  index of the correct word; explanation `Word (pos) — definition`).
- Duplicate words replaced with verified standard terms (e.g. dietary:
  Algivore, Planktivore, Vermivore, Pantophagist, Florivore, Omophagist,
  Gummivore, Baccivore, Graminivore, Ophiophagist, plus **Faster** for
  Kaufmann; obsessions: Oniomania, Phonomania, Numismatomania, Pteridomania,
  Ecdemomania, Thanatomania, Potomania, Morphinomania, Philomania, Lexomania,
  Polymania, Hippomania, Verbomania, Audiomania, Nomomania; phobias:
  **Didaskaleinophobia** for "Aerophobia (draft)", **Athazagoraphobia** for
  "Ailurophobia (severe)"; words-for-killing: Avunculicide, Androcide,
  Vitricide, Libericide, Decimation, Pogrom).
- Wrong definitions corrected (Dinomania → dinosaurs; Aleven → **Alevin**,
  "A newly hatched fish, still carrying its yolk sac."; Crias → **Cria**;
  Feoticide removed in favour of the existing Foeticide).
- Phobias word ids `ph-01`–`ph-50` renamed → `pho-01`–`pho-50`, removing the
  collision with philosophical-stances (which keeps `ph-`).
- Duplicate definitions disambiguated with "also called" clauses
  (collective-nouns bare terms: Convocation, Sleuth, Skulk, Prickle,
  Zeal/Dazzle, Ambush/Streak, Colony of ants, Family of otters, Glaring of
  cats, Hive of bees, Parade of elephants); phobias pairs reworded
  (Autophobia / Monophobia, Enochlophobia, Somniphobia); Flammable kept,
  Inflammable replaced with **Ignitable**; Bolometer/Radiometer reworded
  distinctly; Fleeting, Semiannual reworded.
- Fragment definitions under 15 characters expanded to full sentences
  (~30 entries, e.g. Byre, Apiology, Potable, Ichthyovore, Triumvirate,
  Pedometer, Somnambulist, Assailant, Slayer; phobias "Fear of X." →
  "An intense fear of X."). Short-but-complete definitions (e.g. "A young
  goat.", "The study of cells.") were left as-is — short ≠ wrong.
- Baby-animals `ba-053`–`ba-100` ("Baby X" with one-word definitions like
  "Kit."): kept the "Baby X" words (the file's per-animal design) but gave
  full-sentence definitions `A baby <animal> is called a <term>.` and
  rewrote ~25 examples to use "baby X" phrasing.
- Example fixes: measurement-instruments "AH meter" → "ampere-hour meter",
  "rangefinder" → "laser rangefinder"; medical-specialists abbreviations
  expanded (GP, SLP, RE, GI, "cardiac", "physician"); `kl-43` Slay example
  "slew" → "will slay"; proverbs `pv-049`/`pv-058` examples changed to quote
  the full proverb.
- Per-file changed-entry counts (diff vs original): baby-animals 51,
  phobias 78, dietary-habits 18, obsessions 18, collective-nouns 13,
  medical-specialists 12, words-for-killing 9, time-and-frequency 7,
  animal-habitats 6, philosophical-stances 6, proverbs 6,
  measurement-instruments 5, branches-of-study 4, forms-of-government 4,
  idioms 4, personality-types 4, capability-adjectives 3,
  one-word-substitutions 1; admin-vocabulary, environment,
  natural-phenomena, professions, sensory-sounds, umbrella-terms 0 entries
  changed (quiz still regenerated). Total 249.

## 3. New categories (20 × 100 words + 100 quiz = 2,000 words)

Subject vocabulary for every JAMB/WAEC subject not previously covered,
following the existing schema exactly:

| Category | Title | Word ids | Quiz ids |
|---|---|---|---|
| mathematics | Mathematics Vocabulary | math-001…100 | mat-q1…100 |
| further-mathematics | Further Mathematics Vocabulary | fma-001…100 | fmq-q1…100 |
| physics | Physics Vocabulary | phy-001…100 | phq-q1…100 |
| chemistry | Chemistry Vocabulary | che-001…100 | chq-q1…100 |
| biology | Biology Vocabulary | bio-001…100 | biq-q1…100 |
| economics | Economics Vocabulary | eco-001…100 | ecq-q1…100 |
| government | Government Vocabulary | gv-001…100 | gvq-q1…100 |
| geography | Geography Vocabulary | geo-001…100 | geq-q1…100 |
| literature | Literature Vocabulary | lit-001…100 | liq-q1…100 |
| commerce | Commerce Vocabulary | com-001…100 | cmq-q1…100 |
| accounting | Accounting Vocabulary | acc-001…100 | acq-q1…100 |
| agriculture | Agriculture Vocabulary | agr-001…100 | agq-q1…100 |
| crs | Christian Religious Studies Vocabulary | crs-001…100 | crq-q1…100 |
| irs | Islamic Religious Studies Vocabulary | irs-001…100 | irq-q1…100 |
| history | History Vocabulary | his-001…100 | hiq-q1…100 |
| civic-education | Civic Education Vocabulary | civ-001…100 | ciq-q1…100 |
| computer-studies | Computer Studies Vocabulary | cmp-001…100 | cpq-q1…100 |
| hausa | Hausa Vocabulary | hau-001…100 | huq-q1…100 |
| igbo | Igbo Vocabulary | igb-001…100 | ibq-q1…100 |
| yoruba | Yoruba Vocabulary | yor-001…100 | yoq-q1…100 |

- The 17 English subject categories use syllabus-standard terms (JAMB/WAEC
  subject coverage: e.g. history covers sources, periods, pre-colonial
  states/empires, colonial rule, constitutions, independence; government
  covers constitutions, federalism, parties, elections, ECOWAS, AU, UN).
- The 3 Nigerian-language categories (Hausa, Igbo, Yoruba) hold 100 common
  terms each — greetings, pronouns, question words, numbers 1–10/20/100/1000,
  family, body parts, nature/time, food, animals, verbs, everyday things —
  with English glosses as definitions and a sentence in the language as the
  example, with an English translation in parentheses, e.g. Hausa "Gida" —
  "Muna zama a gida. (We live in a house.)". Language glosses are
  one-word by nature ("Tea.", "Who."), so the definition-length minimum for
  those three files is 4 characters, not 10.
- Dictionary coverage for the new English words: **1,086 of 1,208**
  single-word terms (90%) verified in `merged.json`. The 122 not in the
  dictionary are standard specialist terms, proper names and abbreviations
  (e.g. IRS Arabic terms Sunnah, Shariah, Fiqh, Salah, Wudu; history names
  Ife, Oyo, Kano, Sokoto, Biafra, NCNC; Monomial, Trinomial, Eigenvector,
  Discriminant, Duopoly, Hyperinflation, ECOWAS, Anagnorisis, NPK,
  Intercropping, Olericulture, Agroforestry, Monogastric, Deworming,
  Motherboard, Linux, macOS, Pseudocode, Antivirus, SQL, Terabyte, ICT,
  Cybersecurity, Phishing, Bluetooth, USB, Touchscreen). Language-category
  words are not English and are excluded from dictionary coverage by design.

## 4. Index

- **index.json v3**: `{version: 3, categories: [{slug, title, file, count: 100}]}`,
  44 categories. Order: v1's 14 first, then the 10 previously unlisted
  (alphabetical), then the 20 new categories in subject order.
- All 44 files present, each 100 words + 100 quiz questions.

## 5. Final validation (24 Nov 2026, after all fixes and additions)

- 44 files, **4,400 words, 4,400 quiz questions**.
- **0 entry defects, 0 quiz defects.**
- No duplicate words, ids or definitions within any file; no duplicate word
  ids or quiz ids globally.
- Cross-category shared words: **240** (26 same-sense, 214 different-sense)
  — expected: the new subject categories legitimately share terms (e.g.
  "election" in government, civic-education and history; "soil" in
  geography and agriculture; "pastoralism" in geography and agriculture).
- Every file parses as JSON; every entry has all fields; every quiz item
  has 4 options and a valid answer.
- Validation tooling notes: the example-containment check is Unicode-aware
  (Hausa/Igbo/Yoruba letters ɗ ƙ ụ ọ ẹ ṣ and tone marks), treats an
  apostrophe-joined word as both the joined form and its parts (Igbo
  "n'ụlọ"), and treats "someone's"/"one's" (and bare "someone") as satisfied
  by any possessive pronoun in the example. The builder rebuilds index.json
  from an explicit v1 order, not from a possibly stale index file.

## 6. What must be fixed before import — nothing outstanding

All audit defects are fixed and the full audit passes with 0 defects.
Notes for the importer, not blockers:

- Original files keep their inconsistent id prefixes (e.g. `dh-01` vs
  `dh-067`; branches-of-study `st`/`bos`). Import by `id` value, not by
  prefix pattern; new files use consistent 3-digit ids.
- Cross-category shared words (240) are by design; do not de-duplicate
  across categories — the same word often carries a different sense in
  another category.
- Quiz items are generated deterministically per category
  (`random.Random(category-slug)`); re-running the builder reproduces them.
- Nothing was pushed to GitHub. To publish: review the diff in
  `/tmp/mystudy-repos/vocabulary-database/` (`git status`: 24 modified
  files + 20 new files) and push from there.
