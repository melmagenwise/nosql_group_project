// docker/scripts/seed.js
const fs = require('fs');

db = db.getSiblingDB('api_people');

if (db.people.countDocuments() === 0) {
  const filePath = '/docker-entrypoint-initdb.d/people_data.json';
  const payload = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  let people = [];
  if (Array.isArray(payload)) {
    people = payload;
  } else if (payload && Array.isArray(payload.people)) {
    people = payload.people;
  }

  if (people.length > 0) {
    db.people.insertMany(people);
    print(`Inserted ${people.length} people documents.`);
  } else {
    print('People dataset is empty or not an array. No documents inserted.');
  }
} else {
  print('people collection already populated. Skipping seed.');
}
