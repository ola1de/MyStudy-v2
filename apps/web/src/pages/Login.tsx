import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../lib/api'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [totpCode, setTotpCode] = useState('')
  const [totpRequired, setTotpRequired] = useState(false)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setBusy(true)
    const r = await api.post<{ user_id: number; role: string; premium_status: string }>('/api/auth/login', {
      email,
      password,
      totp_code: totpCode,
    })
    setBusy(false)
    if (!r.ok) {
      if (r.error?.code === 'totp_required') setTotpRequired(true)
      setError(r.error?.message ?? 'Sign-in failed.')
      return
    }
    navigate('/')
  }

  return (
    <div className="page">
      <h1>Sign in</h1>
      <p>No account yet? <Link to="/register">Create one</Link></p>
      <form className="form" onSubmit={submit}>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {totpRequired && (
          <label>
            6-digit authenticator code (or a recovery code)
            <input value={totpCode} onChange={(e) => setTotpCode(e.target.value)} inputMode="numeric" placeholder="123456" />
          </label>
        )}
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>
      </form>
      <p><Link to="/register">Forgot your password?</Link> Password reset uses an email code plus your security questions — that flow lands in P2.</p>
    </div>
  )
}
