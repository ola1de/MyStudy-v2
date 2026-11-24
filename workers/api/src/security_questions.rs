//! The fixed list of 12 security questions (architecture §2.1).
//!
//! Deliberately excludes "mother's maiden name" — too guessable.
//! A user picks 3 *different* questions at registration. Answers are
//! normalised (lowercase, trimmed, collapsed whitespace) and hashed
//! server-side in `auth.rs`; they are never stored or returned plaintext.

/// (id, question text). The id is what the client sends and what is
/// stored in `users.security_q1..3`.
pub const SECURITY_QUESTIONS: [(&str, &str); 12] = [
    ("first-school", "What was the name of your first primary school?"),
    ("fav-teacher", "What is the surname of your favourite teacher?"),
    ("first-pet", "What was the name of your first pet?"),
    ("birth-city", "In which city were you born?"),
    ("best-friend", "What is the first name of your best friend in secondary school?"),
    ("first-phone", "What was the brand of your first mobile phone?"),
    ("fav-food", "What is your favourite food?"),
    ("childhood-nickname", "What nickname did your family call you as a child?"),
    ("first-book", "What was the title of the first book you remember reading?"),
    ("fav-subject", "What was your favourite subject in secondary school?"),
    ("first-job", "Where did you have your first job or holiday job?"),
    ("grandmother-first-name", "What is your maternal grandmother's first name?"),
];

/// True when `id` is one of the 12 fixed questions.
pub fn is_valid_question(id: &str) -> bool {
    SECURITY_QUESTIONS.iter().any(|(qid, _)| *qid == id)
}

/// Normalise a security answer before hashing: lowercase, trim,
/// collapse internal whitespace. Two answers that differ only by
/// case/spacing must match on recovery.
pub fn normalize_answer(answer: &str) -> String {
    answer
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
        .to_lowercase()
}
