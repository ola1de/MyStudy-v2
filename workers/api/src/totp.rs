//! TOTP (RFC 6238 / RFC 4226) — hand-rolled, no TOTP crate.
//!
//! Written for MyStudy v2 from the RFCs, not copied from any other
//! project. Secrets are 20 random bytes (160 bits), base32-encoded per
//! RFC 4648. Codes are 6 digits, 30-second steps, verified with a
//! ±1-step window. The otpauth URL is what the frontend turns into a
//! QR code locally (no external QR service at runtime).

use hmac::{Hmac, Mac};
use sha1::Sha1;

type HmacSha1 = Hmac<Sha1>;

const BASE32_ALPHABET: &[u8; 32] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

/// RFC 4648 base32 encode, no padding (authenticator apps accept both;
/// no-padding matches the common otpauth form).
pub fn base32_encode(bytes: &[u8]) -> String {
    let mut out = String::new();
    let mut buffer: u32 = 0;
    let mut bits = 0;
    for &b in bytes {
        buffer = (buffer << 8) | b as u32;
        bits += 8;
        while bits >= 5 {
            bits -= 5;
            out.push(BASE32_ALPHABET[((buffer >> bits) & 31) as usize] as char);
        }
    }
    if bits > 0 {
        out.push(BASE32_ALPHABET[((buffer << (5 - bits)) & 31) as usize] as char);
    }
    out
}

/// RFC 4648 base32 decode. Accepts upper/lower case, with or without
/// `=` padding. Returns `None` on any invalid character.
pub fn base32_decode(input: &str) -> Option<Vec<u8>> {
    let mut out = Vec::new();
    let mut buffer: u32 = 0;
    let mut bits = 0;
    for c in input.chars() {
        if c == '=' {
            break;
        }
        let v = match c.to_ascii_uppercase() {
            'A'..='Z' => c.to_ascii_uppercase() as u32 - 'A' as u32,
            '2'..='7' => c as u32 - '2' as u32 + 26,
            _ => return None,
        };
        buffer = (buffer << 5) | v;
        bits += 5;
        if bits >= 8 {
            bits -= 8;
            out.push((buffer >> bits) as u8);
        }
    }
    Some(out)
}

fn hotp_code(key: &[u8], counter: u64) -> String {
    let mut mac = HmacSha1::new_from_slice(key).expect("HMAC key length is always valid");
    mac.update(&counter.to_be_bytes());
    let hash = mac.finalize().into_bytes();
    let offset = (hash[19] & 0x0f) as usize;
    let code = (((hash[offset] & 0x7f) as u32) << 24)
        | ((hash[offset + 1] as u32) << 16)
        | ((hash[offset + 2] as u32) << 8)
        | (hash[offset + 3] as u32);
    format!("{:06}", code % 1_000_000)
}

/// TOTP code for a base32 secret at `now_ms` (milliseconds since epoch).
/// Used by the unit tests and by P2 handlers that need to display/verify
/// a code server-side; the login path uses `verify_totp` directly.
#[allow(dead_code)]
pub fn totp_code(secret: &str, now_ms: u64) -> Option<String> {
    let key = base32_decode(secret)?;
    Some(hotp_code(&key, now_ms / 30_000))
}

/// Verify a 6-digit code, accepting the current step and ±1 step
/// (clock skew). The code must be exactly 6 ASCII digits.
pub fn verify_totp(secret: &str, code: &str, now_ms: u64) -> bool {
    if code.len() != 6 || !code.bytes().all(|b| b.is_ascii_digit()) {
        return false;
    }
    let key = match base32_decode(secret) {
        Some(k) => k,
        None => return false,
    };
    let step = now_ms / 30_000;
    [step.wrapping_sub(1), step, step + 1]
        .iter()
        .any(|&s| hotp_code(&key, s) == code)
}

/// Generate a fresh 20-byte TOTP secret (base32). Randomness comes from
/// `getrandom` (JS `crypto.getRandomValues` on wasm32).
pub fn generate_totp_secret() -> Result<String, getrandom::Error> {
    let mut bytes = [0u8; 20];
    getrandom::fill(&mut bytes)?;
    Ok(base32_encode(&bytes))
}

fn percent_encode(s: &str) -> String {
    let mut out = String::new();
    for b in s.bytes() {
        match b {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'-' | b'_' | b'.' | b'~' => {
                out.push(b as char)
            }
            _ => out.push_str(&format!("%{:02X}", b)),
        }
    }
    out
}

/// `otpauth://` URL for the QR code / manual entry.
/// Example: `otpauth://totp/MyStudy:user@example.com?secret=...&issuer=MyStudy&algorithm=SHA1&digits=6&period=30`
pub fn totp_setup_url(secret: &str, account: &str, issuer: &str) -> String {
    format!(
        "otpauth://totp/{}:{}?secret={}&issuer={}&algorithm=SHA1&digits=6&period=30",
        percent_encode(issuer),
        percent_encode(account),
        secret,
        percent_encode(issuer)
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn base32_roundtrip() {
        let bytes: Vec<u8> = (0u8..20).collect();
        assert_eq!(base32_decode(&base32_encode(&bytes)).unwrap(), bytes);
        // RFC 4648 test vector: "foobar" -> "MZXW6YTBOI======"
        assert_eq!(base32_encode(b"foobar"), "MZXW6YTBOI");
        assert_eq!(base32_decode("MZXW6YTBOI======").unwrap(), b"foobar");
        assert_eq!(base32_decode("mzxw6ytboi").unwrap(), b"foobar");
        assert!(base32_decode("not!valid").is_none());
    }

    #[test]
    fn hotp_rfc4226_vectors() {
        // RFC 4226 Appendix D: secret is ASCII "12345678901234567890".
        let secret = base32_encode(b"12345678901234567890");
        let key = base32_decode(&secret).unwrap();
        assert_eq!(hotp_code(&key, 0), "755224");
        assert_eq!(hotp_code(&key, 1), "287082");
        assert_eq!(hotp_code(&key, 2), "359152");
        assert_eq!(hotp_code(&key, 9), "520489");
    }

    #[test]
    fn totp_verify_window() {
        let secret = base32_encode(b"12345678901234567890");
        // Counter 1 == 30_000 ms. Code for counter 1 must verify at
        // 30_000 ms, and also one step either side.
        let code = totp_code(&secret, 30_000).unwrap();
        assert_eq!(code, "287082");
        assert!(verify_totp(&secret, &code, 30_000));
        assert!(verify_totp(&secret, &code, 0));
        assert!(verify_totp(&secret, &code, 60_000));
        assert!(!verify_totp(&secret, &code, 120_000));
        assert!(!verify_totp(&secret, "000000", 30_000));
        assert!(!verify_totp(&secret, "12345", 30_000));
        assert!(!verify_totp(&secret, "1234567", 30_000));
    }

    #[test]
    fn otpauth_url_shape() {
        let url = totp_setup_url("JBSWY3DPEHPK3PXP", "user@example.com", "MyStudy");
        assert_eq!(
            url,
            "otpauth://totp/MyStudy:user%40example.com?secret=JBSWY3DPEHPK3PXP&issuer=MyStudy&algorithm=SHA1&digits=6&period=30"
        );
    }
}
