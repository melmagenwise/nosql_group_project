import React from 'react';
import PropTypes from 'prop-types';
import './PersonDetail.css';

const FALLBACK_PHOTO =
  'https://ui-avatars.com/api/?name=MM&background=023047&color=ffffff&size=512&length=2';

const PersonDetail = ({ person }) => {
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

        {Array.isArray(knownFor) && knownFor.length > 0 ? (
          <div className="person-detail__known-for">
            <h2>Known For</h2>
            <ul>
              {knownFor.map((entry) => (
                <li key={entry._id || entry.title}>{entry.title}</li>
              ))}
            </ul>
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
};

export default PersonDetail;
