import { Link } from 'react-router-dom'

// Vocabulary module design (Phase 1 scaffold — design + tables only).
// Data: vocabulary-database — 24 categories x 100 words = 2,400 words
// (audit §8). The audit found index.json lists only 14 of the 24
// categories; the v2 importer regenerates the index from the data files.
const ALL_CATEGORIES = [
  'admin-vocabulary', 'animal-habitats', 'baby-animals', 'branches-of-study',
  'capability-adjectives', 'collective-nouns', 'dietary-habits', 'environment',
  'forms-of-government', 'idioms', 'measurement-instruments', 'medical-specialists',
  'natural-phenomena', 'obsessions', 'one-word-substitutions', 'personality-types',
  'philosophical-stances', 'phobias', 'professions', 'proverbs',
  'sensory-sounds', 'time-and-frequency', 'umbrella-terms', 'words-for-killing',
]

const UNINDEXED_IN_V1 = [
  'admin-vocabulary', 'animal-habitats', 'capability-adjectives', 'environment',
  'idioms', 'natural-phenomena', 'professions', 'proverbs', 'sensory-sounds',
  'umbrella-terms',
]

export default function Vocabulary() {
  return (
    <div className="page">
      <h1>Vocabulary</h1>
      <p className="notice">
        Status: planned (P3). The design and the database tables (migration 0002) are in place;
        the word import and trainer are not built yet. Nothing on this page is a working
        trainer — it is the plan the trainer will be built to.
      </p>

      <h2>How it works in v2 (different model from v1)</h2>
      <p>
        v1 loaded word data from jsDelivr at runtime and kept learned words and streaks in
        localStorage — editable by the user, and 10 of the 24 categories were unreachable
        because the repo&apos;s <code>index.json</code> lists only 14. v2 is server-backed:
        words live in D1 (<code>vocabulary_words</code>), the category index is regenerated
        by the importer from the data files (never trusted from the repo&apos;s index), and
        learned words + streaks (<code>vocabulary_progress</code>) are recorded server-side.
      </p>
      <ul>
        <li><strong>Word shape (unchanged, the best-structured dataset in the audit):</strong> <code>{'{id, word, pos, definition, example}'}</code>.</li>
        <li><strong>Trainer:</strong> learn words by category, 30-question tests, streaks for daily study — same test length as v1, but progress the user cannot fake.</li>
        <li><strong>Quiz:</strong> 100 quiz questions per category, stored in <code>vocabulary_quizzes</code>.</li>
      </ul>

      <h2>All 24 categories</h2>
      <p>
        {ALL_CATEGORIES.map((c) => (
          <span className="tag" key={c}>{c}</span>
        ))}
      </p>
      <p>
        <strong>Fixed in v2:</strong> these 10 categories were in the data but missing from
        v1&apos;s index, so students likely never reached them:{' '}
        {UNINDEXED_IN_V1.join(', ')}.
      </p>

      <h2>Filling the gaps — new categories</h2>
      <p>
        Every subject/category omitted in v1 gets filled, and topics go to full coverage — no
        shallow or half-done categories left. New categories follow the existing schema
        exactly: 100 words each as <code>{'{id, word, pos, definition, example}'}</code>,
        plus 100 quiz questions per category, and the index is updated to list every category.
        Words and quiz questions come from real vocabulary sources and the syllabus — the
        importer never invents definitions or examples.
      </p>
      <p><Link to="/tools">Back to all tools</Link></p>
    </div>
  )
}
