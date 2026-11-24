# Vocabulary Expansion Manifest — 24 November 2026

Repo: `ola1de/vocabulary-database`, worked on in
`/tmp/mystudy-repos/vocabulary-database/` (**not pushed to GitHub**).
Original files backed up at `~/workspace/mystudy/tools/backup-24-nov-orig/`.
Scripts: `~/workspace/mystudy/tools/vocab_audit.py`, `vocab_fix.py`,
`vocab_build_new.py`, `vocab_new_1.py` … `vocab_new_5.py`.

## Totals

| | Before | After |
|---|---|---|
| Categories in repo | 24 | **44** |
| Categories listed in index.json | 14 (v1, no counts) | **44 (v3, count 100 each)** |
| Words | 2,400 | **4,400** |
| Quiz questions | 2,400 | **4,400** |
| Entry defects | 98 | **0** |
| Quiz defects | 120 | **0** |

## A. Existing categories — fixed, counts unchanged (100 → 100 words, 100 → 100 quiz)

All 24 original categories were kept at 100 words / 100 quiz. The work was
fixing defects and regenerating every quiz item. "Entries changed" is the
verified diff against the original backup (word, definition or example
changed); every quiz item in every file was regenerated.

| Category (file) | Words before → after | Quiz before → after | Entries changed |
|---|---|---|---|
| one-word-substitutions | 100 → 100 | 100 → 100 | 1 |
| phobias | 100 → 100 | 100 → 100 | 78 |
| medical-specialists | 100 → 100 | 100 → 100 | 12 |
| dietary-habits | 100 → 100 | 100 → 100 | 18 |
| forms-of-government | 100 → 100 | 100 → 100 | 4 |
| branches-of-study | 100 → 100 | 100 → 100 | 4 |
| words-for-killing | 100 → 100 | 100 → 100 | 9 |
| obsessions | 100 → 100 | 100 → 100 | 18 |
| baby-animals | 100 → 100 | 100 → 100 | 51 |
| time-and-frequency | 100 → 100 | 100 → 100 | 7 |
| measurement-instruments | 100 → 100 | 100 → 100 | 5 |
| collective-nouns | 100 → 100 | 100 → 100 | 13 |
| personality-types | 100 → 100 | 100 → 100 | 4 |
| philosophical-stances | 100 → 100 | 100 → 100 | 6 |
| admin-vocabulary | 100 → 100 | 100 → 100 | 0 |
| animal-habitats | 100 → 100 | 100 → 100 | 6 |
| capability-adjectives | 100 → 100 | 100 → 100 | 3 |
| environment | 100 → 100 | 100 → 100 | 0 |
| idioms | 100 → 100 | 100 → 100 | 4 |
| natural-phenomena | 100 → 100 | 100 → 100 | 0 |
| proverbs | 100 → 100 | 100 → 100 | 6 |
| professions | 100 → 100 | 100 → 100 | 0 |
| sensory-sounds | 100 → 100 | 100 → 100 | 0 |
| umbrella-terms | 100 → 100 | 100 → 100 | 0 |
| **Total existing** | **2,400 → 2,400** | **2,400 → 2,400** | **249** |

Defects fixed in these files: 98 entry defects (empty/missing fields,
fragment or circular definitions, examples not containing the word, duplicate
words, wrong definitions — e.g. "Kaufmann", "Dinomania", "Aleven",
"Feoticide", "Aerophobia (draft)") and 120 quiz defects (42 answer
mismatches, 30 duplicate stems, 7 duplicate options, 41 correct-word-not-
among-options). The phobias/philosophical-stances word-id collision
(`ph-01`–`ph-50`) was removed by renaming phobias ids to `pho-01`–`pho-50`.

## B. New categories — added (0 → 100 words, 0 → 100 quiz each)

| Category (file) | Words before → after | Quiz before → after | Notes |
|---|---|---|---|
| mathematics | 0 → 100 | 0 → 100 | JAMB/WAEC maths: number, algebra, geometry, trigonometry, statistics |
| further-mathematics | 0 → 100 | 0 → 100 | Matrices, vectors, complex numbers, calculus, logic, probability |
| physics | 0 → 100 | 0 → 100 | Mechanics, waves, electricity, optics, modern physics |
| chemistry | 0 → 100 | 0 → 100 | Atomic structure, bonding, reactions, organic, electrochemistry |
| biology | 0 → 100 | 0 → 100 | Cells, genetics, ecology, physiology, evolution, classification |
| economics | 0 → 100 | 0 → 100 | Demand/supply, market structures, money, trade, development |
| government | 0 → 100 | 0 → 100 | Constitutions, federalism, parties, elections, ECOWAS, AU, UN |
| geography | 0 → 100 | 0 → 100 | Physical, human, economic geography, map work, Nigeria |
| literature | 0 → 100 | 0 → 100 | Genres, devices, drama, poetry, prose, African literature |
| commerce | 0 → 100 | 0 → 100 | Trade, business documents, marketing, insurance, transport |
| accounting | 0 → 100 | 0 → 100 | Double entry, ledgers, final accounts, partnership, company accounts |
| agriculture | 0 → 100 | 0 → 100 | Crops, livestock, soil, farm management, agricultural economics |
| crs | 0 → 100 | 0 → 100 | Old/New Testament, teachings of Jesus, Christian living |
| irs | 0 → 100 | 0 → 100 | Qur'an, Hadith, pillars, jurisprudence, Islamic history |
| history | 0 → 100 | 0 → 100 | Sources, pre-colonial states/empires, colonial rule, constitutions, independence |
| civic-education | 0 → 100 | 0 → 100 | Citizenship, rights/duties, values, democracy, national symbols |
| computer-studies | 0 → 100 | 0 → 100 | Hardware, software, programming, networks, data, security |
| hausa | 0 → 100 | 0 → 100 | 100 common terms, English glosses, Hausa example + translation |
| igbo | 0 → 100 | 0 → 100 | 100 common terms, English glosses, Igbo example + translation |
| yoruba | 0 → 100 | 0 → 100 | 100 common terms, English glosses, Yoruba example + translation |
| **Total new** | **0 → 2,000** | **0 → 2,000** | |

