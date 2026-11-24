import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type NewsPost } from '../lib/api'

const TOOLS = [
  { title: 'CBT Practice', desc: 'Timed JAMB, WAEC, NECO and Post-UTME mocks, just like the real exam.', to: '/tools' },
  { title: 'CGPA Calculator', desc: '4.0 and 5.0 scales, semester GPA, class of degree, printable transcript.', to: '/tools' },
  { title: 'Learn Hub', desc: 'Keypoints, past questions and syllabus — only subjects with real content.', to: '/keypoints' },
  { title: 'Admission Toolkit', desc: 'JAMB subject combinations and Post-UTME aggregate predictor.', to: '/tools' },
  { title: 'Flashcards', desc: 'Leitner spaced repetition for the topics you struggle with.', to: '/tools' },
  { title: 'Study Planner', desc: 'Pomodoro focus timer, timetable, deadlines and study streaks.', to: '/tools' },
]

export default function Home() {
  const [posts, setPosts] = useState<NewsPost[]>([])
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    api
      .get<{ posts: NewsPost[] }>('/api/news')
      .then((r) => {
        if (r.ok && r.data) setPosts(r.data.posts)
        setLoaded(true)
      })
      .catch(() => setLoaded(true))
  }, [])

  return (
    <div className="page">
      <section className="hero">
        <h1>Good morning, scholar</h1>
        <p>Focus. Practice. Graduate stronger.</p>
        <p>
          Run CBT mocks, build study plans, calculate your CGPA, and ace admissions — all in one
          offline-ready portal trusted by Nigerian students.
        </p>
      </section>

      <div className="grid">
        {TOOLS.map((t) => (
          <div className="card" key={t.title}>
            <h3>
              <Link to={t.to}>{t.title}</Link>
            </h3>
            <p>{t.desc}</p>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: '2rem' }}>Latest on MyStudy</h2>
      {!loaded && <p>Loading news…</p>}
      {loaded && posts.length === 0 && (
        <p className="notice">
          No news posts yet. When an admin publishes the first News update, it will appear here —
          v2 never shows empty shells or dead links.
        </p>
      )}
      <div className="grid">
        {posts.map((p) => (
          <article className="card" key={p.slug}>
            {p.category && <span className="eyebrow">{p.category}</span>}
            <h3>
              <Link to={`/news/${p.slug}`}>{p.title}</Link>
            </h3>
            {p.excerpt && <p>{p.excerpt}</p>}
          </article>
        ))}
      </div>
    </div>
  )
}
