import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ActorDetailPage from './pages/ActorDetailPage';
import './App.css';

const NotFound = () => (
  <div className="status status--error" role="alert">
    <h1>Page not found.</h1>
    <p>The page you are trying to reach does not exist.</p>
    <Link className="status__link" to="/">
      Back to home
    </Link>
  </div>
);

function App() {
  return (
    <Router>
      <div className="app-shell">
        <Navbar />
        <main className="app-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/actors/:actorId" element={<ActorDetailPage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
