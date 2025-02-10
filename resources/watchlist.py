from flask import request
from flask_restful import Resource, reqparse, Api
from flask import jsonify
from models import db, Watchlist, User, Movie





# Request Parser
parser = reqparse.RequestParser()
parser.add_argument('rating', type=int, required=False)  # Optional rating field


class WatchlistResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        watchlist = [
            {
                "id": item.movie.id,
                "title": item.movie.title,
                "genre": item.movie.genre,
                "rating": item.rating
            } for item in user.watchlist
        ]
        return jsonify(watchlist)
        
    def post(self, user_id, movie_id):
        data = request.get_json()
        rating = data.get('rating')

        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)

        if not user or not movie:
            return {"message": "User or Movie not found"}, 404

        watchlist_entry = Watchlist(user_id=user_id, movie_id=movie_id, rating=rating)
        db.session.add(watchlist_entry)
        db.session.commit()

        return {"message": "Movie added to watchlist"}, 201
    
    def patch(self, user_id, movie_id):
        data = request.get_json()
        rating = data.get('rating')

    # Match the query logic with DELETE (which works fine)
        watchlist_entry = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if not watchlist_entry:
            return {"message": "Watchlist entry not found"}, 404  # Fixed message

        watchlist_entry.rating = rating
        db.session.commit()

        return {"message": "Watchlist rating updated successfully"}, 200


    def delete(self, user_id, movie_id):
        entry = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return {"message": "Movie removed from watchlist"}, 200
        return {"message": "Movie not found in watchlist"}, 404

