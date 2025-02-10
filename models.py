# models.py
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# ✅ Association Object for Watchlist
class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    rating = db.Column(db.Integer)  # Optional: Rating attribute

    user = db.relationship('User', back_populates='watchlist')
    movie = db.relationship('Movie', back_populates='watchlisted_by')

# ✅ User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    
    watchlist = db.relationship('Watchlist', back_populates='user', cascade='all, delete-orphan')

    def to_dict(self):
        return {"id": self.id, "username": self.username}

# ✅ Movie Model
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer)

    watchlisted_by = db.relationship('Watchlist', back_populates='movie', cascade='all, delete-orphan')

    def to_dict(self):
        return {"id": self.id, "title": self.title, "genre": self.genre}
