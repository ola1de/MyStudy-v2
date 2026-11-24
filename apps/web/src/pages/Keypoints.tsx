import { Link } from 'react-router-dom'

// Keypoints module design (Phase 1 scaffold — design + tables only).
// Data: mystudy-textbooks — 166 chapters, 503 modules, 4,630 quiz questions,
// 12 subjects, SSS 1–3 only (audit §6). The design fixes the v1 gaps
// instead of copying them.
export default function Keypoints() {
  return (
    <div className="page">
      <h1>Keypoints</h1>
      <p className="notice">
        Status: planned (P3). The design and the database tables (migration 0002) are in place;
        the chapter import and reader are not built yet. Nothing on this page is a working
        reader — it is the plan the reader will be built to.
      </p>

      <h2>How it works in v2 (different model from v1)</h2>
      <p>
        v1 kept a 165-topic registry in the template that fetched chapter JSON from jsDelivr at
        runtime — and showed subjects with no topics at all as if they existed. v2 is
        server-backed: chapters are imported once into D1 (<code>textbook_chapters</code>),
        the reader loads one module at a time from the API, and progress
        (<code>keypoint_progress</code>) is recorded server-side, so a student&apos;s
        &ldquo;modules done&rdquo; and best scores cannot be edited in the browser.
      </p>
      <ul>
        <li><strong>Reader:</strong> one module at a time, prev/next, progress bar, &ldquo;mark module done&rdquo;, KaTeX maths rendering, then a 10-question test drawn from the chapter&apos;s quiz pool.</li>
        <li><strong>Tests:</strong> score + time + per-topic progress (modules done, best score, average score, tests taken) kept server-side.</li>
        <li><strong>Honest availability:</strong> only subjects with real imported chapters are offered. Missing subjects show &ldquo;coming soon&rdquo;, never an empty shell.</li>
      </ul>

      <h2>Coverage — what exists, what must be filled</h2>
      <p>
        Imported as-is (12 subjects, SSS 1–3): Mathematics, English, Physics, Chemistry,
        Biology, Economics, Government, Literature, Geography, Commerce, Accounting, Agric —
        166 chapters, 503 modules, 4,630 quiz questions.
      </p>
      <p>
        <strong>Missing and to be authored — no shallow topics left:</strong> CRS, IRS, Civic
        Education, Computer Studies, Further Mathematics, History, Hausa, Igbo, Yoruba have no
        textbook chapters at all. There is no JSS 1–3 content and no Primary content. Every
        topic must be deepened to full coverage: each subject gets its full syllabus topic
        list at every level it is taught, with modules that teach the topic properly (not a
        one-paragraph stub) and a real quiz pool per chapter. Mathematics files use a
        different schema (<code>topic</code>/<code>ss_level</code>/<code>icon</code>/
        <code>color</code>) from the other 11 subjects — the P3 importer normalises both
        schemas to one table.
      </p>
      <p>
        Literature chapters are generic appreciation/prescribed-text frameworks, not the JAMB
        prescribed texts themselves — those need authoring against the current JAMB syllabus.
      </p>

      <h2>Where the content comes from</h2>
      <p>
        Chapters come verbatim from the user&apos;s <code>mystudy-textbooks</code> repo. New
        chapters are authored against the official JAMB/WAEC/NECO syllabuses — the importer
        never invents module content or quiz questions.
      </p>
      <p><Link to="/tools">Back to all tools</Link></p>
    </div>
  )
}
