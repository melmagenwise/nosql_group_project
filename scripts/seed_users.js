// docker/scripts/seed.js
const fs = require('fs');

db = db.getSiblingDB('api_users');

if (db.users.countDocuments() === 0) {
  const filePath = '/docker-entrypoint-initdb.d/users_data.json';
  const payload = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  let users = [];
  if (Array.isArray(payload)) {
    users = payload;
  } else if (payload && Array.isArray(payload.users)) {
    users = payload.users;
  } else if (payload && Object.keys(payload).length > 0) {
    users = [payload];
  }

  if (users.length > 0) {
    db.users.insertMany(users);
    print(`Inserted ${users.length} user documents.`);
  } else {
    print('Users dataset is empty or not an array. No documents inserted.');
  }
} else {
  print('users collection already populated. Skipping seed.');
}
