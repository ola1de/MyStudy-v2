import { useState } from 'react'
import { Link } from 'react-router-dom'
import { VOCABULARY } from '../data/content'

// Vocabulary — the real 44 categories, 4,400 words, 4,400 quiz questions,
// counted from vocabulary-database (index v3). The trainer (adaptive tests,
// streaks saved to your account) is P3 — this page lists the categories
// that exist today, with a search box, and says plainly what is still missing.
export default function Vocabulary() {
  const [q, setQ] = useState('')
  const shown = VOCABULARY.list.filter((c) =>
    c.name.toLowerCase().includes(q.trim().toLowerCase()),
  )
  return (
    <div className="page">
      <p className="kicker">Vocabulary</p>
      <h1>Words JAMB actually tests</h1>
      <p className="lede">
        {VOCABULARY.categories} categories · {VOCABULARY.words.toLocaleString('en-NG')} words ·{' '}
        {VOCABULARY.quiz.toLocaleString('en-NG')} quiz questions — 100 words and 100 quiz
        questions in every category, each word with its part of speech, definition and an
        example sentence.
      </p>
      <p className="fineprint">
        The trainer is being built next (learn by category, 30-question tests, streaks saved
        to your account). This page is the catalogue — every category below is real and in
        the bank, including the 10 categories v1&apos;s index never listed and the 20 new
        subject categories added in November 2026.
      </p>
      <label className="search-label">
        Search categories
        <input
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="e.g. idioms, physics, Yoruba…"
        />
      </label>
      {shown.length === 0 && <p className="notice">No category matches “{q}”.</p>}
      <ul className="subject-index">
        {shown.map((c) => (
          <li key={c.slug}>
            <span>
              <span>{c.name}</span>
              <strong>{c.count} words</strong>
            </span>
          </li>
        ))}
      </ul>
      <p className="fineprint">
        122 of the new specialist terms are standard terms that have not yet been
        spot-checked against a dictionary — they are listed in the expansion manifest,
        not silently trusted.
      </p>
      <p><Link to="/tools">Back to all tools</Link></p>
    </div>
  )
}
