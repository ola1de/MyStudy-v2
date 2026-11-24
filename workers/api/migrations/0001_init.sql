-- MyStudy v2 — D1 migration 0001_init.sql (Phase 1, 2026-11-24).
-- Per architecture docs/architecture-24-nov.md §3.
-- Additive only. No seed data, no secrets, no Paystack keys.
-- All timestamps are ISO-8601 UTC text. Money is integer kobo (minor units).

PRAGMA foreign_keys = ON;

-- Users. totp_secret_enc: Phase 1 stores the base32 TOTP secret; P2 must
-- encrypt it at rest (AES-GCM, key in a Cloudflare secret) — see README.
-- password_hash format: pbkdf2$<iterations>$<base64url salt>$<base64url hash>
-- (PBKDF2-HMAC-SHA256, 60,000 iterations in Phase 1, 16-byte salt, 32-byte hash).
-- Security answers: pbkdf2$... hashes of the normalised answer, never plaintext.
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  totp_secret_enc TEXT,
  totp_enabled INTEGER NOT NULL DEFAULT 0,
  recovery_codes_hash TEXT NOT NULL DEFAULT '[]',
  security_q1 TEXT,
  security_q2 TEXT,
  security_q3 TEXT,
  security_a1_hash TEXT,
  security_a2_hash TEXT,
  security_a3_hash TEXT,
  role TEXT NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'admin')),
  premium_status TEXT NOT NULL DEFAULT 'free' CHECK (premium_status IN ('free', 'active', 'revoked')),
  premium_until TEXT,
  exam_target TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  last_login TEXT
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  expires_at TEXT NOT NULL,
  revoked INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

CREATE TABLE IF NOT EXISTS password_resets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  code_hash TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  used INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS login_attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  ip TEXT,
  attempted_at TEXT NOT NULL DEFAULT (datetime('now')),
  success INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_login_attempts_email ON login_attempts(email, attempted_at);

CREATE TABLE IF NOT EXISTS profiles (
  user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_r2_key TEXT,
  bio TEXT,
  subjects_json TEXT NOT NULL DEFAULT '[]',
  target_score INTEGER,
  institution TEXT,
  course TEXT,
  theme TEXT NOT NULL DEFAULT 'light' CHECK (theme IN ('light', 'dark')),
  accent TEXT NOT NULL DEFAULT '#5b57e8',
  notifications INTEGER NOT NULL DEFAULT 1,
  public_profile INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS news_categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS news_posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  excerpt TEXT,
  body_html TEXT NOT NULL DEFAULT '',
  featured_image_r2_key TEXT,
  featured_image_url TEXT,
  category TEXT,
  tags_json TEXT NOT NULL DEFAULT '[]',
  seo_title TEXT,
  seo_description TEXT,
  seo_keywords TEXT,
  og_image TEXT,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'scheduled')),
  published_at TEXT,
  author_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
  toc_json TEXT NOT NULL DEFAULT '[]',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_news_status_published ON news_posts(status, published_at);
CREATE INDEX IF NOT EXISTS idx_news_slug ON news_posts(slug);

CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  paystack_ref TEXT NOT NULL UNIQUE,
  amount_kobo INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'failed', 'refunded')),
  verified_at TEXT,
  raw_json TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_payments_user ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_ref ON payments(paystack_ref);

-- Settings (key/value). Paystack keys live here ONLY as encrypted values
-- from P2 onwards, set by an admin in Admin -> Settings -> Payments.
-- premium_price_kobo default: 200000 = NGN 2,000 once (v1 price).
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
INSERT OR IGNORE INTO settings (key, value) VALUES
  ('premium_price_kobo', '200000'),
  ('premium_duration', 'once'),
  ('paystack_public_key', ''),
  ('paystack_secret_enc', '');

CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  exam TEXT NOT NULL,
  subject TEXT NOT NULL,
  year INTEGER,
  topic TEXT,
  q_text TEXT NOT NULL,
  options_json TEXT NOT NULL,
  answer_idx INTEGER NOT NULL,
  explanation TEXT,
  passage TEXT,
  source_file TEXT,
  hash TEXT NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_questions_exam_subject_year ON questions(exam, subject, year);

CREATE TABLE IF NOT EXISTS exam_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam TEXT NOT NULL,
  subjects_json TEXT NOT NULL,
  started_at TEXT NOT NULL DEFAULT (datetime('now')),
  ends_at TEXT NOT NULL,
  server_seed INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'submitted', 'expired')),
  answers_json TEXT NOT NULL DEFAULT '{}',
  score_json TEXT,
  strikes INTEGER NOT NULL DEFAULT 0,
  submitted_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_exam_sessions_user ON exam_sessions(user_id, status);

CREATE TABLE IF NOT EXISTS study_data (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tool TEXT NOT NULL,
  data_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, tool)
);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  target TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor_id, created_at);
