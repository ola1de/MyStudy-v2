import { Link } from 'react-router-dom'
import { TOOLS, type ToolStatus } from '../lib/tools'

const STATUS_LABEL: Record<ToolStatus, string> = {
  built: 'Built',
  stubbed: 'Shell only',
  planned: 'Planned',
}

const STATUS_NOTE: Record<ToolStatus, string> = {
  built: 'Implemented in this build and verified. You can use it.',
  stubbed: 'The screen or API exists, but the write path is not wired yet. It says so on the screen.',
  planned: 'Design and rebuild model named, not built yet. Never shown as working.',
}

// Tools index — grouped by honest status, in rows, not a wall of identical
// cards. Each row names the v2 rebuild model and what v1 did, so a student
// can tell at a glance what works today and what is still coming.
export default function Tools() {
  const groups: ToolStatus[] = ['built', 'stubbed', 'planned']
  return (
    <div className="page">
      <p className="kicker">All tools</p>
      <h1>Every tool from v1, rebuilt better than v1</h1>
      <p className="lede">
        {TOOLS.length} tools. Server-backed where it matters (accounts, progress, premium),
        client-side where privacy matters (your documents stay on your device). Nothing here
        is claimed as working until it is built and verified.
      </p>
      {groups.map((status) => {
        const items = TOOLS.filter((t) => t.status === status)
        if (items.length === 0) return null
        return (
          <section key={status}>
            <div className="section-head">
              <h2>
                {STATUS_LABEL[status]} — {items.length}
              </h2>
              <p className="section-note">{STATUS_NOTE[status]}</p>
            </div>
            <div className="tool-rows">
              {items.map((t) => (
                <div className="tool-row static" key={t.name}>
                  <span>
                    <strong>{t.name}</strong>
                    <small>
                      <b>v2:</b> {t.v2model}
                    </small>
                    <small className="muted">
                      <b>v1:</b> {t.v1}
                    </small>
                  </span>
                  <span className={`status-pill ${status}`}>{t.phase}</span>
                </div>
              ))}
            </div>
          </section>
        )
      })}
      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/keypoints">Keypoints</Link> · <Link to="/vocabulary">Vocabulary</Link>
      </p>
    </div>
  )
}
