// Table of contents, same rules as the v1 template shell path:
// scan H2/H3, slugify (max 60 chars, dedup -2/-3), show only if >= 3 headings.
export interface TocEntry {
  id: string
  text: string
  level: number
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 60)
    .replace(/-+$/, '')
}

export function buildToc(html: string): { toc: TocEntry[]; htmlWithIds: string } {
  const seen = new Map<string, number>()
  const toc: TocEntry[] = []
  const htmlWithIds = html.replace(/<(h[23])([^>]*)>(.*?)<\/\1>/gi, (_m, tag, attrs, inner) => {
    const text = inner.replace(/<[^>]+>/g, '').trim()
    if (!text) return _m
    let slug = slugify(text) || 'section'
    const n = (seen.get(slug) ?? 0) + 1
    seen.set(slug, n)
    if (n > 1) slug = `${slug}-${n}`
    const level = tag === 'h2' ? 2 : 3
    toc.push({ id: slug, text, level })
    const cleaned = attrs.replace(/\s+id="[^"]*"/, '')
    return `<${tag}${cleaned} id="${slug}" class="anchor-heading">${inner}</${tag}>`
  })
  return { toc: toc.length >= 3 ? toc : [], htmlWithIds }
}

export function readTimeMinutes(html: string): number {
  const words = html.replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / 220))
}
