export interface ApiResult<T> {
  ok: boolean
  data: T | null
  error: { code: string; message: string } | null
}

async function request<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  const res = await fetch(path, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init,
  })
  const body = (await res.json().catch(() => null)) as ApiResult<T> | null
  if (!body) return { ok: false, data: null, error: { code: 'network', message: 'Could not reach the server.' } }
  return body
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, data: unknown) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(data) }),
}

export interface NewsPost {
  slug: string
  title: string
  excerpt: string | null
  body_html: string
  featured_image_url: string | null
  category: string | null
  tags: string[]
  seo_title: string | null
  seo_description: string | null
  published_at: string | null
  toc: { id: string; text: string; level: number }[]
}
