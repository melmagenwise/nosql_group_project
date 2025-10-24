const { createProxyMiddleware } = require('http-proxy-middleware');

const MOVIES_API_TARGET =
  process.env.MOVIES_API_TARGET ||
  process.env.REACT_APP_API_BASE_URL ||
  'http://localhost:5000';

const PEOPLE_API_TARGET =
  process.env.PEOPLE_API_TARGET ||
  process.env.REACT_APP_PEOPLE_API_BASE_URL ||
  'http://localhost:5002';

module.exports = function setupProxy(app) {
  app.use(
    ['/api/movies-series', '/api/movies', '/api/series'],
    createProxyMiddleware({
      target: MOVIES_API_TARGET,
      changeOrigin: true,
      secure: false,
      ws: false,
      logLevel: 'warn',
      pathRewrite: {
        '^/api': '',
      },
    }),
  );

  app.use(
    ['/api/people'],
    createProxyMiddleware({
      target: PEOPLE_API_TARGET,
      changeOrigin: true,
      secure: false,
      ws: false,
      logLevel: 'warn',
      pathRewrite: {
        '^/api': '',
      },
    }),
  );
};
