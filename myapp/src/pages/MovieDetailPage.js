import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import MovieDetail from '../components/MovieDetail';
import MoviePeople from '../components/MoviePeople';
import MovieRail from '../components/MovieRail';
import { buildMoviesUrl } from '../config';

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

const MovieDetailPage = () => {
  const { movieId } = useParams();
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();

    const loadMovies = async () => {
      const endpoint = buildMoviesUrl('/movies-series');

      try {
        setIsLoading(true);
        setError(null);
        const response = await fetch(endpoint, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error('Unable to load movie data');
        }

        const payload = await response.json();
        const selection = curatedSelection(payload);

        setMovies(selection);
        if (movieId) {
          const match = selection.find((entry) => entry._id === movieId);
          setSelectedMovie(match ?? selection[0] ?? null);
        } else {
          setSelectedMovie(selection[0] ?? null);
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          const baseMessage =
            err.message || 'Unknown error loading movies from the API';
          const hint = endpoint.startsWith('http')
            ? `Please verify the service at ${endpoint} is reachable.`
            : 'Please verify the service is reachable through the development proxy (port 5000).';
          setError(`${baseMessage}. ${hint}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadMovies();

    return () => controller.abort();
  }, [movieId]);

  const heroMovie = useMemo(() => {
    if (selectedMovie) {
      return selectedMovie;
    }

    return movies.find((entry) => entry._id === movieId) ?? movies[0] ?? null;
  }, [movies, selectedMovie, movieId]);

  if (error) {
    return (
      <div className="status status--error" role="alert">
        <h1>We hit a snag.</h1>
        <p>{error}</p>
        <Link className="status__link" to="/">
          Back to home
        </Link>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="status status--loading" role="status">
        <div className="spinner" aria-hidden />
        <p>Loading the cinematic universe...</p>
      </div>
    );
  }

  return (
    <div className="movie-detail-page">
      <MovieDetail movie={heroMovie} />
      <MoviePeople movie={heroMovie} />
      <MovieRail
        movies={movies}
        selectedId={heroMovie?._id}
        onSelect={(movie) => setSelectedMovie(movie)}
      />
    </div>
  );
};

export default MovieDetailPage;
