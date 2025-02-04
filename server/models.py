from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

# User Model
class User(db.Model, SerializerMixin):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
    
    serialize_rules = ('-reviews.user',)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

# Movie Model
class Movie(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50))

    reviews = db.relationship('Review', back_populates='movie', cascade='all, delete')
    
    serialize_rules = ('-reviews.movie',)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
        }

# Review Model
class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

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
