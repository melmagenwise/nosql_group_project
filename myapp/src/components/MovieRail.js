import React from 'react';
import './MovieRail.css';

const MovieRail = ({ movies, selectedId, onSelect }) => {
  return (
    <section className="movie-rail" aria-label="Browse titles">
      <div className="movie-rail__header">
        <h2>Discover More</h2>
        <p>Pick another title to explore its world.</p>
      </div>

      <div className="movie-rail__scroller">
        {movies.map((movie) => {
          const isActive = selectedId === movie._id;
          return (
            <button
              key={movie._id}
              type="button"
              onClick={() => onSelect(movie)}
              className={`movie-rail__item${isActive ? ' movie-rail__item--active' : ''}`}
            >
              <div className="movie-rail__thumb">
                <img
                  src={movie.poster_url}
                  alt={`${movie.title} poster`}
                  loading="lazy"
                />
              </div>
              <div className="movie-rail__info">
                <span className="movie-rail__title">{movie.title}</span>
                <span className="movie-rail__meta">
                  {(movie.year && String(movie.year)) || 'N/A'} |{' '}
                  {movie.imdb_type || 'Unknown'}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </section>
  );
};

export default MovieRail;
