# Social Media Backend API

A RESTful backend for a social media platform, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**, and secured with **JWT authentication**.

Users can register, log in, create and manage posts, and vote on posts. The database schema is versioned with Alembic migrations.

## Overview

This project is a backend-only application that exposes a REST API for a social media platform. It demonstrates:

* Designing a relational database with PostgreSQL and SQLAlchemy ORM
* Implementing stateless authentication with JWT
* Enforcing authorization so users can only modify their own data
* Managing schema changes safely with Alembic
* Validating requests and responses with Pydantic

## Features

* User registration and login
* JWT-based authentication with OAuth2 password flow
* Secure password hashing using bcrypt
* Protected routes with ownership checks
* Full CRUD operations on posts
* Post voting (like and unlike)
* Relational schema with foreign keys and constraints
* Versioned database migrations with Alembic
* Request and response validation with Pydantic
* Auto-generated interactive docs (Swagger UI and ReDoc)

## Tech Stack

| Layer | Technology |
| ----- | ---------- |
| Language | Python |
| Framework | FastAPI |
| Server | Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT (python-jose), OAuth2 |
| Password Hashing | Passlib, bcrypt |
| Validation | Pydantic |

## Project Structure

```text
FastApi/
├── app/
│   ├── __init__.py
│   ├── main.py          # Application entry point
│   ├── database.py      # Database engine and session
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── oauth2.py        # JWT creation and verification
│   ├── utils.py         # Password hashing helpers
│   └── routers/
│       ├── __init__.py
│       ├── auth.py      # Login
│       ├── user.py      # User routes
│       ├── post.py      # Post routes
│       └── vote.py      # Vote routes
├── alembic/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Schema

### users

| Column | Type | Notes |
| ------ | ---- | ----- |
| id | Integer | Primary key |
| email | String | Unique, not null |
| password | String | Hashed, not null |
| created_at | Timestamp | Defaults to now |

### posts

| Column | Type | Notes |
| ------ | ---- | ----- |
| id | Integer | Primary key |
| title | String | Not null |
| content | String | Not null |
| published | Boolean | Defaults to true |
| owner_id | Integer | Foreign key to users.id |
| created_at | Timestamp | Defaults to now |

### votes

| Column | Type | Notes |
| ------ | ---- | ----- |
| user_id | Integer | Foreign key to users.id |
| post_id | Integer | Foreign key to posts.id |

The `votes` table uses a composite primary key (`user_id`, `post_id`), so a user can vote on a post only once.

```text
users 1 ──── * posts
users * ──── * posts   (through votes)
```

## API Endpoints

### Authentication and Users

| Method | Endpoint | Description | Auth |
| ------ | -------- | ----------- | ---- |
| `POST` | `/login` | Log in and receive a JWT | No |
| `POST` | `/users` | Register a new user | No |
| `GET` | `/users/{id}` | Get a user by ID | No |

### Posts

| Method | Endpoint | Description | Auth |
| ------ | -------- | ----------- | ---- |
| `GET` | `/posts` | Get all posts | Yes |
| `GET` | `/posts/{id}` | Get a post by ID | Yes |
| `POST` | `/posts` | Create a post | Yes |
| `PUT` | `/posts/{id}` | Update your post | Yes |
| `DELETE` | `/posts/{id}` | Delete your post | Yes |

### Votes

| Method | Endpoint | Description | Auth |
| ------ | -------- | ----------- | ---- |
| `POST` | `/vote` | Add or remove a vote on a post | Yes |

## Quick Start

### Prerequisites

* Python 3.9 or higher
* PostgreSQL
* Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/pritikajha2005/social-media-backend.git
cd social-media-backend
# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE your_database_name;
```

Create a `.env` file (see below), then run the migrations and start the server:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

| Docs | URL |
| ---- | --- |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_postgres_username
DATABASE_PASSWORD=your_postgres_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Never commit your `.env` file. It is excluded through `.gitignore`.

## Usage Examples

### Register a user

`POST /users`

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-10-07T10:30:00"
}
```

### Log in

`POST /login` with form data (`username` is the email, plus `password`).

Response:

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

### Call a protected endpoint

Send the token in the request header:

```text
Authorization: Bearer <jwt_token>
```

### Create a post

`POST /posts`

```json
{
  "title": "My First Post",
  "content": "Hello from my FastAPI backend!"
}
```

### Vote on a post

`POST /vote`

```json
{
  "post_id": 1,
  "dir": 1
}
```

Use `"dir": 1` to like a post and `"dir": 0` to remove the like.

## Security

* Passwords are hashed with bcrypt and never stored in plain text.
* Access tokens are signed JWTs with a configurable expiry time.
* Protected routes verify the token on every request.
* Update and delete operations check that the user owns the post.
* Secrets and database credentials are loaded from environment variables.

## HTTP Status Codes

| Code | Meaning |
| ---- | ------- |
| `200 OK` | Request succeeded |
| `201 Created` | Resource created |
| `204 No Content` | Resource deleted |
| `401 Unauthorized` | Missing or invalid token |
| `403 Forbidden` | Action not permitted for this user |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate vote |
| `422 Unprocessable Entity` | Request validation failed |

## Key Learnings

* Building a structured, modular REST API with FastAPI routers
* Implementing JWT authentication and route protection
* Designing relational schemas and relationships with SQLAlchemy
* Handling schema evolution with Alembic migrations
* Writing request and response models with Pydantic
* Keeping secrets out of source control

## Future Improvements

* Pagination, search, and filtering
* Comments and follow system
* User profile management
* Automated tests with Pytest
* Docker and CI/CD setup
* Cloud deployment

## Author

**Pritika Jha**
B.Tech, Artificial Intelligence and Machine Learning

* GitHub: [pritikajha2005](https://github.com/pritikajha2005)
* LinkedIn: [pritikajha](https://www.linkedin.com/in/pritikajha)