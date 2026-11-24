import { useCallback, useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api, uploadImage, type AdminNewsPost, type NewsCategory } from '../lib/api'
import { buildToc, readTimeMinutes } from '../lib/toc'
import './admin.css'

// Blogger-like News editor (admin only): create AND edit.
// Body is kept as HTML in a contenteditable area; the toolbar uses
// document.execCommand on that element. Preview renders the post in the
// v1 format (eyebrow, Fraunces title, meta, featured image, TOC, body,
// tags) — the same approach as PostPage.
function slugifyTitle(value: string) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 80)
}

function toLocalInput(iso: string | null): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

export default function AdminEditor() {
  const { slug: editSlug } = useParams<{ slug: string }>()
  const isEdit = Boolean(editSlug)
  const navigate = useNavigate()
  const bodyRef = useRef<HTMLDivElement>(null)
  const bodyImageInputRef = useRef<HTMLInputElement>(null)
  const featuredImageInputRef = useRef<HTMLInputElement>(null)

  const [title, setTitle] = useState('')
  const [slug, setSlug] = useState('')
  const [slugTouched, setSlugTouched] = useState(false)
  const [excerpt, setExcerpt] = useState('')
  const [bodyHtml, setBodyHtml] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [imageR2Key, setImageR2Key] = useState('')
  const [categories, setCategories] = useState<NewsCategory[]>([])
  const [category, setCategory] = useState('')
  const [newCategory, setNewCategory] = useState('')
  const [showNewCategory, setShowNewCategory] = useState(false)
  const [tags, setTags] = useState('')
  const [seoTitle, setSeoTitle] = useState('')
  const [seoDescription, setSeoDescription] = useState('')
  const [seoKeywords, setSeoKeywords] = useState('')
  const [ogImage, setOgImage] = useState('')
  const [status, setStatus] = useState<'draft' | 'published' | 'scheduled'>('draft')
  const [publishAt, setPublishAt] = useState('')
  const [showPreview, setShowPreview] = useState(false)
  const [loading, setLoading] = useState(isEdit)
  const [notAdmin, setNotAdmin] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  const loadCategories = useCallback(async () => {
    const r = await api.get<{ categories: NewsCategory[] }>('/api/admin/news-categories')
    if (r.ok && r.data) setCategories(r.data.categories)
  }, [])

  useEffect(() => {
    loadCategories()
  }, [loadCategories])

  useEffect(() => {
    if (!editSlug) return
    setLoading(true)
    api
      .get<AdminNewsPost>(`/api/admin/news/${encodeURIComponent(editSlug)}`)
      .then((r) => {
        setLoading(false)
        if (!r.ok || !r.data) {
          if (/not an admin|forbidden/i.test(r.error?.message ?? '')) setNotAdmin(true)
          else setError(r.error?.message ?? 'Could not load the post.')
          return
        }
        const p = r.data
        setTitle(p.title)
        setSlug(p.slug)
        setSlugTouched(true)
        setExcerpt(p.excerpt ?? '')
        setBodyHtml(p.body_html)
        setImageUrl(p.featured_image_url ?? '')
        setImageR2Key(p.featured_image_r2_key ?? '')
        setCategory(p.category ?? '')
        setTags(p.tags.join(', '))
        setSeoTitle(p.seo_title ?? '')
        setSeoDescription(p.seo_description ?? '')
        setSeoKeywords(p.seo_keywords ?? '')
        setOgImage(p.og_image ?? '')
        setStatus(p.status)
        setPublishAt(toLocalInput(p.published_at))
      })
      .catch(() => {
        setLoading(false)
        setError('Could not reach the server.')
      })
  }, [editSlug])

  // Keep the contenteditable in sync when the post loads (edit mode).
  useEffect(() => {
    if (bodyRef.current && bodyRef.current.innerHTML !== bodyHtml) {
      bodyRef.current.innerHTML = bodyHtml
    }
  }, [bodyHtml])

  function onTitleChange(value: string) {
    setTitle(value)
    if (!slugTouched) setSlug(slugifyTitle(value))
  }

  function exec(command: string, value?: string) {
    bodyRef.current?.focus()
    document.execCommand(command, false, value)
    syncBody()
  }

  function syncBody() {
    if (bodyRef.current) setBodyHtml(bodyRef.current.innerHTML)
  }

  function formatBlock(tag: string) {
    exec('formatBlock', tag)
  }

  function insertLink() {
    const url = window.prompt('Link URL', 'https://')
    if (!url) return
    exec('createLink', url)
  }

  async function insertImageFromFile(file: File | undefined) {
    if (!file) return
    setUploading(true)
    setUploadError('')
    const r = await uploadImage(file)
    setUploading(false)
    if (!r.ok || !r.data) {
      setUploadError(r.error?.message ?? 'Image upload failed.')
      return
    }
    exec('insertImage', r.data.url)
  }

  function insertImageFromUrl() {
    const url = window.prompt('Image URL', 'https://')
    if (!url) return
    exec('insertImage', url)
  }

  async function handleFeaturedUpload(file: File | undefined) {
    if (!file) return
    setUploading(true)
    setUploadError('')
    const r = await uploadImage(file)
    setUploading(false)
    if (!r.ok || !r.data) {
      setUploadError(r.error?.message ?? 'Image upload failed.')
      return
    }
    setImageUrl(r.data.url)
    setImageR2Key(r.data.key)
  }

  async function createCategory() {
    const name = newCategory.trim()
    if (!name) return
    setError('')
    const r = await api.post<NewsCategory>('/api/admin/news-categories', { name })
    if (!r.ok || !r.data) {
      setError(r.error?.message ?? 'Could not create the category.')
      return
    }
    setCategories((prev) => [...prev, r.data!])
    setCategory(r.data.slug)
    setNewCategory('')
    setShowNewCategory(false)
  }

  function buildPayload(saveStatus: 'draft' | 'published' | 'scheduled') {
    return {
      title: title.trim(),
      slug: slug.trim(),
      excerpt: excerpt.trim() || null,
      body_html: bodyHtml,
      featured_image_url: imageUrl.trim() || null,
      featured_image_r2_key: imageR2Key || null,
      category: category || null,
      tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
      seo_title: seoTitle.trim() || null,
      seo_description: seoDescription.trim() || null,
      seo_keywords: seoKeywords.trim() || null,
      og_image: ogImage.trim() || null,
      status: saveStatus,
      published_at:
        saveStatus === 'scheduled'
          ? publishAt
            ? new Date(publishAt).toISOString()
            : null
          : saveStatus === 'published'
            ? publishAt
              ? new Date(publishAt).toISOString()
              : new Date().toISOString()
            : publishAt
              ? new Date(publishAt).toISOString()
              : null,
    }
  }

  async function save(saveStatus: 'draft' | 'published' | 'scheduled') {
    if (!title.trim()) {
      setError('A title is required.')
      return
    }
    if (!slug.trim()) {
      setError('A slug is required.')
      return
    }
    if (saveStatus === 'scheduled' && !publishAt) {
      setError('Choose a publish date and time for a scheduled post.')
      return
    }
    setError('')
    setMessage('')
    setBusy(true)
    const payload = buildPayload(saveStatus)
    const r = isEdit
      ? await api.put<AdminNewsPost>(`/api/admin/news/${encodeURIComponent(editSlug!)}`, payload)
      : await api.post<AdminNewsPost>('/api/admin/news', payload)
    setBusy(false)
    if (!r.ok || !r.data) {
      // 403 = not an admin; 409 = duplicate slug.
      setError(r.error?.message ?? 'Could not save the post.')
      return
    }
    setMessage(
      saveStatus === 'published'
        ? `Published: ${r.data.slug}`
        : saveStatus === 'scheduled'
          ? `Scheduled for ${publishAt.replace('T', ' ')}: ${r.data.slug}`
          : `Draft saved: ${r.data.slug}`,
    )
    if (!isEdit) navigate(`/admin/posts/${encodeURIComponent(r.data.slug)}/edit`, { replace: true })
  }

  const { toc, htmlWithIds } = buildToc(bodyHtml)
  const previewDate = status === 'scheduled' && publishAt ? publishAt : new Date().toISOString()

  if (notAdmin) {
    return (
      <div className="page admin-page">
        <h1>{isEdit ? 'Edit post' : 'New post'}</h1>
        <p className="admin-error">You are not signed in as an admin. Only admins can manage News posts.</p>
        <p><Link to="/login">Sign in</Link> · <Link to="/admin/posts">Back to Posts</Link></p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="page admin-page">
        <p>Loading post…</p>
      </div>
    )
  }

  return (
    <div className="page admin-page admin-editor-page">
      <div className="admin-head">
        <div>
          <h1>{isEdit ? 'Edit post' : 'New post'}</h1>
          <p className="admin-sub">
            <Link to="/admin/posts">← All posts</Link>
          </p>
        </div>
        <div className="admin-actions">
          <button type="button" className="admin-btn" onClick={() => setShowPreview((v) => !v)}>
            {showPreview ? 'Back to editing' : 'Preview'}
          </button>
          <button type="button" className="admin-btn" disabled={busy} onClick={() => save('draft')}>
            {busy ? 'Saving…' : 'Save draft'}
          </button>
          <button type="button" className="admin-btn admin-btn-primary" disabled={busy} onClick={() => save(status === 'scheduled' ? 'scheduled' : 'published')}>
            {busy ? 'Saving…' : status === 'scheduled' ? 'Schedule' : 'Publish'}
          </button>
        </div>
      </div>

      {error && <p className="admin-error">{error}</p>}
      {message && <p className="admin-notice">{message}</p>}

      {showPreview ? (
        <article className="admin-preview" style={{ maxWidth: 880 }}>
          {category && <span className="eyebrow">{categories.find((c) => c.slug === category)?.name ?? category}</span>}
          <h1 className="post-title">{title || 'Untitled post'}</h1>
          <p className="post-meta">
            {new Date(previewDate).toLocaleDateString('en-NG', { day: 'numeric', month: 'long', year: 'numeric' })}
            {' · '}
            {readTimeMinutes(bodyHtml)} min read
            {status !== 'published' && ` · ${status}`}
          </p>
          {imageUrl && <img className="featured-image" src={imageUrl} alt={title} />}
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
          {tags.split(',').map((t) => t.trim()).filter(Boolean).length > 0 && (
            <p>
              {tags.split(',').map((t) => t.trim()).filter(Boolean).map((t) => (
                <span className="tag" key={t}>{t}</span>
              ))}
            </p>
          )}
          <p className="admin-sub">Preview only — not published until you save.</p>
        </article>
      ) : (
        <form className="admin-form" onSubmit={(e) => { e.preventDefault(); save('draft') }}>
          <label>
            Title
            <input value={title} onChange={(e) => onTitleChange(e.target.value)} required />
          </label>
          <label>
            Slug (auto-generated from the title, editable)
            <input
              value={slug}
              onChange={(e) => { setSlug(e.target.value); setSlugTouched(true) }}
              required
            />
          </label>

          <div className="admin-toolbar" role="toolbar" aria-label="Formatting">
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => formatBlock('h2')}>H2</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => formatBlock('h3')}>H3</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => exec('bold')}><strong>B</strong></button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => exec('italic')}><em>I</em></button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => exec('insertUnorderedList')}>Bullets</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => exec('insertOrderedList')}>1. List</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => formatBlock('blockquote')}>Quote</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => formatBlock('pre')}>Code</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={insertLink}>Link</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => bodyImageInputRef.current?.click()}>Image</button>
            <button type="button" onMouseDown={(e) => e.preventDefault()} onClick={insertImageFromUrl}>Image URL</button>
            <input
              ref={bodyImageInputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={(e) => { insertImageFromFile(e.target.files?.[0]); e.target.value = '' }}
            />
          </div>
          <div
            ref={bodyRef}
            className="admin-body-editor"
            contentEditable
            suppressContentEditableWarning
            onInput={syncBody}
            aria-label="Post body"
          />

          <label>
            Excerpt
            <textarea value={excerpt} onChange={(e) => setExcerpt(e.target.value)} rows={2} />
          </label>

          <fieldset className="admin-fieldset">
            <legend>Featured image</legend>
            <div className="admin-image-row">
              <button type="button" className="admin-btn" disabled={uploading} onClick={() => featuredImageInputRef.current?.click()}>
                {uploading ? 'Uploading…' : 'Upload image (max 2 MB)'}
              </button>
              <input
                ref={featuredImageInputRef}
                type="file"
                accept="image/*"
                hidden
                onChange={(e) => { handleFeaturedUpload(e.target.files?.[0]); e.target.value = '' }}
              />
              <span>or paste a URL:</span>
              <input
                value={imageUrl}
                onChange={(e) => { setImageUrl(e.target.value); setImageR2Key('') }}
                placeholder="https://…"
              />
            </div>
            {uploadError && <p className="admin-error">{uploadError}</p>}
            {imageUrl && (
              <img className="admin-image-preview" src={imageUrl} alt="Featured image preview" />
            )}
          </fieldset>

          <label>
            Category
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              <option value="">No category</option>
              {categories.map((c) => (
                <option key={c.id} value={c.slug}>{c.name}</option>
              ))}
            </select>
          </label>
          {!showNewCategory ? (
            <button type="button" className="admin-btn admin-link-btn" onClick={() => setShowNewCategory(true)}>
              + Create new category
            </button>
          ) : (
            <div className="admin-inline-row">
              <input
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                placeholder="New category name"
                aria-label="New category name"
              />
              <button type="button" className="admin-btn admin-btn-primary" onClick={createCategory}>Create</button>
              <button type="button" className="admin-btn" onClick={() => { setShowNewCategory(false); setNewCategory('') }}>Cancel</button>
            </div>
          )}

          <label>
            Tags (comma-separated)
            <input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="jamb, 2027, registration" />
          </label>

          <h3>SEO</h3>
          <label>
            SEO title ({seoTitle.length}/60)
            <input value={seoTitle} onChange={(e) => setSeoTitle(e.target.value)} maxLength={60} placeholder={title || 'Defaults to the post title'} />
          </label>
          <label>
            SEO description ({seoDescription.length}/160)
            <textarea value={seoDescription} onChange={(e) => setSeoDescription(e.target.value)} maxLength={160} rows={2} placeholder={excerpt || 'Defaults to the excerpt'} />
          </label>
          <label>
            SEO keywords (comma-separated)
            <input value={seoKeywords} onChange={(e) => setSeoKeywords(e.target.value)} />
          </label>
          <label>
            OG image (URL, or reuse the featured image)
            <input value={ogImage} onChange={(e) => setOgImage(e.target.value)} placeholder="https://…" />
          </label>
          {imageUrl && !ogImage && (
            <button type="button" className="admin-btn admin-link-btn" onClick={() => setOgImage(imageUrl)}>
              Use featured image as OG image
            </button>
          )}

          <label>
            Status
            <select value={status} onChange={(e) => setStatus(e.target.value as 'draft' | 'published' | 'scheduled')}>
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="scheduled">Scheduled</option>
            </select>
          </label>
          {status === 'scheduled' && (
            <label>
              Publish date and time
              <input type="datetime-local" value={publishAt} onChange={(e) => setPublishAt(e.target.value)} required />
            </label>
          )}
          {status === 'published' && (
            <label>
              Publish date and time (leave blank for now)
              <input type="datetime-local" value={publishAt} onChange={(e) => setPublishAt(e.target.value)} />
            </label>
          )}
        </form>
      )}
    </div>
  )
}
