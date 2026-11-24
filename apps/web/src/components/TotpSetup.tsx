import { useEffect, useState } from 'react'
import QRCode from 'qrcode'

// Renders the otpauth URL as a QR code SVG entirely in the browser —
// no external QR service is called at runtime. The manual secret is
// shown alongside it for users who cannot scan.
export default function TotpSetup({ otpauthUrl, secret }: { otpauthUrl: string; secret: string }) {
  const [svg, setSvg] = useState('')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    let alive = true
    QRCode.toString(otpauthUrl, { type: 'svg', margin: 1, width: 220 })
      .then((s) => {
        if (alive) setSvg(s)
      })
      .catch(() => setSvg(''))
    return () => {
      alive = false
    }
  }, [otpauthUrl])

  async function copySecret() {
    try {
      await navigator.clipboard.writeText(secret)
      setCopied(true)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div>
      <p>Scan this QR code with Google Authenticator, Authy, or any authenticator app:</p>
      {svg ? (
        <div className="qr-box" dangerouslySetInnerHTML={{ __html: svg }} />
      ) : (
        <p className="notice">QR code could not be rendered — use the manual code below.</p>
      )}
      <p>
        Can&apos;t scan? Copy this code into your authenticator app instead:
      </p>
      <p className="mono">{secret}</p>
      <button type="button" className="ghost" onClick={copySecret}>
        {copied ? 'Copied' : 'Copy manual code'}
      </button>
    </div>
  )
}
