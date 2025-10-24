const stripTrailingSlash = (value) => value.replace(/\/+$/, '');

const MOVIES_API_ENV = process.env.REACT_APP_API_BASE_URL || process.env.MOVIES_API_TARGET || '';
const PEOPLE_API_ENV = process.env.REACT_APP_PEOPLE_API_BASE_URL || process.env.PEOPLE_API_TARGET || '';

export const MOVIES_API_BASE = MOVIES_API_ENV
  ? stripTrailingSlash(MOVIES_API_ENV)
  : '';

export const PEOPLE_API_BASE = PEOPLE_API_ENV
  ? stripTrailingSlash(PEOPLE_API_ENV)
  : '';

export const buildMoviesUrl = (path) =>
  MOVIES_API_BASE ? `${MOVIES_API_BASE}${path}` : `/api${path}`;

export const buildPeopleUrl = (path) =>
  PEOPLE_API_BASE ? `${PEOPLE_API_BASE}${path}` : `/api${path}`;
