import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type AdminNewsPost, type NewsCategory } from '../lib/api'
import './admin.css'

// Admin → Posts: every post with status badge, search, category/status
// filters, Edit and Delete (with confirmation). Admin routes return 403
// unless the signed-in user has role admin.
export default function AdminPosts() {
  const [posts, setPosts] = useState<AdminNewsPost[]>([])
  const [categories, setCategories] = useState<NewsCategory[]>([])
  const [q, setQ] = useState('')
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(true)
  const [notAdmin, setNotAdmin] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [deleting, setDeleting] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    const params = new URLSearchParams()
    if (q.trim()) params.set('q', q.trim())
    if (category) params.set('category', category)
    if (status) params.set('status', status)
    const query = params.toString()
    const [postsRes, catsRes] = await Promise.all([
      api.get<{ posts: AdminNewsPost[] }>(`/api/admin/news${query ? `?${query}` : ''}`),
      api.get<{ categories: NewsCategory[] }>('/api/admin/news-categories'),
    ])
    setLoading(false)
    if (!postsRes.ok) {
      if (postsRes.error?.code === 'forbidden' || /not an admin|forbidden/i.test(postsRes.error?.message ?? '')) {
        setNotAdmin(true)
      } else {
        setError(postsRes.error?.message ?? 'Could not load posts.')
      }
      return
    }
    setPosts(postsRes.data?.posts ?? [])
    if (catsRes.ok && catsRes.data) setCategories(catsRes.data.categories)
  }, [q, category, status])

  useEffect(() => {
    const t = window.setTimeout(load, q ? 300 : 0)
    return () => window.clearTimeout(t)
  }, [load, q])

  async function handleDelete(post: AdminNewsPost) {
    if (!window.confirm(`Delete "${post.title}"? This cannot be undone.`)) return
    setDeleting(post.slug)
    setNotice('')
    setError('')
    const r = await api.delete<{ deleted: boolean }>(`/api/admin/news/${encodeURIComponent(post.slug)}`)
    setDeleting(null)
    if (!r.ok) {
      setError(r.error?.message ?? 'Could not delete the post.')
      return
    }
    setNotice(`Deleted "${post.title}".`)
    setPosts((prev) => prev.filter((p) => p.slug !== post.slug))
  }

  function formatDate(value: string | null) {
    if (!value) return '—'
    return new Date(value).toLocaleDateString('en-NG', { day: 'numeric', month: 'short', year: 'numeric' })
  }

  if (notAdmin) {
    return (
      <div className="page admin-page">
        <h1>Admin posts</h1>
        <p className="admin-error">You are not signed in as an admin. Only admins can manage News posts.</p>
        <p><Link to="/login">Sign in</Link> · <Link to="/news">Back to News</Link></p>
      </div>
    )
  }

  return (
    <div className="page admin-page">
      <div className="admin-head">
        <div>
          <h1>Posts</h1>
          <p className="admin-sub">{posts.length} post{posts.length === 1 ? '' : 's'}</p>
        </div>
        <Link className="admin-btn admin-btn-primary" to="/admin/posts/new">New post</Link>
      </div>

      <div className="admin-filters">
        <input
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search title or excerpt…"
          aria-label="Search posts"
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)} aria-label="Filter by category">
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.slug}>{c.name}</option>
          ))}
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} aria-label="Filter by status">
          <option value="">All statuses</option>
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="scheduled">Scheduled</option>
        </select>
      </div>

      {error && <p className="admin-error">{error}</p>}
      {notice && <p className="admin-notice">{notice}</p>}
      {loading && <p>Loading posts…</p>}

      {!loading && posts.length === 0 && (
        <p className="admin-empty">
          No posts yet. <Link to="/admin/posts/new">Write the first post</Link>.
        </p>
      )}

      {!loading && posts.length > 0 && (
        <table className="admin-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {posts.map((p) => (
              <tr key={p.id}>
                <td>
                  <div className="admin-post-title">{p.title}</div>
                  <div className="admin-post-slug">/{p.slug}</div>
                </td>
                <td>{p.category ?? '—'}</td>
                <td>
                  <span className={`admin-badge admin-badge-${p.status}`}>{p.status}</span>
                </td>
                <td>{formatDate(p.published_at ?? p.created_at)}</td>
                <td className="admin-actions">
                  <Link className="admin-btn" to={`/admin/posts/${encodeURIComponent(p.slug)}/edit`}>Edit</Link>
                  {p.status === 'published' && (
                    <Link className="admin-btn" to={`/news/${encodeURIComponent(p.slug)}`} target="_blank" rel="noreferrer">View</Link>
                  )}
                  <button
                    type="button"
                    className="admin-btn admin-btn-danger"
                    disabled={deleting === p.slug}
                    onClick={() => handleDelete(p)}
                  >
                    {deleting === p.slug ? 'Deleting…' : 'Delete'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
