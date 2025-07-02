# Movieverse - Backend Application

## Project Overview

Movieverse is a full-stack application that allows users to explore movies, save favorites, and share ratings and comments. This backend service powers the React frontend by handling user authentication, movie data retrieval, and user-generated content.

## Key Functionalities

1. **User Authentication**
   - Secure registration and login with JWT tokens
   - Password hashing for security
   - Rate limiting to prevent abuse

2. **Movie Management**
   - Search movies using the OMDb API
   - Save favorite movies to user profiles
   - View detailed movie information


3. **Technical Features**
   - Comprehensive error handling
   - Automated testing suite
   - API documentation
   - Deployment-ready configuration

## User Stories

### Authentication & Profile
- As a new user, I want to register an account so I can access all features
- As a returning user, I want to log in securely to access my saved data
- As a security-conscious user, I want my password to be securely hashed
- As a user, I want to view and update my profile information

### Movie Discovery
- As a movie enthusiast, I want to search for movies by title so I can find ones I'm interested in
- As a user, I want to see detailed movie information (plot, cast, ratings) in one place
- As a frequent user, I want the app to remember my favorite movies

### Community Interaction
- As a user, I want to rate movies so I can share my opinions
- As a social user, I want to read comments from other movie fans
- As an engaged user, I want to leave my own comments on movies
- As a data-driven user, I want to see average ratings for movies

### Technical Requirements
- As a developer, I want comprehensive tests to ensure reliability
- As an API consumer, I want clear documentation to understand how to use the endpoints
- As an admin, I want proper error handling to diagnose issues
- As a team member, I want the app deployed so users can access it

## Technology Stack

**Backend:**
- Python Flask
- Flask-JWT-Extended for authentication
- SQLAlchemy for database operations
- Bcrypt for password hashing
- OMDb API for movie data
- pytest for testing

**Deployment:**
- Render or Heroku for hosting
- Postman for API testing

