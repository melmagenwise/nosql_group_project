import React from 'react';
import './MovieDetail.css';

const FALLBACK_POSTER =
  'https://via.placeholder.com/400x600.png?text=Poster+Unavailable';

const formatRuntime = (duration) => {
  if (!duration || Number.isNaN(Number(duration))) {
    return null;
  }
  const totalMinutes = Number(duration);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  if (hours === 0) {
    return `${minutes}m`;
  }
  return `${hours}h ${minutes.toString().padStart(2, '0')}m`;
};

const MovieDetail = ({ movie }) => {
  if (!movie) {
    return (
      <section className="movie-detail movie-detail--empty" aria-live="polite">
        <p>Select a title to explore its details.</p>
      </section>
    );
  }

  const {
    title,
    description,
    duration,
    poster_url: posterUrl,
    genres,
    rating,
    year,
    imdb_type: imdbType,
    series_total_seasons: totalSeasons,
    series_total_episodes: totalEpisodes,
  } = movie;

  const runtimeLabel = formatRuntime(duration);
  const typeTitle =
    imdbType === 'TVSeries'
      ? `TV Series${year ? ` - ${year}` : ''}`
      : `Movie${year ? ` - ${year}` : ''}`;

  const extraSeriesInfo =
    imdbType === 'TVSeries'
      ? [
          totalSeasons
            ? `${totalSeasons} season${totalSeasons > 1 ? 's' : ''}`
            : null,
          totalEpisodes
            ? `${totalEpisodes} episode${totalEpisodes > 1 ? 's' : ''}`
            : null,
        ]
          .filter(Boolean)
          .join(' | ')
      : null;

  return (
    <section
      className="movie-detail"
      aria-labelledby="movie-detail-title"
      id="home"
    >
      <div className="movie-detail__poster">
        <img
          src={posterUrl || FALLBACK_POSTER}
          alt={`Poster for ${title}`}
          loading="lazy"
        />
      </div>

      <div className="movie-detail__content">
        <div className="movie-detail__meta">
          <span className="movie-detail__type">{typeTitle}</span>
          {runtimeLabel ? (
            <span className="movie-detail__runtime">{runtimeLabel}</span>
          ) : null}
          {rating ? (
            <span className="movie-detail__score" aria-label="IMDB rating">
              Rating {Number(rating).toFixed(1)}
            </span>
          ) : null}
        </div>

        <h1 className="movie-detail__title" id="movie-detail-title">
          {title}
        </h1>

        {extraSeriesInfo ? (
          <p className="movie-detail__series-info" id="series">
            {extraSeriesInfo}
          </p>
        ) : null}

        <p className="movie-detail__description">{description}</p>

        <div className="movie-detail__genres" id="movies">
          {genres?.map((genre) => (
            <span key={genre} className="movie-detail__badge">
              {genre}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MovieDetail;
