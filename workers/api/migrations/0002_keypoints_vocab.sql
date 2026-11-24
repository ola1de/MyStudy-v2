-- MyStudy v2 — D1 migration 0002_keypoints_vocab.sql (Phase 1, 2026-11-24).
-- Keypoints + Vocabulary, server-backed (architecture §10).
-- Source data: mystudy-textbooks chapters (166 files, 12 subjects, SSS 1-3)
-- and vocabulary-database (24 categories x 100 words). The import itself
-- is P3; this migration only creates the tables so P3 has a target.
-- No seed data here. No invented content: chapters/words are imported
-- verbatim from the repos, and missing subjects/categories are authoring
-- work, shown as "coming soon", never as empty shells.

PRAGMA foreign_keys = ON;

-- Keypoints: one row per textbook chapter (topic) from mystudy-textbooks.
-- Mathematics files use a different schema (topic/ss_level/icon/color) —
-- the P3 importer normalises both schemas to this one table.
CREATE TABLE IF NOT EXISTS textbook_chapters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  level TEXT NOT NULL,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  outline_json TEXT NOT NULL DEFAULT '[]',
  modules_json TEXT NOT NULL DEFAULT '[]',
  quiz_json TEXT NOT NULL DEFAULT '[]',
  source_file TEXT,
  UNIQUE (subject, level, slug)
);
CREATE INDEX IF NOT EXISTS idx_chapters_subject_level ON textbook_chapters(subject, level);

-- Per-user Keypoints progress: modules done + best/average test score.
CREATE TABLE IF NOT EXISTS keypoint_progress (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  chapter_id INTEGER NOT NULL REFERENCES textbook_chapters(id) ON DELETE CASCADE,
  modules_done_json TEXT NOT NULL DEFAULT '[]',
  best_score INTEGER,
  avg_score REAL,
  tests_taken INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, chapter_id)
);

-- Vocabulary categories. The v2 index lists ALL categories (the audit
-- found index.json lists only 14 of 24 — the P3 importer regenerates
-- the index from the data files, it does not trust the repo's index).
CREATE TABLE IF NOT EXISTS vocabulary_categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  word_count INTEGER NOT NULL DEFAULT 0,
  quiz_count INTEGER NOT NULL DEFAULT 0
);

-- Vocabulary words. Schema (per repo): {id, word, pos, definition,
-- example}. New categories follow the same schema, 100 words each,
-- plus 100 quiz questions per category (stored in vocabulary_quizzes).
CREATE TABLE IF NOT EXISTS vocabulary_words (
  id TEXT PRIMARY KEY,
  category_slug TEXT NOT NULL REFERENCES vocabulary_categories(slug) ON DELETE CASCADE,
  word TEXT NOT NULL,
  pos TEXT,
  definition TEXT NOT NULL,
  example TEXT
);
CREATE INDEX IF NOT EXISTS idx_vocab_words_category ON vocabulary_words(category_slug, word);

CREATE TABLE IF NOT EXISTS vocabulary_quizzes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_slug TEXT NOT NULL REFERENCES vocabulary_categories(slug) ON DELETE CASCADE,
  q_text TEXT NOT NULL,
  options_json TEXT NOT NULL,
  answer_idx INTEGER NOT NULL,
  explanation TEXT
);
CREATE INDEX IF NOT EXISTS idx_vocab_quizzes_category ON vocabulary_quizzes(category_slug);

-- Per-user Vocabulary progress: words learned + streak, server-side
-- (v1 kept streaks in localStorage, which the user could edit).
CREATE TABLE IF NOT EXISTS vocabulary_progress (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category_slug TEXT NOT NULL,
  learned_json TEXT NOT NULL DEFAULT '[]',
  streak_days INTEGER NOT NULL DEFAULT 0,
  last_study_date TEXT,
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, category_slug)
);
