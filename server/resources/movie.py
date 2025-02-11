from flask_restful import Resource
from flask import request, jsonify
from models import db, Movie

class MovieListResource(Resource):
    def get(self):
        """Get all movies"""
        movies = Movie.query.all()
        return jsonify([movie.to_dict() for movie in movies])

    def post(self):
        """Add a new movie"""
        data = request.get_json()

        # Validation
        title = data.get('title')
        genre = data.get('genre')

        if not title or not genre:
            return {"error": "Both 'title' and 'genre' are required."}, 400

        # Add new movie
        new_movie = Movie(title=title.strip(), genre=genre.strip())
        try:
            db.session.add(new_movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to add movie: {str(e)}"}, 500

        return jsonify(new_movie.to_dict()), 201


class MovieResource(Resource):
    def get(self, movie_id):
        """Get a specific movie by ID"""
        movie = Movie.query.get_or_404(movie_id)
        return jsonify(movie.to_dict())

    def patch(self, movie_id):
        """Update a movie"""
        movie = Movie.query.get_or_404(movie_id)
        data = request.get_json()

        # Update only provided fields
        title = data.get('title')
        genre = data.get('genre')

        if title:
            movie.title = title.strip()
        if genre:
            movie.genre = genre.strip()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update movie: {str(e)}"}, 500

        return jsonify(movie.to_dict()), 200

    def delete(self, movie_id):
        """Delete a movie"""
        movie = Movie.query.get_or_404(movie_id)
        try:
            db.session.delete(movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete movie: {str(e)}"}, 500

        return {"message": "Movie deleted successfully"}, 200
