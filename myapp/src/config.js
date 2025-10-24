const stripTrailingSlash = (value) => value.replace(/\/+$/, '');

const MOVIES_API_ENV = process.env.REACT_APP_API_BASE_URL || '';
const PEOPLE_API_ENV = process.env.REACT_APP_PEOPLE_API_BASE_URL || '';

export const MOVIES_API_BASE = MOVIES_API_ENV
  ? stripTrailingSlash(MOVIES_API_ENV)
  : '';

export const PEOPLE_API_BASE = PEOPLE_API_ENV
  ? stripTrailingSlash(PEOPLE_API_ENV)
  : '';

export const buildMoviesUrl = (path) =>
  MOVIES_API_BASE ? `${MOVIES_API_BASE}${path}` : path;

export const buildPeopleUrl = (path) =>
  PEOPLE_API_BASE ? `${PEOPLE_API_BASE}${path}` : path;
