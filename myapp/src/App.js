import { useEffect, useMemo, useState } from 'react';
import Navbar from './components/Navbar';
import MovieDetail from './components/MovieDetail';
import MovieRail from './components/MovieRail';
import MoviePeople from './components/MoviePeople';
import './App.css';

const apiBaseFromEnv = process.env.REACT_APP_API_BASE_URL;
const API_BASE_URL = apiBaseFromEnv
  ? apiBaseFromEnv.replace(/\/+$/, '')
  : '';

const curatedSelection = (movies) => {
  const filtered = movies.filter(
    (movie) => movie?.title && movie?.poster_url && movie?.description,
  );

  return filtered
    .sort((a, b) => {
      const ratingA = Number.isFinite(Number(a.rating)) ? Number(a.rating) : 0;
      const ratingB = Number.isFinite(Number(b.rating)) ? Number(b.rating) : 0;
      return ratingB - ratingA;
    })
    .slice(0, 18);
};

function App() {
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();

    const loadMovies = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const requestUrl = API_BASE_URL
          ? `${API_BASE_URL}/movies-series`
          : '/movies-series';
        const response = await fetch(requestUrl, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error('Unable to load movie data');
        }

        const payload = await response.json();
        const selection = curatedSelection(payload);

        setMovies(selection);
        setSelectedMovie(selection[0] ?? null);
      } catch (err) {
        if (err.name !== 'AbortError') {
          const message =
            err.message || 'Unknown error loading movies from the API';
          const hint = API_BASE_URL
            ? `Please verify the service at ${API_BASE_URL}/movies-series is reachable.`
            : 'Please verify the service is reachable through the development proxy (port 5000).';
          setError(`${message}. ${hint}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadMovies();

    return () => controller.abort();
  }, []);

  const heroMovie = useMemo(() => {
    if (selectedMovie) {
      return selectedMovie;
    }

    return movies[0] ?? null;
  }, [movies, selectedMovie]);

  return (
    <div className="app-shell">
      <Navbar />
      <main className="app-content">
        {error ? (
          <div className="status status--error" role="alert">
            <h1>We hit a snag.</h1>
            <p>{error}</p>
          </div>
        ) : null}

        {!error && isLoading ? (
          <div className="status status--loading" role="status">
            <div className="spinner" aria-hidden />
            <p>Loading the cinematic universe...</p>
          </div>
        ) : null}

        {!error && !isLoading ? (
          <>
            <MovieDetail movie={heroMovie} />
            <MoviePeople movie={heroMovie} />
            <MovieRail
              movies={movies}
              selectedId={heroMovie?._id}
              onSelect={(movie) => setSelectedMovie(movie)}
            />
          </>
        ) : null}
      </main>
    </div>
  );
}

export default App;
