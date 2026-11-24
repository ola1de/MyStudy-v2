import { useState } from 'react'

// Profile page (Phase 1 shell): local, customisable fields per
// architecture §2.4. Server persistence (PUT /api/profile) lands in P2;
// Phase 1 saves to the browser only and says so, so nothing is
// mistaken for a synced profile.
const ACCENTS = ['#5b57e8', '#0b95e0', '#0f8073', '#f0a020', '#e2504f', '#58cc02']

export default function Profile() {
  const [displayName, setDisplayName] = useState('')
  const [bio, setBio] = useState('')
  const [examTarget, setExamTarget] = useState('JAMB')
  const [subjects, setSubjects] = useState('English, Mathematics, Physics, Chemistry')
  const [targetScore, setTargetScore] = useState(300)
  const [institution, setInstitution] = useState('')
  const [course, setCourse] = useState('')
  const [theme, setTheme] = useState('light')
  const [accent, setAccent] = useState('#5b57e8')
  const [saved, setSaved] = useState(false)

  function save(e: React.FormEvent) {
    e.preventDefault()
    document.documentElement.setAttribute('data-theme', theme)
    document.documentElement.style.setProperty('--primary', accent)
    localStorage.setItem(
      'mystudy-profile-v2',
      JSON.stringify({ displayName, bio, examTarget, subjects, targetScore, institution, course, theme, accent }),
    )
    setSaved(true)
  }

  return (
    <div className="page">
      <h1>Your profile</h1>
      <p className="notice">
        Phase 1: these settings save in this browser only. Server-synced profiles (with avatar
        upload to R2) land in P2.
      </p>
      <form className="form" onSubmit={save}>
        <label>
          Display name
          <input value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
        </label>
        <label>
          Bio
          <textarea value={bio} onChange={(e) => setBio(e.target.value)} rows={3} />
        </label>
        <label>
          Exam target
          <select value={examTarget} onChange={(e) => setExamTarget(e.target.value)}>
            <option>JAMB</option>
            <option>WAEC</option>
            <option>NECO</option>
            <option>Post-UTME</option>
          </select>
        </label>
        <label>
          Subjects (comma-separated)
          <input value={subjects} onChange={(e) => setSubjects(e.target.value)} />
        </label>
        <label>
          Target score (JAMB, out of 400)
          <input type="number" min={0} max={400} value={targetScore} onChange={(e) => setTargetScore(Number(e.target.value))} />
        </label>
        <label>
          Institution
          <input value={institution} onChange={(e) => setInstitution(e.target.value)} />
        </label>
        <label>
          Course
          <input value={course} onChange={(e) => setCourse(e.target.value)} />
        </label>
        <label>
          Theme
          <select value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label>
          Accent colour
          <select value={accent} onChange={(e) => setAccent(e.target.value)}>
            {ACCENTS.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
        {saved && <p className="notice">Saved in this browser.</p>}
        <button type="submit">Save profile</button>
      </form>
    </div>
  )
}
