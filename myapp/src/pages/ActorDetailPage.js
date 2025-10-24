import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import PersonDetail from '../components/PersonDetail';
import { buildPeopleUrl, buildMoviesUrl } from '../config';

const ActorDetailPage = () => {
  const { actorId } = useParams();
  const [person, setPerson] = useState(null);
  const [knownForDetails, setKnownForDetails] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!actorId) {
      setError('The requested actor identifier is missing.');
      setIsLoading(false);
      return;
    }

    const controller = new AbortController();

    const loadPerson = async () => {
      const endpoint = buildPeopleUrl(`/people/${actorId}`);

      try {
        setIsLoading(true);
        setError(null);

        const response = await fetch(endpoint, {
          signal: controller.signal,
        });

        if (response.status === 404) {
          throw new Error('We could not find that actor in the database.');
        }

        if (!response.ok) {
          throw new Error('Unable to load actor details.');
        }

        const payload = await response.json();
        setPerson(payload);
      } catch (err) {
        if (err.name !== 'AbortError') {
          const baseMessage = err.message || 'Unknown error loading actor';
          const hint = endpoint.startsWith('http')
            ? `Please verify the service at ${endpoint} is reachable.`
            : 'Please verify the people service is reachable through the development proxy (port 5002).';
          setError(`${baseMessage}. ${hint}`);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadPerson();

    return () => controller.abort();
  }, [actorId]);

  useEffect(() => {
    if (!person || !Array.isArray(person.movie) || person.movie.length === 0) {
      setKnownForDetails([]);
      return;
    }

    let cancelled = false;
    const controller = new AbortController();

    const loadKnownFor = async () => {
      try {
        const uniqueMovies = Array.from(
          new Map(
            person.movie
              .filter((entry) => entry?._id)
              .map((entry) => [entry._id, entry]),
          ).values(),
        );

        const results = await Promise.all(
          uniqueMovies.map(async (entry) => {
            const endpoint = buildMoviesUrl(`/movies-series/${entry._id}`);
            try {
              const response = await fetch(endpoint, {
                signal: controller.signal,
              });
              if (!response.ok) {
                return null;
              }
              return await response.json();
            } catch (movieErr) {
              console.warn(movieErr);
              return null;
            }
          }),
        );

        if (!cancelled) {
          setKnownForDetails(results.filter(Boolean));
        }
      } catch (err) {
        if (!cancelled) {
          console.warn('Failed to load known-for titles', err);
          setKnownForDetails([]);
        }
      }
    };

    loadKnownFor();

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [person]);

  if (error) {
    return (
      <div className="status status--error" role="alert">
        <h1>Something went wrong.</h1>
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
        <p>Gathering actor insights...</p>
      </div>
    );
  }

  return (
    <div className="actor-detail-page">
      <PersonDetail person={person} knownForDetails={knownForDetails} />
      <div className="actor-detail-page__actions">
        <Link to="/" className="actor-detail-page__back">
          ← Back to home
        </Link>
      </div>
    </div>
  );
};

export default ActorDetailPage;
