// MyStudy v2 — tools registry (Phase 1 scaffold).
// Every v1 tool (from docs/template-inventory-24-nov.md §1), its v2
// rebuild model, and its honest status. Status meanings:
//   built   — implemented in this scaffold and verified (see build doc).
//   stubbed — UI/API exists but the write path is not wired yet (says so).
//   planned — design + model named, not built yet. Never shown as working.
export type ToolStatus = 'built' | 'stubbed' | 'planned'

export interface ToolEntry {
  name: string
  v1: string
  v2model: string
  status: ToolStatus
  phase: string
}

export const TOOLS: ToolEntry[] = [
  { name: 'Home dashboard', v1: 'Greeting, stats, tool tiles, latest posts (localStorage)', v2model: 'React shell; stats read from D1 per user; News from GET /api/news', status: 'built', phase: 'P1' },
  { name: 'Register / Sign in', v1: 'No auth at all', v2model: 'Rust: PBKDF2 passwords, compulsory TOTP (QR + manual code), 3 security questions, lockout, opaque sessions', status: 'built', phase: 'P1' },
  { name: 'News (was Blog)', v1: 'Blogger posts, theme only reads labels', v2model: 'Admin-only editor (P2 write); read path live from D1 with v1 post format + TOC', status: 'built', phase: 'P1 read / P2 write' },
  { name: 'News editor', v1: 'None — posts authored in Blogger', v2model: 'React editor: title/slug/excerpt/body, image URL or R2 upload, category, tags, SEO fields, draft/published/scheduled', status: 'stubbed', phase: 'P1 shell / P2 write' },
  { name: 'Profile', v1: 'Name/institution/course/theme in localStorage', v2model: 'Full profile (display name, avatar to R2, bio, exam target, subjects, target score, theme/accent); server sync in P2', status: 'built', phase: 'P1 shell / P2 sync' },
  { name: 'CBT Practice', v1: 'Client-side mocks; premium flag in localStorage (bypassable)', v2model: 'Rust exam sessions: server clock, seeded shuffle, answers scored server-side, premium read from D1 per request, 3-strike anti-cheat', status: 'planned', phase: 'P2' },
  { name: 'Premium + Paystack', v1: 'Manual ₦2,000 bank transfer + WhatsApp activation key', v2model: 'Admin pastes Paystack keys; server creates pending payment, verifies via Paystack API + webhook signature; premium flips only on verified success', status: 'planned', phase: 'P2' },
  { name: 'Keypoints', v1: '165-topic registry pointing at external JSON; 6 subjects empty', v2model: 'Server-backed chapters from mystudy-textbooks (see architecture §10); module reader + 10-question tests; full-coverage authoring for missing subjects/levels', status: 'planned', phase: 'P3' },
  { name: 'Vocabulary', v1: '24 categories but index lists only 14; streaks in localStorage', v2model: 'Server-backed words from vocabulary-database; regenerated index lists all 24 categories; new categories follow {id, word, pos, definition, example} + 100 quiz Qs (see architecture §10)', status: 'planned', phase: 'P3' },
  { name: 'Past Questions browser', v1: 'Blogger label pages — empty when no post exists', v2model: 'Reads the normalised questions table; only years with real questions are offered', status: 'planned', phase: 'P3' },
  { name: 'English Quiz', v1: '9 categories, client-side, Old* duplicate files', v2model: 'Server-backed from the 900 current English-Quiz questions (Old* twins dropped); timed, explanations shown after submit', status: 'planned', phase: 'P3' },
  { name: 'Dictionary', v1: 'Per-letter JSON shipped to the browser from jsDelivr', v2model: 'Server-side lookup from merged.json (121,340 entries); the 72 MB dictionary is never shipped to the browser', status: 'planned', phase: 'P4' },
  { name: 'CGPA Calculator', v1: 'Client-side, draft in localStorage', v2model: 'Exact decimal math (integer hundredths, no float); semesters saved server-side per user; printable transcript generated server-side', status: 'planned', phase: 'P4' },
  { name: 'Graduation Predictor', v1: 'Client-side computed', v2model: 'Same exact-math engine as CGPA; reads saved semesters from D1', status: 'planned', phase: 'P4' },
  { name: 'GPA to Class of Degree', v1: 'Client-side computed', v2model: 'Same exact-math engine; 4.0/5.0 class thresholds from the v1 tables, verified', status: 'planned', phase: 'P4' },
  { name: 'Admission Toolkit', v1: '78-course combo checker + aggregate predictor, client-side', v2model: 'Server-side course table (faculties, UTME + O-Level subjects); aggregate formulas per university, versioned in D1', status: 'planned', phase: 'P4' },
  { name: 'Flashcards (Leitner)', v1: 'Deck builder in localStorage', v2model: 'Server-backed decks in study_data; Leitner 3-box scheduling computed server-side so progress cannot be edited client-side', status: 'planned', phase: 'P4' },
  { name: 'Exam Planner', v1: 'Countdowns + alarms in localStorage', v2model: 'Server-backed exams in study_data; countdowns from the server clock; reminders on-read (no cron — account is at 5/5 triggers)', status: 'planned', phase: 'P4' },
  { name: 'Lecture Schedule', v1: 'Weekly grid in localStorage', v2model: 'Server-backed weekly grid in study_data; conflict detection on save', status: 'planned', phase: 'P4' },
  { name: 'Study Planner (Pomodoro + Feynman)', v1: 'Timer + notes in localStorage', v2model: 'Server-recorded focus sessions (streak/XP from server time); Feynman notes stored per user in study_data', status: 'planned', phase: 'P4' },
  { name: 'Class Timetable', v1: 'Builder in localStorage, printable', v2model: 'Server-backed timetable in study_data; print/export generated server-side', status: 'planned', phase: 'P4' },
  { name: 'Revision Timetable', v1: 'Generated client-side', v2model: 'Server-side generator from exam dates + Keypoints progress (weak topics first)', status: 'planned', phase: 'P4' },
  { name: 'Deadline Planner', v1: 'Tracking in localStorage', v2model: 'Server-backed deadlines in study_data; days-left from the server clock', status: 'planned', phase: 'P4' },
  { name: 'Note Outline Builder', v1: 'Client-side outline builder', v2model: 'Server-backed outlines in study_data; export to Word Office', status: 'planned', phase: 'P4' },
  { name: 'Budget Tracker', v1: 'Monthly ₦ limit + expenses in localStorage', v2model: 'Integer-kobo money (never float); expenses saved server-side; monthly summaries computed in Rust', status: 'planned', phase: 'P4' },
  { name: 'Study Streak & XP', v1: 'Streaks in localStorage (editable by the user)', v2model: 'Server-side streak from recorded study activity; XP rules in Rust, one source of truth', status: 'planned', phase: 'P4' },
  { name: 'Word Office', v1: 'TinyMCE A4 editor, DOCX/PDF export in-browser', v2model: 'TipTap-style editor in React; DOCX read via mammoth, write via the docx library, PDF export client-side; documents optionally saved to R2 per user', status: 'planned', phase: 'P4' },
  { name: 'PDF Toolkit', v1: 'Merge/split/compress/reorder/watermark/OCR/E-Sign in-browser (pdf-lib, jsPDF)', v2model: 'Client-side pdf-lib for merge/split/reorder/watermark (files never leave the device); server-side fallback for large files; OCR via Workers AI, labelled as AI and optional', status: 'planned', phase: 'P4' },
  { name: 'Image Toolkit', v1: 'Compress/resize/convert/batch/watermark/EXIF/QR in-browser', v2model: 'Canvas + Web Worker processing (no main-thread freeze); saved outputs to R2; EXIF stripped client-side before any upload', status: 'planned', phase: 'P4' },
  { name: 'Word & Character Counter', v1: 'Client-side counter', v2model: 'Client-side counter (no server needed); counts words, characters, sentences, reading time', status: 'planned', phase: 'P4' },
  { name: 'Citation Generator', v1: 'APA/MLA/Harvard/Chicago/IEEE/Vancouver templates, client-side', v2model: 'Local CSL-style templates that format ONLY metadata the user supplies — citations are never invented; optional Workers AI extracts metadata from pasted text and labels it AI-suggested', status: 'planned', phase: 'P4' },
  { name: 'Quick Cite', v1: 'Inline citations, client-side', v2model: 'Same no-invention rule as Citation Generator; inline format from user-supplied metadata', status: 'planned', phase: 'P4' },
  { name: 'Note Summarizer', v1: 'Short/medium/long bullet summaries, offline, client-side', v2model: 'Local extractive summarizer first (no AI, no invented content); optional Workers AI abstractive summary, clearly labelled as AI-generated', status: 'planned', phase: 'P4' },
  { name: 'Text Compare', v1: 'Side-by-side diff, client-side', v2model: 'Client-side diff (Myers) with word-level highlighting; no server needed', status: 'planned', phase: 'P4' },
  { name: 'Constitution Library', v1: '1999 Constitution from nigeria-constitution via jsDelivr', v2model: 'Server-side sections (227 sections, Ch. I–VIII) from the repo; search in Rust; amendment status verified against the official text before presenting as current law', status: 'planned', phase: 'P4' },
  { name: 'Unit Converter', v1: 'Length/mass/temperature/area/volume/time, client-side', v2model: 'Client-side exact conversion tables; length/mass use rational factors, temperature uses exact formulas', status: 'planned', phase: 'P4' },
  { name: 'Chart Generator', v1: 'Bar/Line/Pie/Doughnut/Radar + PNG/JPG/PDF/CSV export, client-side', v2model: 'Client-side canvas charts; export PNG/CSV locally; data never leaves the device', status: 'planned', phase: 'P4' },
  { name: 'Bookmarks', v1: 'Saved posts in localStorage', v2model: 'Server-backed bookmarks per user (study_data)', status: 'planned', phase: 'P4' },
  { name: 'Study Assistant chatbot', v1: 'bot.mystudysuite.workers.dev + local rule-based fallback', v2model: 'Workers AI with tool-aware context (knows the user\'s subjects, streak, weak topics); answers about tools only — never invents exam answers; v1 bot endpoint is not carried over as-is', status: 'planned', phase: 'P5' },
]
