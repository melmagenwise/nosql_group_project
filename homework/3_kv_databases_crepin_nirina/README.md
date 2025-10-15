**TO DO:** CTRL + SHIFT + V 
# Part 2 - Exercise 4

In this exercise, a RESTful API for a video game store and a client database was created using Python, the Flask web framework, and MongoDB. The API allows basic CRUD (Create, Read, Update, Delete) operations. Docker Compose is used to run the Flask APIs and MongoDB together. Redis was added as a cache layer. 

## Table of Content
- [Repository structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [API usage](#api-usage)
- [Other references](#other-references)
- [Author](#author)
- [Redis caching](#redis-caching)
- [Testing cache](#testing-cache)

## Repository structure

```python
3_kv_databases_crepin_nirina/
│
├── api_games/                        # Folder for the Games API
│   ├── games.py                      # Defines the Game model (attributes of a video game)
│   ├── games_collection.py           # Flask routes for CRUD operations on games
│   ├── DatabaseManagerGames.py       # MongoDB connection and database logic for games
│   ├── cache.py                      # Implement correct cache invalidation
│   ├── Dockerfile                    # Docker image definition for the Games API
│   └── requirements.txt              # Python dependencies for the Games API
│
├── api_clients/                      # Folder for the Clients API
│   ├── clients.py                    # Defines the Client model (attributes of a client)
│   ├── clients_collection.py         # Flask routes for CRUD operations on clients
│   ├── DatabaseManagerClients.py     # MongoDB connection and database logic for clients
│   ├── cache.py                      # Implement correct cache invalidation
│   ├── Dockerfile                    # Docker image definition for the Clients API
│   └── requirements.txt              # Python dependencies for the Clients API
│
├── redis_data/                       # Redis data
├── redisinsight_data/                # RedisInsight data
│
├── .dockerignore                     # Files and folders ignored by Docker during build
├── docker-compose.yml                # Multi-container configuration (APIs + MongoDB)
└── README.md                         # Project documentation and usage instructions
```


## Prerequisites
- Python 3.10+
- Flask
- PyMongo
- Docker and Docker Compose
- PowerShell (Windows) or curl (Linux/Mac)
- MongoDB Compass
- redis

## Getting started

### Create and activate virtual environment
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Install dependencies

```bash
pip install flask pymongo
```

### Run locally

For games API:

```bash
python api_games/games_collection.py
```

For clients API:

```bash
python api_clients/clients_collection.py
```

### Run with Docker Compose

```bash
. cd 3_kv_databases_crepin_nirina

docker-compose up --build
```

## MongoDB Compass

**URI CONNECTION**
```txt
mongodb://localhost:27017
```

## API usage

**Flask API GAMES**

http://127.0.0.1:5000/games

**Flask API CLIENTS**

http://127.0.0.1:5001/clients

---
## Redis caching
**Cached endpoints**
- Games: `GET /games` (key: `games:list:page=..:per=..[:genre=..][:platform=..][:year=..]`)
- Games: `GET /games/{id}` (key: `game:{id}`)
- Clients: `GET /clients` (key: `clients:list:page=..:per=..[:city=..][:genre=..]`)
- Clients: `GET /clients/{id}` (key: `client:{id}`)

**TTL**
- JSON responses are cached with a TTL (`CACHE_TTL_SECONDS`, default 120s).

**Invalidation on writes**
- After POST/PUT/DELETE:
  - delete `game:{id}` or `client:{id}`
  - delete list/search prefixes: `games:list:*`, `clients:list:*`, `search:*`

**Ping**
- `GET /__ping/redis` returns the Redis connectivity status.

**Example**

Games – list (filters)
- Request: `GET /games?page=2&per=20&genre=Sport`
- Cache key: `games:list:page=2:per=20:genre=Sport`
- Run:
  - PowerShell: `irm "http://localhost:5000/games?page=2&per=20&genre=Sport"`

Games – single
- Request: `GET /games/1`
- Cache key: `game:1`
- Run:
  - PowerShell: `irm http://localhost:5000/games/1`

Clients – list (filters)
- Request: `GET /clients?page=1&per=10&city=Brussels`
- Cache key: `clients:list:page=1:per=10:city=Brussels`
- Run:
  - PowerShell: `irm "http://localhost:5001/clients?page=1&per=10&city=Brussels"`

Search (hash key)
- Request (games): `GET /games?q=fifa+ps5&page=1`
- Cache key: `search:{sha1(sorted_query_params)}`
- Run:
  - PowerShell: `irm "http://localhost:5000/games?q=fifa+ps5&page=1"`

Ping
- Request: `GET /__ping/redis`
- Run:
  - PowerShell: `irm "http://localhost:5001/__ping/redis"`
  - PowerShell: `irm "http://localhost:5000/__ping/redis"`
---
### Games API (port 5000)
---
**GET all games**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/games -Method GET
```

**GET one game by ID**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/games/1 -Method GET
```

**POST create a new game**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/games -Method POST -Body '{
  "title": "FIFA 25",
  "year": 2025,
  "genre": "Sport",
  "platform": "PS5",
  "price": 70,
  "quantity": 5
}' -ContentType "application/json"
```

**PUT update a game**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/games/1 -Method PUT -Body '{
  "price": 80,
  "quantity": 10
}' -ContentType "application/json"
```

**DELETE a game**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/games/1 -Method DELETE
```

---
### Clients API (port 5001)
---
**GET all clients**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5001/clients -Method GET
```

**GET one client by ID**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5001/clients/1 -Method GET
```

**POST create a new client**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5001/clients -Method POST -Body '{
  "name": "Nirina Crepin",
  "birthday": "29/10/2001",
  "email": "nicrepin@ecam.be",
  "phone": "02562358455",
  "city": "Bousval",
  "genre": "Woman"
}' -ContentType "application/json"
```

**PUT update a client**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5001/clients/1 -Method PUT -Body '{
  "city": "Brussels"
}' -ContentType "application/json"
```

**DELETE a client**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5001/clients/1 -Method DELETE
```

---
## Testing cache
---
### Latency (miss vs hit)
```powershell
# MISS then HIT (games list)
Measure-Command { irm "http://localhost:5000/games?page=1&per=5" | Out-Null }
Measure-Command { irm "http://localhost:5000/games?page=1&per=5" | Out-Null }

# MISS then HIT (game by id)
Measure-Command { irm "http://localhost:5000/games/1" | Out-Null }
Measure-Command { irm "http://localhost:5000/games/1" | Out-Null }

# Clients
Measure-Command { irm "http://localhost:5001/clients?page=1&per=5&city=Bousval" | Out-Null }
Measure-Command { irm "http://localhost:5001/clients?page=1&per=5&city=Bousval" | Out-Null }

```
### Invalidation
```powershell
# GET
irm "http://localhost:5000/games/1" | Out-Null
irm "http://localhost:5000/games?page=1&per=5&genre=Sport" | Out-Null

# PUT -> invalidate resource + lists
$body = @{ title="FIFA 25"; year=2025; genre="Sport"; platform="PS5"; price=70; quantity=5 } | ConvertTo-Json
irm -Method PUT -Body $body -ContentType "application/json" http://localhost:5000/games/1

# Read back
irm http://localhost:5000/games/1
irm "http://localhost:5000/games?page=1&per=5&genre=Sport" | ConvertTo-Json -Depth 6
```
---
### Redis ping
---
```powershell
irm http://localhost:5000/__ping/redis
irm http://localhost:5001/__ping/redis
```

---
## Other references
- https://github.com/ProfeserCode/PythonMongoDB.git
- https://www.youtube.com/playlist?list=PL4cUxeGkcC9hxjeEtdHFNYMtCpjNBm3h7
- https://www.youtube.com/watch?v=gFjpv-nZO0U
- https://plainenglish.io/blog/creating-a-simple-task-crud-app-with-fastapi-postgresql-sqlalchemy-and-docker
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.5
- https://hyperskill.org/blog/post/building-and-deploying-a-flask-to-do-app-with-docker-mongodb-and-redis
- https://redis.io/docs/latest/develop/clients/redis-vl/
- https://github.com/monetree/redis-flask-mongo
- https://aws.plainenglish.io/redis-mongodb-caching-with-redis-72dd92be9a1a?gi=8ab2c6710449
- https://ankush-chavan.medium.com/creating-flask-application-with-mongodb-database-77ec45b5b995
- https://testdriven.io/blog/flask-server-side-sessions/

## Author
Nirina Crépin
