import { Link, Route, Routes } from 'react-router-dom'
import AdminEditor from './pages/AdminEditor'
import AdminPosts from './pages/AdminPosts'
import Home from './pages/Home'
import Keypoints from './pages/Keypoints'
import Login from './pages/Login'
import NewsList from './pages/NewsList'
import PostPage from './pages/PostPage'
import Profile from './pages/Profile'
import Register from './pages/Register'
import Tools from './pages/Tools'
import Vocabulary from './pages/Vocabulary'

export default function App() {
  return (
    <div>
      <header className="topbar">
        <Link className="brand" to="/">MyStudy</Link>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/news">News</Link>
          <Link to="/tools">All tools</Link>
          <Link to="/keypoints">Keypoints</Link>
          <Link to="/vocabulary">Vocabulary</Link>
          <Link to="/profile">Profile</Link>
          <Link to="/admin/posts">Admin posts</Link>
          <Link to="/login">Sign in</Link>
          <Link to="/register">Register</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/news" element={<NewsList />} />
        <Route path="/news/:slug" element={<PostPage />} />
        <Route path="/tools" element={<Tools />} />
        <Route path="/keypoints" element={<Keypoints />} />
        <Route path="/vocabulary" element={<Vocabulary />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin/posts" element={<AdminPosts />} />
        <Route path="/admin/posts/new" element={<AdminEditor />} />
        <Route path="/admin/posts/:slug/edit" element={<AdminEditor />} />
        <Route path="/admin/news" element={<AdminPosts />} />
        <Route
          path="*"
          element={
            <div className="page">
              <h1>Page not found</h1>
              <p>This page does not exist. <Link to="/">Back to MyStudy</Link></p>
            </div>
          }
        />
      </Routes>
      <footer className="footer">
        <div className="page footer-inner">
          <div>
            <p className="footer-brand">MyStudy Academic Suite</p>
            <p>
              JAMB, WAEC and NECO preparation for Nigerian students — past questions,
              keypoints, vocabulary and the tools that carry you through the term.
            </p>
          </div>
          <div>
            <p className="footer-head">Prepare</p>
            <p>
              <Link to="/tools">CBT Practice</Link><br />
              <Link to="/keypoints">Keypoints</Link><br />
              <Link to="/vocabulary">Vocabulary</Link><br />
              <Link to="/news">News</Link>
            </p>
          </div>
          <div>
            <p className="footer-head">Contact</p>
            <p>
              <a href="mailto:mystudyacademicsuite@gmail.com">mystudyacademicsuite@gmail.com</a><br />
              <a href="https://wa.me/2348100259673" target="_blank" rel="noreferrer">WhatsApp +234 810 025 9673</a>
            </p>
          </div>
          <p className="footer-note">
            MyStudy v2 is in staging. The Blogger site at mystudy.name.ng stays live until
            staging is walked through and approved.
          </p>
        </div>
      </footer>
    </div>
  )
}
