import { Link } from 'react-router-dom'
import { TOOLS, type ToolStatus } from '../lib/tools'

const STATUS_LABEL: Record<ToolStatus, string> = {
  built: 'Built — verified in Phase 1',
  stubbed: 'Stubbed — shell exists, write path lands in P2',
  planned: 'Planned — design + model named, not built yet',
}

export default function Tools() {
  const built = TOOLS.filter((t) => t.status === 'built').length
  const stubbed = TOOLS.filter((t) => t.status === 'stubbed').length
  const planned = TOOLS.filter((t) => t.status === 'planned').length
  return (
    <div className="page">
      <h1>All tools</h1>
      <p>
        Every tool from v1, rebuilt better than v1 — each with a different model, not a copy of
        the v1 localStorage JavaScript. Server-backed where it matters (accounts, progress,
        premium), client-side where privacy matters (your documents stay on your device).
      </p>
      <p className="notice">
        {TOOLS.length} tools: {built} built, {stubbed} stubbed, {planned} planned. Nothing here
        is claimed as working until it is built and verified — planned tools show their model
        and their phase, not a fake working screen.
      </p>
      <div className="grid">
        {TOOLS.map((t) => (
          <article className="card" key={t.name}>
            <span className="eyebrow">{t.phase} · {t.status}</span>
            <h3>{t.name}</h3>
            <p><strong>v2 model:</strong> {t.v2model}</p>
            <p><strong>v1:</strong> {t.v1}</p>
            <p>{STATUS_LABEL[t.status]}</p>
          </article>
        ))}
      </div>
      <p style={{ marginTop: '1.5rem' }}>
        <Link to="/keypoints">Keypoints design</Link> · <Link to="/vocabulary">Vocabulary design</Link>
      </p>
    </div>
  )
}
