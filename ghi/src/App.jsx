import './styles/App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import Profile from './components/Profile.jsx';
import LandingPage from './components/LandingPage.jsx';

function App() {
    return (
      <BrowserRouter>
        <div className="app">
          <nav className="nav-bar">
            <ul>
              <li><Link to="/">Landing Page</Link></li>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/profile">Profile</Link></li>
            </ul>
          </nav>
          <main className="main-content">
            <header className="hero">
              <h1>Hero Section</h1>
            </header>
            <section className="content-panel">
              <Routes>
                <Route path="/" exact element={<LandingPage />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </section>
          </main>
        </div>
      </BrowserRouter>
    );
  }

  export default App;
