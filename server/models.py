from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from app import db


watchlist = db.Table('watchlist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)

# User Model
class User(db.Model, SerializerMixin):  
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    watchlist = db.relationship('Movie', secondary=watchlist, backref=('users_watching'))

    reviews = db.relationship('Review', back_populates='users', cascade='all, delete')
    
    serialize_rules = ('-reviews.user',)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

# Movie Model
class Movie(db.Model, SerializerMixin):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50))

    reviews = db.relationship('Review', back_populates='movies', cascade='all, delete-orphan')
    
    serialize_rules = ('-reviews.movie',)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
        }

# Review Model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')  
    movie = db.relationship('Movie', back_populates='reviews')  
    
    serialize_rules = ('-user.reviews', '-movie.reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'user': self.user.to_dict(),  # Serialize associated user
            'movie': self.movie.to_dict()  # Serialize associated movie
        }