## C. Index

- Before: index.json **v1**, 14 categories, no `count` field; 10 existing
  categories unlisted.
- After: index.json **v3**, **44 categories**, each with `count: 100`.
  Order: v1's 14 first, then the 10 previously unlisted (alphabetical), then
  the 20 new categories in subject order.

## D. Sources used

1. **Dictionary verification** — `/tmp/mystudy-repos/mystudy-dic/processed/
   merged.json` (121,340 entries, `{word: {MEANINGS: [[POS, definition…]]}}`).
   - Original 24 categories: 2,014/2,400 words (84%) verified in the
     dictionary.
   - New English categories: 1,086/1,208 single-word terms (90%) verified.
   - Rule applied throughout: verify against the dictionary where it covers
     the term; specialist terms kept only if standard, well-attested English.
     A dictionary miss alone does not make a word wrong. No word was included
     that could not be verified as correct standard English (or, for the
     language categories, as a correct common term of that language).
2. **JAMB/WAEC syllabuses** — subject coverage for the 17 new English subject
   categories follows the published JAMB/UTME and WAEC syllabus topic areas
   (terms are standard syllabus vocabulary, not past-paper questions).
3. **Standard reference knowledge** — word-formation families for specialist
   terms (-mania, -phobia, -cide, -vore), Nigerian history (pre-colonial
   states, constitutions 1922–1960, independence), CRS/IRS doctrine and
   terminology, and the three Nigerian languages' standard everyday
   vocabulary (greetings, numbers, family, body, food, verbs).
4. **Repo itself** — the existing 24 files defined the schema, quiz shape
   (`Which word means: "<definition>"?`, 4 options, answer index,
   explanation `Word (pos) — definition`) and file format
   (`json.dump(indent=2, ensure_ascii=False)`, no trailing newline).

## E. Single-word terms NOT in the dictionary (122) — kept on standard-usage grounds

These were checked as standard terms, proper names or abbreviations; none was
invented. Grouped by category:

- mathematics: Monomial, Trinomial, Factorisation, HCF
- further-mathematics: Directrix, Eigenvector, Contrapositive, Discriminant
- chemistry: Neutralisation, Polymerisation
- biology: Decomposer
- economics: Duopoly, Nationalisation, Privatisation, HDI, Hyperinflation
- government: ECOWAS
- geography: Landform, Pastoralism, Nomadism
- literature: Anagnorisis
- commerce: Standardisation
- agriculture: NPK, Intercropping, Pastoralism, Olericulture, Agroforestry,
  Mechanisation, Monogastric, Deworming
- irs: Sunnah, Shariah, Fiqh, Iman, Adhan, Salah, Wudu, Ghusl, Tayammum,
  Sawm, Umrah, Shahadah, Tawhid, Haram, Makruh, Fard, Sadaqah, Khutbah,
  Taraweeh, Iftar, Suhoor, Hijrah, Surah, Juz, Hifz, Hafiz, Tafsir, Tajwid,
  Ijtihad, Ijma, Qiyas, Madhhab, Hanafi, Maliki, Hanbali, Ummah, Khalifah,
  Umar, Uthman, Khadijah, Aisha, Bilal, Jibril, Iblis, Jannah, Jahannam,
  Barzakh, Qiyamah, Mizan, Sirat, Akhirah, Dunya, Taqwa, Sabr, Shukr,
  Ikhlas, Tawakkul, Istighfar, Dhikr, Dua, Bismillah, Alhamdulillah
- history: Ife, Oyo, Kano, Sokoto, Calabar, Biafra, Nupe, Tiv, Ibibio, Efik,
  Ijaw, NCNC
- civic-education: Followership, Sustainability, HIV/AIDS, NYSC
- computer-studies: Motherboard, Linux, macOS, Pseudocode, Antivirus,
  Website, SQL, Terabyte, ICT, Cybersecurity, Phishing, Bluetooth, USB,
  Touchscreen

Hausa, Igbo and Yoruba words are not English and are excluded from dictionary
coverage by design; their glosses are standard everyday vocabulary of each
language.

## F. Final validation (24 Nov 2026)

- 44 files, 4,400 words, 4,400 quiz questions; every file parses as JSON.
- 0 entry defects, 0 quiz defects (audit: `vocab_audit.py`).
- No duplicate words, ids or definitions within any file; no duplicate word
  ids or quiz ids globally.
- Cross-category shared words: 240 (26 same-sense, 214 different-sense) —
  legitimate, by design; do not de-duplicate across categories.
- Nothing pushed to GitHub. Publish from
  `/tmp/mystudy-repos/vocabulary-database/` after review
  (`git status`: 24 modified files + 20 new files).
