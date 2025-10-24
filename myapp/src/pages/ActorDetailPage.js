import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import PersonDetail from '../components/PersonDetail';
import { buildPeopleUrl } from '../config';

const ActorDetailPage = () => {
  const { actorId } = useParams();
  const [person, setPerson] = useState(null);
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
      <PersonDetail person={person} />
      <div className="actor-detail-page__actions">
        <Link to="/" className="actor-detail-page__back">
          ← Back to home
        </Link>
      </div>
    </div>
  );
};

export default ActorDetailPage;
