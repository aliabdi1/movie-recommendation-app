from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Movie

# Request Parser
parser = reqparse.RequestParser()
# parser.add_argument('title', type=str, required=True)
parser.add_argument('genre', type=str, required=False)

class MovieListResource(Resource):
    def get(self):
        movies = Movie.query.all()
        return jsonify([movie.to_dict() for movie in movies])

    def post(self):
        args = parser.parse_args()
        new_movie = Movie(title=args['title'], genre=args['genre'])
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict()), 201

class MovieResource(Resource):
    def get(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return jsonify(movie.to_dict())

    def patch(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        args = parser.parse_args()
        movie.title = args['title']
        movie.genre = args['genre']
        db.session.commit()
        return jsonify(movie.to_dict())

    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return {"message": "Movie deleted"}, 200
