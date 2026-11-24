import { Link, Route, Routes } from 'react-router-dom'
import AdminEditor from './pages/AdminEditor'
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
          <Link to="/admin/news">Admin editor</Link>
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
        <Route path="/admin/news" element={<AdminEditor />} />
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
        MyStudy Academic Suite v2 (Phase 1 scaffold) — Blogger v1 stays live until staging is approved.
      </footer>
    </div>
  )
}
