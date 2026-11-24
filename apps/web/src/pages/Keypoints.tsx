import { Link } from 'react-router-dom'
import { KEYPOINTS } from '../data/content'

// Learn Hub / Keypoints — the real coverage, counted from mystudy-textbooks.
// 273 chapters, 1,482 modules, 13,650 quiz questions (50 per chapter).
// The chapter reader and 10-question tests are P3 — this page lists what
// exists today and says plainly what is still missing (JSS 1–3, Primary,
// and the real Literature prescribed texts).
export default function Keypoints() {
  return (
    <div className="page">
      <p className="kicker">Learn Hub — Keypoints</p>
      <h1>Short notes that follow the syllabus</h1>
      <p className="lede">
        {KEYPOINTS.chapters} chapters across {KEYPOINTS.subjects.length} subjects, SSS 1–3.
        Every chapter has its study modules and exactly 50 quiz questions —{' '}
        {KEYPOINTS.quiz.toLocaleString('en-NG')} questions in total, across{' '}
        {KEYPOINTS.modules.toLocaleString('en-NG')} modules.
      </p>
      <p className="fineprint">
        The chapter reader (one module at a time, progress saved to your account, then a
        10-question test from the chapter&apos;s quiz pool) is being built next. This page
        lists the content that is already in the bank — nothing here is a working reader yet.
      </p>

      <table className="data-table">
        <thead>
          <tr>
            <th>Subject</th>
            <th>Chapters</th>
            <th>Quiz questions</th>
          </tr>
        </thead>
        <tbody>
          {KEYPOINTS.subjects.map((s) => (
            <tr key={s.slug}>
              <td>{s.name}</td>
              <td>{s.chapters}</td>
              <td>{(s.chapters * 50).toLocaleString('en-NG')}</td>
            </tr>
          ))}
          <tr className="total-row">
            <td>Total</td>
            <td>{KEYPOINTS.chapters}</td>
            <td>{KEYPOINTS.quiz.toLocaleString('en-NG')}</td>
          </tr>
        </tbody>
      </table>

      <h2>What is still missing</h2>
      <ul className="tick-list plain">
        <li>JSS 1–3 and Primary keypoints — no chapters exist yet.</li>
        <li>Literature chapters are appreciation frameworks, not the actual JAMB prescribed texts.</li>
        <li>2,071 of the quiz questions (15.2%) are syllabus-modelled practice, labelled as such — they need a subject review before they are presented as exam-grade.</li>
      </ul>
      <p>
        Chapters come from the user&apos;s <code>mystudy-textbooks</code> repo, authored against
        the official JAMB/WAEC/NECO syllabuses. The importer never invents module content or
        quiz questions.
      </p>
      <p><Link to="/tools">Back to all tools</Link></p>
    </div>
  )
}
