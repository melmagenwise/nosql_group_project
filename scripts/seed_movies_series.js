// docker/scripts/seed.js
const fs = require('fs');

db = db.getSiblingDB('api_movies_series');

if (db.movies_series.countDocuments() === 0) {
  const filePath = '/docker-entrypoint-initdb.d/movies_data.json';
  const movies = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

  if (Array.isArray(movies) && movies.length > 0) {
    db.movies_series.insertMany(movies);
    print(`Inserted ${movies.length} movies/series documents.`);
  } else {
    print('Movies dataset is empty or not an array. No documents inserted.');
  }
} else {
  print('movies_series collection already populated. Skipping seed.');
}

