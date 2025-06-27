#  MovieVerse Backend API

A Flask REST API backend for the MovieVerse app – a movie discovery and social platform where users can rate, comment on, and favorite movies. The backend uses PostgreSQL, SQLAlchemy, Flask-JWT-Extended, and includes session management and secure authentication.

---

## Features

-  User registration and login (JWT auth)
-  Add/view/delete favorites
-  Rate movies
-  Comment on movies
-  Secure password hashing with bcrypt
-  Full RESTful API with error handling
-  Tested with pytest
-  Ready for deployment (Render/Heroku)

---

## Technologies Used

- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- PostgreSQL
- Bcrypt (for password hashing)
- Pytest (for testing)

---

## 📂 Folder Structure

├── app.py
├── models.py
├── seed.py
├── config.py
├── requirements.txt
├── migrations/
├── movieverse-backend/
│ └── routes/
│ ├── auth_routes.py
│ ├── favorite_routes.py
│ ├── comment_routes.py
│ ├── rating_routes.py
│
├── tests/
│ └── test_auth.py
│ └── conftest.py
│
├── README.md
└── postman_collection.json

# 📬 API Endpoints

| Method | Endpoint      |     Description     |
|--------|---------------|---------------------|
| POST   | `/api/register`  | Register new user       |
| POST   | `/api/login`     | Login and get token     |
| GET    | `/api/favorites` | Get all user favorites  |
| POST   | `/api/favorites` | Add a new favorite      |
| DELETE | `/api/favorites/<id>` | Remove a favorite   |
| POST   | `/api/comments`  | Post a comment          |
| GET    | `/api/comments`  | Get all comments        |
| POST   | `/api/ratings`   | Rate a movie            |
| GET    | `/api/ratings`   | Get all ratings      

Supported status codes:

. 400 Bad Request

. 401 Unauthorized

. 404 Not Found

. 500 Internal Server Error


## Running Tests

```bash
pytest

AUTHOR 
author lenny kimanthi 
full Stack Developer | Python.Flask.React 