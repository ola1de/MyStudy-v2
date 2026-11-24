import { useEffect, useState, type JSX } from 'react'
import { Link } from 'react-router-dom'
import HeroArt from '../components/HeroArt'
import {
  IconArrowRight,
  IconBookOpen,
  IconCalendar,
  IconCap,
  IconChart,
  IconChat,
  IconCheck,
  IconClipboardCheck,
  IconClock,
  IconLayers,
  IconPen,
  IconScale,
  IconTarget,
  IconWrench,
} from '../components/icons'
import { api, type NewsPost } from '../lib/api'
import { TOOLS } from '../lib/tools'
import {
  EXAM_QUESTIONS,
  EXAM_SUBJECTS,
  KEYPOINTS,
  PRACTICE_QUESTIONS,
  VOCABULARY,
} from '../data/content'

// Homepage — editorial, in the v1 Blogger template's own language:
// Fraunces headings, Inter body, dark navy header strip, real numbers
// counted from the repos. No greeting, no gradient hero, no marketing copy.
// Every figure below comes from tools/generate-content-data.py.
const fmt = (n: number) => n.toLocaleString('en-NG')

const TOOL_GROUPS: { heading: string; note: string; items: { icon: JSX.Element; title: string; desc: string; to: string }[] }[] = [
  {
    heading: 'Exams & admission',
    note: 'The tools students open first, in exam season.',
    items: [
      { icon: <IconClipboardCheck />, title: 'CBT Practice', desc: 'Timed JAMB, WAEC, NECO and Post-UTME mocks, marked the way the real exam is marked.', to: '/tools' },
      { icon: <IconTarget />, title: 'Admission Toolkit', desc: 'JAMB subject combinations for your course, and a Post-UTME aggregate predictor.', to: '/tools' },
      { icon: <IconScale />, title: 'Legal & Civic Library', desc: 'The 1999 Constitution, chapter by chapter, plus the civic documents students are asked about.', to: '/tools' },
    ],
  },
  {
    heading: 'Study & planning',
    note: 'For the term, not just the exam hall.',
    items: [
      { icon: <IconLayers />, title: 'Flashcards', desc: 'Spaced-repetition decks built from the keypoints and vocabulary banks.', to: '/tools' },
      { icon: <IconCalendar />, title: 'Study Planner', desc: 'Timetable, lecture schedule, revision plan and deadlines in one place.', to: '/tools' },
      { icon: <IconChart />, title: 'CGPA Calculator', desc: '4.0 and 5.0 scales, semester GPA, class of degree and a printable transcript.', to: '/tools' },
    ],
  },
  {
    heading: 'Writing & language',
    note: 'For assignments, essays and English papers.',
    items: [
      { icon: <IconPen />, title: 'Word Office', desc: 'Write and export documents, with citations that actually follow a style guide.', to: '/tools' },
      { icon: <IconBookOpen />, title: 'Dictionary', desc: '121,340 entries from the MyStudy dictionary bank, with pronunciation.', to: '/tools' },
      { icon: <IconChat />, title: 'Vocabulary Trainer', desc: '4,400 words across 44 categories, tested the way JAMB tests them.', to: '/vocabulary' },
    ],
  },
]

