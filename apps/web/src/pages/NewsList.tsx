import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type NewsPost } from '../lib/api'

export default function NewsList() {
  const [posts, setPosts] = useState<NewsPost[]>([])
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get<{ posts: NewsPost[] }>('/api/news')
      .then((r) => {
        if (r.ok && r.data) setPosts(r.data.posts)
        else setError(r.error?.message ?? 'Could not load news.')
        setLoaded(true)
      })
      .catch(() => {
        setError('Could not reach the server.')
        setLoaded(true)
      })
  }, [])

  return (
    <div className="page">
      <h1>News</h1>
      <p>Exam news, admission updates and study guides — published by the MyStudy admin team only.</p>
      {!loaded && <p>Loading…</p>}
      {error && <p className="error">{error}</p>}
      {loaded && !error && posts.length === 0 && (
        <p className="notice">No news posts have been published yet.</p>
      )}
      <div className="grid">
        {posts.map((p) => (
          <article className="card" key={p.slug}>
            {p.category && <span className="eyebrow">{p.category}</span>}
            <h3>
              <Link to={`/news/${p.slug}`}>{p.title}</Link>
            </h3>
            {p.excerpt && <p>{p.excerpt}</p>}
            {p.published_at && <p>{new Date(p.published_at).toLocaleDateString('en-NG')}</p>}
          </article>
        ))}
      </div>
    </div>
  )
}
