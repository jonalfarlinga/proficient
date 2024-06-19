import './styles/App.css';
import { HashRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import Profile from './components/Profile.jsx';
import LandingPage from './components/LandingPage.jsx';
import { useLazyGetTokenQuery } from './api/profApi.js';
import { useDispatch } from 'react-redux';
import { useEffect } from 'react';
import { useAuthToken } from './features/tokenSelector.js';
import { setToken } from './features/authTokenSlice.js';


function App() {
    const [fetchToken, { data: tokenData, isLoading, isError }] = useLazyGetTokenQuery();
    const token = useAuthToken();
    const dispatch = useDispatch();
    useEffect(() => {
      if (localStorage.getItem('token')) {
        fetchToken();
      }
    }, [fetchToken]);

    useEffect(() => {
      if (tokenData && !isError) {
        dispatch(setToken(tokenData));
      } else if (!isLoading) {
        localStorage.removeItem('token');
      }
    }, [tokenData, isLoading, isError, dispatch]);
    return (
      <HashRouter>
        <div className="app">
          <nav className="navbar nav-pills align-content-start p-3">
            <ul className="nav flex-column">
              <li className="nav-item"><Link className="nav-link" to="/">Landing Page</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/dashboard">Dashboard</Link></li>
              {token &&
               (<li className="nav-item"><Link className="nav-link" to="/profile">Profile</Link></li>)
              }
            </ul>
          </nav>
          <main className="main-content">
            <header className="hero">
            </header>
            <h1>The Proficient Professor</h1>
            <section className="content-panel">
              <Routes>
                <Route path="/" exact element={<LandingPage />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </section>
          </main>
        </div>
      </HashRouter>
    );
  }

  export default App;
