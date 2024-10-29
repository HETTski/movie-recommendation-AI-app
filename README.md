
# Movie Recommendation API

A Django REST API for managing users and movies, allowing users to register, authenticate, add movies to their list, and view their collection. This API also allows users to store a list of URLs where each movie is available.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Technologies](#technologies)

## Features

- User registration and authentication (JWT-based).
- Adding movies to a user's collection with an optional description.
- Storing URLs where each movie can be watched.
- Viewing the list of movies added by a user.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```
    git clone https://github.com/HETTski/movie-recommendation-AI-app.git
    cd movie-recommendation-api
    ```
2. **Set up the virtual environment:**
    ```
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
3. **Install dependencies:**
    ```
    pip install -r req.txt
    ```
4. **Apply migrations:**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
5. **Run the development server:**
    ```
    python manage.py runserver
    ```

Your API should now be running locally at ```http://127.0.0.1:8000```.

## Usage
### Authentication
This API uses JSON Web Tokens (JWT) for authentication. You can obtain a token by sending a POST request with your credentials to /api/token/get. Include this token in the Authorization header for all authenticated requests.

### Sample Workflow
- Register a new user at ```/api/user/register/```.
- Obtain a token by logging in at ```/api/token/get```.
- Use the token to add movies to the user's collection via ```/api/user/movies/add/```.
- View the user's movie collection at ```/api/user/movies/```.

## API Endpoints

### User Endpoints
- POST ```/api/user/register/```: Register a new user.
- POST ```/api/token/get```: Obtain an access and refresh token.
- POST ```/api/token/refresh```: Refresh the access token using the refresh token.

### Movie Endpoints
- GET ```/api/user/movies/```: Retrieve the current user's movie list.
- POST ```/api/user/movies/add/```: Add a movie to the current user's movie list.
Sample JSON for Adding a Movie
```
{
  "title": "Inception",
  "description": "A mind-bending thriller about dreams within dreams.",
  "sites": [
    "https://example.com/inception",
    "https://anotherexample.com/inception"
  ]
}
```
## Authentication
For authenticated routes, use the token in the Authorization header:

```
Authorization: Bearer your_jwt_token
```

## Technologies
- Backend Framework: Django & Django REST Framework
- Database: PostgreSQL (with ArrayField for storing multiple URLs)
- Authentication: JWT (using django-rest-framework-simplejwt)
- Environment: Python 3