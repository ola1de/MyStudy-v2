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
  put: <T>(path: string, data: unknown) =>
    request<T>(path, { method: 'PUT', body: JSON.stringify(data) }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
}

// Admin upload: images only, max 2 MB (server enforces too).
export const MAX_UPLOAD_BYTES = 2 * 1024 * 1024

function arrayBufferToBase64(buf: ArrayBuffer): string {
  const bytes = new Uint8Array(buf)
  let binary = ''
  const CHUNK = 0x8000
  for (let i = 0; i < bytes.length; i += CHUNK) {
    binary += String.fromCharCode(...bytes.subarray(i, i + CHUNK))
  }
  return btoa(binary)
}

export async function uploadImage(file: File): Promise<ApiResult<{ key: string; url: string }>> {
  if (!file.type.startsWith('image/')) {
    return { ok: false, data: null, error: { code: 'not_image', message: 'Only image files can be uploaded.' } }
  }
  if (file.size > MAX_UPLOAD_BYTES) {
    return {
      ok: false,
      data: null,
      error: { code: 'too_large', message: `Image is ${(file.size / 1024 / 1024).toFixed(1)} MB — the maximum is 2 MB.` },
    }
  }
  const data_base64 = arrayBufferToBase64(await file.arrayBuffer())
  return api.post<{ key: string; url: string }>('/api/admin/upload', {
    filename: file.name,
    content_type: file.type,
    data_base64,
  })
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

// Full admin post, per the /api/admin/news contract.
export interface AdminNewsPost {
  id: number
  slug: string
  title: string
  excerpt: string | null
  body_html: string
  featured_image_url: string | null
  featured_image_r2_key: string | null
  category: string | null
  tags: string[]
  seo_title: string | null
  seo_description: string | null
  seo_keywords: string | null
  og_image: string | null
  status: 'draft' | 'published' | 'scheduled'
  published_at: string | null
  created_at: string
  updated_at: string
}

export interface NewsCategory {
  id: number
  slug: string
  name: string
}
