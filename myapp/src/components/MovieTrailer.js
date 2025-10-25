import React from 'react';
import PropTypes from 'prop-types';
import './MovieTrailer.css';

const getEmbedUrl = (url) => {
  if (!url) {
    return null;
  }

  try {
    const parsed = new URL(url);
    const host = parsed.hostname.toLowerCase();

    if (host.includes('youtube.com')) {
      const videoId = parsed.searchParams.get('v');
      if (videoId) {
        return `https://www.youtube-nocookie.com/embed/${videoId}`;
      }

      const match = parsed.pathname.match(/\/embed\/([A-Za-z0-9_-]+)/);
      if (match && match[1]) {
        return `https://www.youtube-nocookie.com/embed/${match[1]}`;
      }
    }

    if (host.includes('youtu.be')) {
      const videoId = parsed.pathname.replace('/', '');
      return videoId ? `https://www.youtube-nocookie.com/embed/${videoId}` : null;
    }

    if (host.includes('imdb.com')) {
      const match = parsed.pathname.match(/\/video\/(?:imdb\/)?(vi[0-9]+)/);
      if (match && match[1]) {
        return `https://www.imdb.com/video/imdb/${match[1]}/imdb/embed?autoplay=false&width=854`;
      }
    }

    return null;
  } catch (err) {
    return null;
  }
};

const MovieTrailer = ({ trailerUrl }) => {
  const embedUrl = getEmbedUrl(trailerUrl);

  if (!trailerUrl) {
    return null;
  }

  return (
    <section className="movie-trailer" aria-labelledby="movie-trailer-title">
      <div className="movie-trailer__header">
        <h2 id="movie-trailer-title">Trailer</h2>
        {trailerUrl ? (
          <a
            className="movie-trailer__link"
            href={trailerUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            Watch on original site
          </a>
        ) : null}
      </div>

      {embedUrl ? (
        <div className="movie-trailer__frame" role="presentation">
          <iframe
            src={embedUrl}
            title="Movie trailer"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            loading="lazy"
          />
        </div>
      ) : (
        <div className="movie-trailer__placeholder">
          <p>Preview unavailable. You can watch the trailer via the link above.</p>
        </div>
      )}
    </section>
  );
};

MovieTrailer.propTypes = {
  trailerUrl: PropTypes.string,
};

export default MovieTrailer;
