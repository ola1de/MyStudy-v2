import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, type NewsPost } from '../lib/api'
import { buildToc, readTimeMinutes } from '../lib/toc'

// Post page — keeps the v1 format the user loves: eyebrow (category) ->
// Fraunces title -> meta -> featured image -> TOC -> body -> tags -> share.
export default function PostPage() {
  const { slug } = useParams<{ slug: string }>()
  const [post, setPost] = useState<NewsPost | null>(null)
  const [error, setError] = useState('')
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    if (!slug) return
    api
      .get<NewsPost>(`/api/news/${encodeURIComponent(slug)}`)
      .then((r) => {
        if (r.ok && r.data) setPost(r.data)
        else setError(r.error?.message ?? 'Post not found.')
        setLoaded(true)
      })
      .catch(() => {
        setError('Could not reach the server.')
        setLoaded(true)
      })
  }, [slug])

  const { toc, htmlWithIds } = useMemo(() => {
    if (!post) return { toc: [], htmlWithIds: '' }
    // Prefer the server-stored TOC; fall back to building it from the body.
    if (post.toc && post.toc.length >= 3) return { toc: post.toc, htmlWithIds: post.body_html }
    return buildToc(post.body_html)
  }, [post])

  if (!loaded) return <div className="page"><p>Loading…</p></div>
  if (error || !post) {
    return (
      <div className="page">
        <p className="error">{error || 'Post not found.'}</p>
        <p><Link to="/news">Back to News</Link></p>
      </div>
    )
  }

  const shareUrl = `${window.location.origin}/news/${post.slug}`
  return (
    <div className="page" style={{ maxWidth: 880 }}>
      {post.category && <span className="eyebrow">{post.category}</span>}
      <h1 className="post-title">{post.title}</h1>
      <p className="post-meta">
        {post.published_at ? new Date(post.published_at).toLocaleDateString('en-NG', { day: 'numeric', month: 'long', year: 'numeric' }) : ''}
        {' · '}
        {readTimeMinutes(post.body_html)} min read
      </p>
      <p>
        <a href={`https://wa.me/?text=${encodeURIComponent(`${post.title} ${shareUrl}`)}`} target="_blank" rel="noreferrer">Share on WhatsApp</a>
        {' · '}
        <a href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(shareUrl)}`} target="_blank" rel="noreferrer">Share on X</a>
        {' · '}
        <button type="button" className="ghost" onClick={() => navigator.clipboard.writeText(shareUrl)}>Copy link</button>
      </p>
      {post.featured_image_url && (
        <img className="featured-image" src={post.featured_image_url} alt={post.title} />
      )}
      {toc.length >= 3 && (
        <details className="post-toc" open>
          <summary>Table of Contents</summary>
          <ol className="toc-list">
            {toc.map((t) => (
              <li key={t.id} className={t.level === 3 ? 'toc-l3' : undefined}>
                <a href={`#${t.id}`}>{t.text}</a>
              </li>
            ))}
          </ol>
        </details>
      )}
      <div className="post-body" dangerouslySetInnerHTML={{ __html: htmlWithIds }} />
      {post.tags.length > 0 && (
        <p>
          {post.tags.map((t) => (
            <span className="tag" key={t}>{t}</span>
          ))}
        </p>
      )}
      <p><Link to="/news">← Back to News</Link></p>
    </div>
  )
}
