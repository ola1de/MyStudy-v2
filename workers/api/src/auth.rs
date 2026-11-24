//! Password + recovery-code + session-token helpers (architecture §2).
//!
//! Passwords: PBKDF2-HMAC-SHA256, 60,000 iterations, 16-byte salt,
//! 32-byte hash. Stored format:
//!   `pbkdf2$60000$<base64url salt>$<base64url hash>`
//! 60k (not 100k) is a deliberate Phase 1 choice for the 10 ms
//! free-tier CPU limit — see architecture §0. Measure on staging
//! before raising it; the format carries the iteration count, so
//! raising it later does not break existing logins.
//!
//! TODO (P2): encrypt `totp_secret_enc` at rest with AES-GCM, key in a
//! Cloudflare secret (`TOTP_ENC_KEY`). Phase 1 stores the base32
//! secret in that column as-is, and this is stated in the README.
//! Do not present Phase 1 storage as encrypted.

use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
use pbkdf2::pbkdf2_hmac;
use sha2::{Digest, Sha256};

pub const PASSWORD_MIN_LEN: usize = 12;
pub const PBKDF2_ITERATIONS: u32 = 60_000;

pub fn random_bytes(n: usize) -> Result<Vec<u8>, getrandom::Error> {
    let mut buf = vec![0u8; n];
    getrandom::fill(&mut buf)?;
    Ok(buf)
}

/// Hash a password into the stored `pbkdf2$...` format.
pub fn hash_password(password: &str) -> Result<String, getrandom::Error> {
    let salt = random_bytes(16)?;
    let mut hash = [0u8; 32];
    pbkdf2_hmac::<Sha256>(password.as_bytes(), &salt, PBKDF2_ITERATIONS, &mut hash);
    Ok(format!(
        "pbkdf2${}${}${}",
        PBKDF2_ITERATIONS,
        URL_SAFE_NO_PAD.encode(salt),
        URL_SAFE_NO_PAD.encode(hash)
    ))
}

/// Verify a password against a stored `pbkdf2$...` hash.
/// Returns false (never panics) on any malformed stored value.
pub fn verify_password(password: &str, stored: &str) -> bool {
    let parts: Vec<&str> = stored.split('$').collect();
    if parts.len() != 4 || parts[0] != "pbkdf2" {
        return false;
    }
    let iterations: u32 = match parts[1].parse() {
        Ok(n) => n,
        Err(_) => return false,
    };
    let salt = match URL_SAFE_NO_PAD.decode(parts[2]) {
        Ok(s) => s,
        Err(_) => return false,
    };
    let expected = match URL_SAFE_NO_PAD.decode(parts[3]) {
        Ok(h) => h,
        Err(_) => return false,
    };
    let mut hash = vec![0u8; expected.len()];
    pbkdf2_hmac::<Sha256>(password.as_bytes(), &salt, iterations, &mut hash);
    // Constant-time comparison.
    if hash.len() != expected.len() {
        return false;
    }
    hash.iter()
        .zip(expected.iter())
        .fold(0u8, |acc, (a, b)| acc | (a ^ b))
        == 0
}

/// Hash a normalised security-question answer. Same PBKDF2 scheme as
/// passwords, fewer iterations (answers are low-entropy by nature;
/// the email-code step in the reset flow is the real gate — see
/// architecture §2.2). Never store the answer itself.
pub fn hash_security_answer(normalised: &str) -> Result<String, getrandom::Error> {
    let salt = random_bytes(16)?;
    let mut hash = [0u8; 32];
    pbkdf2_hmac::<Sha256>(normalised.as_bytes(), &salt, 30_000, &mut hash);
    Ok(format!(
        "pbkdf2$30000${}${}",
        URL_SAFE_NO_PAD.encode(salt),
        URL_SAFE_NO_PAD.encode(hash)
    ))
}

// Used by the P2 password-reset handler (email code + 2 of 3 answers).
#[allow(dead_code)]
pub fn verify_security_answer(normalised: &str, stored: &str) -> bool {
    verify_password(normalised, stored)
}

/// SHA-256 hex of a string (session-token and recovery-code storage).
pub fn sha256_hex(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    hasher
        .finalize()
        .iter()
        .map(|b| format!("{:02x}", b))
        .collect()
}

/// 10 one-time recovery codes, shown to the user once at registration.
/// Returns `(plaintext_codes, json_array_of_sha256_hashes)` — the
/// plaintext list must never be stored or logged.
pub fn generate_recovery_codes() -> Result<(Vec<String>, String), getrandom::Error> {
    const CHARS: &[u8] = b"ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
    let mut codes = Vec::with_capacity(10);
    let mut hashes = Vec::with_capacity(10);
    for _ in 0..10 {
        let bytes = random_bytes(8)?;
        let mut code = String::with_capacity(9);
        for (i, &b) in bytes.iter().enumerate() {
            if i == 4 {
                code.push('-');
            }
            code.push(CHARS[(b % 32) as usize] as char);
        }
        hashes.push(sha256_hex(&code));
        codes.push(code);
    }
    let json = serde_json::to_string(&hashes).unwrap_or_else(|_| "[]".to_string());
    Ok((codes, json))
}

/// Opaque session token (32 random bytes, base64url). Only the
/// SHA-256 hash is stored in D1 (`sessions.token_hash`).
pub fn new_session_token() -> Result<(String, String), getrandom::Error> {
    let bytes = random_bytes(32)?;
    let token = URL_SAFE_NO_PAD.encode(&bytes);
    Ok((token.clone(), sha256_hex(&token)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn password_roundtrip() {
        let hash = hash_password("correct horse battery staple").unwrap();
        assert!(hash.starts_with("pbkdf2$60000$"));
        assert!(verify_password("correct horse battery staple", &hash));
        assert!(!verify_password("wrong password", &hash));
        assert!(!verify_password("correct horse battery staple", "garbage"));
        assert!(!verify_password("correct horse battery staple", "pbkdf2$60000$@@@$"));
    }

    #[test]
    fn recovery_codes_shape() {
        let (codes, json) = generate_recovery_codes().unwrap();
        assert_eq!(codes.len(), 10);
        assert!(codes.iter().all(|c| c.len() == 9 && c.as_bytes()[4] == b'-'));
        let hashes: Vec<String> = serde_json::from_str(&json).unwrap();
        assert_eq!(hashes.len(), 10);
        assert_eq!(sha256_hex(&codes[0]), hashes[0]);
    }
}
