🎬 Movie Recommendation App - Backend

This is the Flask API backend for the Movie Recommendation App, built with Flask-RESTful, SQLAlchemy, and Flask-Migrate. It provides RESTful endpoints to manage users, movies, and watchlists.

🚀 Features

User Management: Create, retrieve, and manage users.
Movie Database: Add and view movies.
Watchlist Functionality: Users can add movies to their watchlist with ratings.
CRUD Operations: Full CRUD support for watchlists, with create & read for users and movies.
Relational Database: One-to-many and many-to-many relationships with SQLAlchemy ORM.

📦 Project Structure

server/
├── app.py
├── models.py
├── resources/
│   ├── user.py
│   ├── movie.py
│   └── watchlist.py
├── migrations/
├── instance/
│   └── database.db
└── requirements.txt

⚙️ Technologies Used

Python 3.8+
Flask
Flask-RESTful
Flask-SQLAlchemy
Flask-Migrate
SQLite (for development)

📥 Installation & Setup

Clone the repository:

git clone git@github.com:aliabdi1/movie-recommendation-app.git

cd movie-recommendation-app/server


Create a virtual environment:

python3 -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run database migrations:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Start the development server:

flask run


🔑 API Endpoints

Users
    POST /users - Create a new user
    GET /users/<user_id> - Get a user's details

Movies
    POST /movies - Add a new movie
    GET /movies - Retrieve all movies

Watchlist
    GET /users/<user_id>/watchlist - Get a user's watchlist
    POST /users/<user_id>/watchlist/<movie_id> - Add a movie to watchlist
    PATCH /users/<user_id>/watchlist/<movie_id> - Update rating for a movie in watchlist
    DELETE /users/<user_id>/watchlist/<movie_id> - Remove a movie from watchlist


🗃️ Database Schema

User: id, username, email

Movie: id, title, genre

Watchlist: id, user_id, movie_id, rating (Many-to-Many 
with extra attribute rating)


📤 Deployment

For deployment, consider using:

Gunicorn + Nginx for production servers.

Docker for containerization.

🤝 Contributing

1.Fork the repository.
2.Create your feature branch: git checkout -b feature-name
3.Commit your changes: git commit -m 'Add new feature'
4.Push to the branch: git push origin feature-name
5.Open a Pull Request.


📝 License

This project is licensed under the MIT License. Feel free to use and modify it for your learning or personal projects.

