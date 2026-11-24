import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import TotpSetup from '../components/TotpSetup'
import { api } from '../lib/api'
import { SECURITY_QUESTIONS } from '../lib/securityQuestions'

interface RegisterResponse {
  user_id: number
  totp_secret: string
  otpauth_url: string
  recovery_codes: string[]
}

export default function Register() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [examTarget, setExamTarget] = useState('JAMB')
  const [q, setQ] = useState(['first-school', 'first-pet', 'birth-city'])
  const [a, setA] = useState(['', '', ''])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [setup, setSetup] = useState<RegisterResponse | null>(null)
  const [code, setCode] = useState('')
  const [verified, setVerified] = useState(false)

  function setQuestion(i: number, value: string) {
    setQ((prev) => prev.map((v, j) => (j === i ? value : v)))
  }
  function setAnswer(i: number, value: string) {
    setA((prev) => prev.map((v, j) => (j === i ? value : v)))
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (new Set(q).size !== 3) {
      setError('Pick 3 different security questions.')
      return
    }
    setBusy(true)
    const r = await api.post<RegisterResponse>('/api/auth/register-start', {
      name,
      email,
      password,
      exam_target: examTarget,
      security_questions: q.map((question, i) => ({ question, answer: a[i] })),
    })
    setBusy(false)
    if (!r.ok || !r.data) {
      setError(r.error?.message ?? 'Registration failed.')
      return
    }
    setSetup(r.data)
  }

  async function verify(e: React.FormEvent) {
    e.preventDefault()
    if (!setup) return
    setError('')
    setBusy(true)
    const r = await api.post<{ totp_enabled: boolean }>('/api/auth/totp-verify', {
      user_id: setup.user_id,
      code,
    })
    setBusy(false)
    if (!r.ok) {
      setError(r.error?.message ?? 'That code is not valid.')
      return
    }
    setVerified(true)
  }

  if (verified) {
    return (
      <div className="page">
        <h1>Your account is active</h1>
        <p className="notice">
          Two-factor authentication is on. Keep your authenticator app handy — you will need a
          code every time you sign in.
        </p>
        <button type="button" onClick={() => navigate('/')}>Go to MyStudy</button>
      </div>
    )
  }

  if (setup) {
    return (
      <div className="page">
        <h1>Set up two-factor authentication</h1>
        <p>
          Two-factor authentication is compulsory. Scan the QR code below, then enter the 6-digit
          code from your authenticator app to finish registration.
        </p>
        <TotpSetup otpauthUrl={setup.otpauth_url} secret={setup.totp_secret} />
        <div className="notice" style={{ marginTop: '1rem' }}>
          <strong>Save these recovery codes now — they are shown once only.</strong>
          <p className="mono">{setup.recovery_codes.join('  ')}</p>
          <p>Each code works once, if you lose access to your authenticator app.</p>
        </div>
        <form className="form" onSubmit={verify} style={{ marginTop: '1rem' }}>
          <label>
            6-digit code from your authenticator app
            <input value={code} onChange={(e) => setCode(e.target.value)} inputMode="numeric" maxLength={6} placeholder="123456" />
          </label>
          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={busy}>{busy ? 'Verifying…' : 'Verify and activate my account'}</button>
        </form>
      </div>
    )
  }

  return (
    <div className="page">
      <h1>Create your account</h1>
      <p>Already have an account? <Link to="/login">Sign in</Link></p>
      <form className="form" onSubmit={submit}>
        <label>
          Full name
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password (at least 12 characters)
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={12} required />
        </label>
        <label>
          Exam target
          <select value={examTarget} onChange={(e) => setExamTarget(e.target.value)}>
            <option>JAMB</option>
            <option>WAEC</option>
            <option>NECO</option>
            <option>Post-UTME</option>
          </select>
        </label>
        <h3>Security questions — for password recovery</h3>
        <p>Pick 3 different questions. Your answers are hashed on the server and never shown to anyone.</p>
        {[0, 1, 2].map((i) => (
          <div key={i}>
            <label>
              Question {i + 1}
              <select value={q[i]} onChange={(e) => setQuestion(i, e.target.value)}>
                {SECURITY_QUESTIONS.map((s) => (
                  <option key={s.id} value={s.id} disabled={q.some((v, j) => j !== i && v === s.id)}>
                    {s.text}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Your answer
              <input value={a[i]} onChange={(e) => setAnswer(i, e.target.value)} required minLength={2} />
            </label>
          </div>
        ))}
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={busy}>{busy ? 'Creating…' : 'Create account'}</button>
      </form>
    </div>
  )
}
