# Docker Setup

## Run with Docker Compose

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:5000
```

The first registered user becomes an admin account when the database is empty.

## Environment

Set a real secret key before deployment:

```bash
set SECRET_KEY=replace-with-a-long-random-secret
docker compose up --build
```

On macOS/Linux:

```bash
SECRET_KEY=replace-with-a-long-random-secret docker compose up --build
```

## Persistent Data

`docker-compose.yml` stores SQLite data in the `cancer-risk-data` Docker volume:

```text
/app/data/users.db
```

To reset users and reports:

```bash
docker compose down -v
```

## Manual Docker Commands

Build:

```bash
docker build -t cancer-risk-app .
```

Run:

```bash
docker run --rm -p 5000:5000 -e SECRET_KEY=replace-with-a-long-random-secret -v cancer-risk-data:/app/data cancer-risk-app
```
