import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './PersonDetail.css';

const FALLBACK_PHOTO =
  'https://ui-avatars.com/api/?name=MM&background=023047&color=ffffff&size=512&length=2';

const FALLBACK_POSTER =
  'https://via.placeholder.com/200x300.png?text=No+Poster';

const PersonDetail = ({ person, knownForDetails = [] }) => {
  if (!person) {
    return null;
  }

  const {
    name,
    photo_url: photoUrl,
    biography,
    role,
    movie: knownFor,
    url: externalUrl,
  } = person;

  const knownForMap = new Map(
    (knownForDetails || [])
      .filter((entry) => entry && entry._id)
      .map((entry) => [entry._id, entry]),
  );

  const displayKnownFor = Array.isArray(knownFor)
    ? knownFor.map((entry) => {
        if (entry?._id && knownForMap.has(entry._id)) {
          return knownForMap.get(entry._id);
        }
        return entry;
      })
    : knownForDetails || [];

  return (
    <section className="person-detail" aria-labelledby="person-detail-title">
      <div className="person-detail__photo">
        <img
          src={photoUrl || FALLBACK_PHOTO}
          alt={`Portrait of ${name}`}
          loading="lazy"
        />
      </div>

      <div className="person-detail__body">
        <div className="person-detail__header">
          <h1 className="person-detail__title" id="person-detail-title">
            {name}
          </h1>
          {externalUrl ? (
            <a
              className="person-detail__external"
              href={externalUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              View on IMDb
            </a>
          ) : null}
        </div>

        {Array.isArray(role) && role.length > 0 ? (
          <div className="person-detail__roles">
            {role.map((entry) => (
              <span key={entry} className="person-detail__badge">
                {entry}
              </span>
            ))}
          </div>
        ) : null}

        {biography ? (
          <p className="person-detail__biography">{biography}</p>
        ) : (
          <p className="person-detail__biography person-detail__biography--muted">
            We don&apos;t have a biography for this person just yet.
          </p>
        )}

        {Array.isArray(displayKnownFor) && displayKnownFor.length > 0 ? (
          <div className="person-detail__known-for">
            <h2>Known For</h2>
            <div className="person-detail__known-for-grid">
              {displayKnownFor.map((entry) => {
                const id = entry?._id || entry?.movie_id;
                const title = entry?.title || 'Untitled';
                const poster = entry?.poster_url || FALLBACK_POSTER;
                const content = (
                  <>
                    <div className="person-detail__known-for-poster">
                      <img src={poster} alt={title} loading="lazy" />
                    </div>
                    <span className="person-detail__known-for-title">
                      {title}
                    </span>
                  </>
                );

                if (id) {
                  return (
                    <Link
                      key={id}
                      to={`/movies-series/${id}`}
                      className="person-detail__known-for-card"
                    >
                      {content}
                    </Link>
                  );
                }

                return (
                  <div
                    key={title}
                    className="person-detail__known-for-card person-detail__known-for-card--disabled"
                  >
                    {content}
                  </div>
                );
              })}
            </div>
          </div>
        ) : null}
      </div>
    </section>
  );
};

PersonDetail.propTypes = {
  person: PropTypes.shape({
    name: PropTypes.string,
    photo_url: PropTypes.string,
    biography: PropTypes.string,
    role: PropTypes.arrayOf(PropTypes.string),
    url: PropTypes.string,
    movie: PropTypes.arrayOf(
      PropTypes.shape({
        _id: PropTypes.string,
        title: PropTypes.string,
      }),
    ),
  }),
  knownForDetails: PropTypes.arrayOf(
    PropTypes.shape({
      _id: PropTypes.string,
      title: PropTypes.string,
      poster_url: PropTypes.string,
    }),
  ),
};

PersonDetail.defaultProps = {
  knownForDetails: [],
};

export default PersonDetail;
