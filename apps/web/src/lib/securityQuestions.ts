// The fixed list of 12 security questions (must match
// workers/api/src/security_questions.rs exactly — same ids, same order).
export const SECURITY_QUESTIONS: { id: string; text: string }[] = [
  { id: 'first-school', text: 'What was the name of your first primary school?' },
  { id: 'fav-teacher', text: 'What is the surname of your favourite teacher?' },
  { id: 'first-pet', text: 'What was the name of your first pet?' },
  { id: 'birth-city', text: 'In which city were you born?' },
  { id: 'best-friend', text: 'What is the first name of your best friend in secondary school?' },
  { id: 'first-phone', text: 'What was the brand of your first mobile phone?' },
  { id: 'fav-food', text: 'What is your favourite food?' },
  { id: 'childhood-nickname', text: 'What nickname did your family call you as a child?' },
  { id: 'first-book', text: 'What was the title of the first book you remember reading?' },
  { id: 'fav-subject', text: 'What was your favourite subject in secondary school?' },
  { id: 'first-job', text: 'Where did you have your first job or holiday job?' },
  { id: 'grandmother-first-name', text: "What is your maternal grandmother's first name?" },
]
