import React from 'react';
import './MovieVitals.css';

const MovieVitals = ({ movie }) => {
  if (!movie) {
    return null;
  }

  const { country, languages, genre_interests: genreInterests } = movie;

  const languageList = Array.isArray(languages)
    ? languages.filter(Boolean)
    : [];
  const interestList = Array.isArray(genreInterests)
    ? genreInterests.filter(Boolean)
    : [];
  const countryList = country ? [country] : [];

  if (
    !interestList.length &&
    !languageList.length &&
    !countryList.length
  ) {
    return null;
  }

  return (
    <section className="movie-vitals" aria-label="Additional movie context">
      {interestList.length ? (
        <div className="movie-vitals__chips movie-vitals__chips--inline" role="list">
          {interestList.map((item, index) => (
            <span
              className="movie-vitals__chip movie-vitals__chip--inline"
              role="listitem"
              key={`genre-interests-${item}-${index}`}
            >
              {item}
            </span>
          ))}
        </div>
      ) : null}

      {languageList.length || countryList.length ? (
        <div className="movie-vitals__grid">
          {languageList.length ? (
            <div className="movie-vitals__card">
              <span className="movie-vitals__card-label">Languages</span>
              <div className="movie-vitals__chips" role="list">
                {languageList.map((item, index) => (
                  <span
                    className="movie-vitals__chip"
                    role="listitem"
                    key={`languages-${item}-${index}`}
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ) : null}

          {countryList.length ? (
            <div className="movie-vitals__card">
              <span className="movie-vitals__card-label">Country</span>
              <div className="movie-vitals__chips" role="list">
                {countryList.map((item, index) => (
                  <span
                    className="movie-vitals__chip"
                    role="listitem"
                    key={`country-${item}-${index}`}
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </section>
  );
};

export default MovieVitals;
