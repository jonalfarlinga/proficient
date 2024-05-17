import './styles/App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import Profile from './components/Profile.jsx';
import LandingPage from './components/LandingPage.jsx';
import { useAuthToken } from './features/tokenSelector.js';


function App() {
    const token = useAuthToken()

    return (
      <BrowserRouter>
        <div className="app">
          <nav className="navbar nav-pills align-content-start p-3">
            <ul className="nav flex-column">
              <li className="nav-item"><Link className="nav-link" to="/">Landing Page</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/dashboard">Dashboard</Link></li>
              {token && (<li className="nav-item"><Link className="nav-link" to="/profile">Profile</Link></li>)}
            </ul>
          </nav>
          <main className="main-content">
            <header className="hero">
              <h1>Title</h1>
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
