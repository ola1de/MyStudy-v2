import { useState } from 'react'
import { api } from '../lib/api'
import { buildToc } from '../lib/toc'

// Admin News editor shell (Phase 1): full editor fields per architecture
// §6 — title, slug, excerpt, body (H2/H3, bullets, lists, blockquote),
// featured image (upload or URL), category, tags, SEO fields, status.
// The POST /api/admin/news write path lands in P2; Phase 1 previews the
// post (including its TOC) and reports the API result honestly.
const CATEGORIES = ['JAMB', 'WAEC', 'NECO', 'Admissions', 'Study Tips', 'Announcements']

export default function AdminEditor() {
  const [title, setTitle] = useState('')
  const [slug, setSlug] = useState('')
  const [excerpt, setExcerpt] = useState('')
  const [body, setBody] = useState(
    '<h2>Heading</h2>\n<p>Write the news update here. Use H2 for sections and H3 for sub-sections.</p>\n<ul>\n<li>Bullet point one</li>\n<li>Bullet point two</li>\n</ul>\n<h3>Sub-heading</h3>\n<p>More detail.</p>\n<h2>Another section</h2>\n<p>Final section.</p>\n',
  )
  const [imageUrl, setImageUrl] = useState('')
  const [category, setCategory] = useState('JAMB')
  const [tags, setTags] = useState('')
  const [seoTitle, setSeoTitle] = useState('')
  const [seoDescription, setSeoDescription] = useState('')
  const [seoKeywords, setSeoKeywords] = useState('')
  const [status, setStatus] = useState('draft')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function autoSlug(value: string) {
    setTitle(value)
    if (!slug) {
      setSlug(
        value
          .toLowerCase()
          .replace(/[^a-z0-9\s-]/g, '')
          .trim()
          .replace(/\s+/g, '-')
          .slice(0, 80),
      )
    }
  }

  const preview = buildToc(body)

  async function publish(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setMessage('')
    setBusy(true)
    const r = await api.post<{ slug: string }>('/api/admin/news', {
      title,
      slug,
      excerpt,
      body_html: body,
      featured_image_url: imageUrl || null,
      category,
      tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
      seo_title: seoTitle || title,
      seo_description: seoDescription || excerpt,
      seo_keywords: seoKeywords,
      status,
      toc: preview.toc,
    })
    setBusy(false)
    if (!r.ok) {
      // 403 = not an admin; 501 = admin check passed, write path lands in P2.
      setError(r.error?.message ?? 'Could not save the post.')
      return
    }
    setMessage(`Post saved: ${r.data?.slug ?? slug}`)
  }

  return (
    <div className="page">
      <h1>News editor (admin only)</h1>
      <p className="notice">
        Only admins can publish News. Students see published posts only. Phase 1: this editor
        saves nothing yet — the write path lands in P2, and the API says so honestly.
      </p>
      <form className="form" onSubmit={publish} style={{ maxWidth: 760 }}>
        <label>
          Title
          <input value={title} onChange={(e) => autoSlug(e.target.value)} required />
        </label>
        <label>
          Slug (auto-generated, editable)
          <input value={slug} onChange={(e) => setSlug(e.target.value)} required />
        </label>
        <label>
          Excerpt
          <textarea value={excerpt} onChange={(e) => setExcerpt(e.target.value)} rows={2} />
        </label>
        <label>
          Body (HTML — H2/H3, bold, bullets, numbered lists, blockquote, tables, links)
          <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={12} className="mono" />
        </label>
        <label>
          Featured image — URL
          <input value={imageUrl} onChange={(e) => setImageUrl(e.target.value)} placeholder="https://…" />
        </label>
        <label>
          Featured image — upload (R2 upload lands in P2; use a URL for now)
          <input type="file" accept="image/*" disabled />
        </label>
        <label>
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {CATEGORIES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          Tags (comma-separated)
          <input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="jamb, 2027, registration" />
        </label>
        <h3>SEO</h3>
        <label>
          SEO title (max 60 characters) — {seoTitle.length}/60
          <input value={seoTitle} onChange={(e) => setSeoTitle(e.target.value)} maxLength={60} />
        </label>
        <label>
          SEO description (max 160 characters) — {seoDescription.length}/160
          <textarea value={seoDescription} onChange={(e) => setSeoDescription(e.target.value)} maxLength={160} rows={2} />
        </label>
        <label>
          SEO keywords (comma-separated)
          <input value={seoKeywords} onChange={(e) => setSeoKeywords(e.target.value)} />
        </label>
        <label>
          Status
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="draft">Draft</option>
            <option value="published">Published</option>
            <option value="scheduled">Scheduled (goes live on first read after the publish date)</option>
          </select>
        </label>
        {error && <p className="error">{error}</p>}
        {message && <p className="notice">{message}</p>}
        <button type="submit" disabled={busy}>{busy ? 'Saving…' : 'Save post'}</button>
      </form>

      <h2 style={{ marginTop: '2rem' }}>Preview — table of contents</h2>
      {preview.toc.length >= 3 ? (
        <details className="post-toc" open>
          <summary>Table of Contents</summary>
          <ol>
            {preview.toc.map((t) => (
              <li key={t.id} className={t.level === 3 ? 'toc-l3' : undefined}>{t.text}</li>
            ))}
          </ol>
        </details>
      ) : (
        <p className="notice">Add at least 3 headings (H2/H3) and a table of contents will appear here, as in v1.</p>
      )}
    </div>
  )
}