export default function Home() {
  const [posts, setPosts] = useState<NewsPost[]>([])
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    api
      .get<{ posts: NewsPost[] }>('/api/news')
      .then((r) => {
        if (r.ok && r.data) setPosts(r.data.posts)
        setLoaded(true)
      })
      .catch(() => setLoaded(true))
  }, [])

  return (
    <div className="page home">
      {/* Masthead — editorial, not a marketing hero */}
      <section className="masthead">
        <div className="masthead-copy">
          <p className="kicker">MyStudy Academic Suite — JAMB · WAEC · NECO</p>
          <h1>Focus. Practice. Graduate stronger.</h1>
          <p className="lede">
            Past questions, keypoints and vocabulary for Nigerian students preparing for
            JAMB/UTME, WAEC and NECO — plus the calculators, planners and writing tools
            that carry you through the term.
          </p>
          <p className="masthead-actions">
            <Link className="btn-primary" to="/tools">
              Start a CBT mock <IconArrowRight size={16} />
            </Link>
            <Link className="btn-ghost" to="/keypoints">
              Browse keypoints
            </Link>
          </p>
          <p className="fineprint">
            Free to use. Premium is ₦2,000 once and unlocks the full CBT — 180 questions
            per JAMB mock instead of 5 per subject. Paid securely in the app; no bank
            transfer, no WhatsApp receipt.
          </p>
        </div>
        <div className="masthead-art" aria-hidden="true">
          <HeroArt />
        </div>
      </section>

      {/* The bank, in numbers — counted from the repos, not claimed */}
      <section className="bank-strip" aria-label="What is in the bank">
        <div className="bank-stat">
          <strong>{fmt(EXAM_QUESTIONS.total)}</strong>
          <span>past questions in the bank</span>
          <small>JAMB {fmt(EXAM_QUESTIONS.jamb)} · WAEC {fmt(EXAM_QUESTIONS.waec)} · NECO {fmt(EXAM_QUESTIONS.neco)} · Primary {fmt(EXAM_QUESTIONS.primary)}</small>
        </div>
        <div className="bank-stat">
          <strong>{fmt(PRACTICE_QUESTIONS.total)}</strong>
          <span>syllabus-modelled practice questions</span>
          <small>For the 2020–2023 papers the bank does not hold — labelled practice, never passed off as official papers</small>
        </div>
        <div className="bank-stat">
          <strong>{fmt(KEYPOINTS.quiz)}</strong>
          <span>keypoint quiz questions</span>
          <small>{fmt(KEYPOINTS.chapters)} chapters · {fmt(KEYPOINTS.modules)} study modules · 50 questions per chapter</small>
        </div>
        <div className="bank-stat">
          <strong>{fmt(VOCABULARY.words)}</strong>
          <span>vocabulary words</span>
          <small>{VOCABULARY.categories} categories · {fmt(VOCABULARY.quiz)} quiz questions</small>
        </div>
      </section>

      {/* CBT, stated plainly */}
      <section className="cbt-band">
        <div>
          <p className="kicker">Computer-based test</p>
          <h2>Mock the real exam, under real exam rules</h2>
          <p>
            A JAMB mock is 180 questions in 2 hours — English compulsory (60 questions)
            plus three other subjects (40 each) — timed by the server, not by your
            browser clock. Answers and explanations appear only after you submit, and
            corrections open in review mode, the way the v1 CBT worked.
          </p>
          <ul className="tick-list">
            <li><IconCheck size={16} /> English is compulsory, as in the real UTME</li>
            <li><IconCheck size={16} /> One active session per student; tab-switching is counted</li>
            <li><IconCheck size={16} /> Free: 5 questions per subject. Premium: the full paper</li>
          </ul>
        </div>
        <aside className="cbt-facts">
          <p><IconClock size={18} /> <strong>2 hours</strong><span>per JAMB mock</span></p>
          <p><IconClipboardCheck size={18} /> <strong>180 questions</strong><span>60 English + 3 × 40</span></p>
          <p><IconCap size={18} /> <strong>400 marks</strong><span>1 mark per correct answer</span></p>
          <p className="cbt-note">WAEC and NECO mocks follow their own paper patterns. Post-UTME and Primary are in the bank too.</p>
        </aside>
      </section>

      {/* Subjects — the real 21, with real counts */}
      <section>
        <div className="section-head">
          <div>
            <p className="kicker">Past questions by subject</p>
            <h2>Twenty-one subjects, JAMB, WAEC and NECO</h2>
          </div>
          <p className="section-note">
            Counts are the real imported questions (2021–2025 JAMB, 2024–2025 WAEC/NECO,
            2026 Primary). {fmt(EXAM_QUESTIONS.withExplanations)} of them carry an explanation.
          </p>
        </div>
        <ul className="subject-index">
          {EXAM_SUBJECTS.map((s) => (
            <li key={s.slug}>
              <Link to="/keypoints">
                <span>{s.name}</span>
                <strong>{fmt(s.questions)} questions</strong>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* Keypoints + vocabulary, side by side, dense */}
      <section className="duo">
        <div>
          <p className="kicker">Learn Hub — keypoints</p>
          <h2>Short notes that follow the syllabus</h2>
          <p>
            {KEYPOINTS.chapters} chapters across {KEYPOINTS.subjects.length} subjects,
            SSS 1–3 — each chapter with its study modules and 50 quiz questions.
            New this term: CRS, IRS, Civic Education, History, Computer Studies,
            Further Mathematics, Hausa, Igbo and Yoruba.
          </p>
          <p className="subject-cloud">
            {KEYPOINTS.subjects.map((s) => (
              <Link key={s.slug} to="/keypoints">{s.name} <span>({s.chapters})</span></Link>
            ))}
          </p>
          <Link className="text-link" to="/keypoints">Open Learn Hub <IconArrowRight size={15} /></Link>
        </div>
        <div>
          <p className="kicker">Vocabulary</p>
          <h2>Words JAMB actually tests</h2>
          <p>
            {VOCABULARY.categories} categories — one-word substitutions, phobias,
            idioms, proverbs, medical terms, and a full subject set (Mathematics,
            Physics, Chemistry, Biology, Economics, Government, Geography and more),
            plus Hausa, Igbo and Yoruba word lists.
          </p>
          <p className="subject-cloud">
            {VOCABULARY.list.slice(0, 18).map((c) => (
              <Link key={c.slug} to="/vocabulary">{c.name}</Link>
            ))}
            <span className="more">+ {VOCABULARY.list.length - 18} more categories</span>
          </p>
          <Link className="text-link" to="/vocabulary">Open Vocabulary <IconArrowRight size={15} /></Link>
        </div>
      </section>

      {/* Tools — grouped, varied, honest about what each one does */}
      <section>
        <div className="section-head">
          <div>
            <p className="kicker">All tools</p>
            <h2>{TOOLS.length} tools, rebuilt for v2</h2>
          </div>
          <p className="section-note">
            Every tool from v1, rebuilt server-side where it matters — your work is
            saved to your account now, not to one browser.
          </p>
        </div>
        {TOOL_GROUPS.map((g) => (
          <div className="tool-group" key={g.heading}>
            <h3>{g.heading}</h3>
            <p className="group-note">{g.note}</p>
            <div className="tool-rows">
              {g.items.map((t) => (
                <Link className="tool-row" key={t.title} to={t.to}>
                  <span className="tool-icon">{t.icon}</span>
                  <span>
                    <strong>{t.title}</strong>
                    <small>{t.desc}</small>
                  </span>
                  <IconArrowRight size={16} className="tool-arrow" />
                </Link>
              ))}
            </div>
          </div>
        ))}
        <p><Link className="btn-ghost" to="/tools"><IconWrench size={16} /> See all tools</Link></p>
      </section>

      {/* News — real posts only; a small note when empty */}
      <section>
        <div className="section-head">
          <div>
            <p className="kicker">News</p>
            <h2>Latest from MyStudy</h2>
          </div>
          <Link className="text-link" to="/news">All news <IconArrowRight size={15} /></Link>
        </div>
        {!loaded && <p>Loading news…</p>}
        {loaded && posts.length === 0 && (
          <p className="fineprint">No news posts yet — the first update from the admin team will appear here.</p>
        )}
        <div className="news-list-home">
          {posts.map((p) => (
            <article className="news-item" key={p.slug}>
              {p.category && <span className="eyebrow">{p.category}</span>}
              <h3><Link to={`/news/${p.slug}`}>{p.title}</Link></h3>
              {p.excerpt && <p>{p.excerpt}</p>}
              {p.published_at && (
                <time>{new Date(p.published_at).toLocaleDateString('en-NG', { day: 'numeric', month: 'long', year: 'numeric' })}</time>
              )}
            </article>
          ))}
        </div>
      </section>

      {/* Contact — the real v1 contact details */}
      <section className="contact-band">
        <div>
          <h2>Questions, or a correction to a question?</h2>
          <p>
            Past questions and answers are checked against the syllabus and the real
            papers. If you spot a wrong answer or a missing topic, tell us — corrections
            go into the bank, they are not left standing.
          </p>
        </div>
        <p className="contact-lines">
          <a href="mailto:mystudyacademicsuite@gmail.com">mystudyacademicsuite@gmail.com</a>
          <a href="https://wa.me/2348100259673" target="_blank" rel="noreferrer">WhatsApp +234 810 025 9673</a>
        </p>
      </section>
    </div>
  )
}
