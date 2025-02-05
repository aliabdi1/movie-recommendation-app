from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from config import app, db, migrate
from models import db, User, Movie, Review

api = Api(app)

db.init_app(app)
migrate.init_app(app, db)

# Home Route
@app.route('/')
def home():
    return "Project Server Running!"

# ========================= MOVIES =========================

# GET all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])

# GET single movie
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(movie.to_dict())

# POST create movie
@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    new_movie = Movie(title=data['title'], genre=data['genre'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.to_dict()), 201

# PATCH update movie
@app.route('/movies/<int:id>', methods=['PATCH'])
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    data = request.json
    if 'title' in data:
        movie.title = data['title']
    if 'genre' in data:
        movie.genre = data['genre']
    
    db.session.commit()
    return jsonify(movie.to_dict())

# DELETE movie
@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted"}), 200

# ========================= USERS =========================

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# GET single user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# POST create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# PATCH update user
@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    if 'username' in data:
        user.username = data['username']
    
    db.session.commit()
    return jsonify(user.to_dict())

# DELETE user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# ========================= REVIEWS =========================

# GET all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])

# GET reviews for a specific movie
@app.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return jsonify([review.to_dict() for review in reviews])

# POST create review
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['rating', 'user_id', 'movie_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if movie exists
    movie = Movie.query.get(data['movie_id'])
    if not movie:
        return jsonify({'error': f"Movie with id {data['movie_id']} not found"}), 404
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': f"User with id {data['user_id']} not found"}), 404
    
    # Create new review
    try:
        new_review = Review(
            rating=data['rating'],
            user_id=data['user_id'],
            movie_id=data['movie_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# PATCH update review
@app.route('/reviews/<int:id>', methods=['PATCH'])
def update_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    
    data = request.json
    if 'rating' in data:
        review.rating = data['rating']
    
    db.session.commit()
    return jsonify(review.to_dict())

# DELETE review
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200

# ========================= SERVER =========================


@app.route('/users/<int:user_id>/watchlist', methods=['GET'])
def get_watchlist(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([movie.to_dict() for movie in user.watchlist])

@app.route('/users/<int:user_id>/watchlist/<int:movie_id>', methods=['POST'])
def add_to_watchlist(user_id, movie_id):
    user = User.query.get_or_404(user_id)
    movie = Movie.query.get_or_404(movie_id)
    
    if movie not in user.watchlist:
        user.watchlist.append(movie)
        db.session.commit()
    
    return jsonify({"message": "Movie added to watchlist"}), 200

@app.route('/users/<int:user_id>/watchlist/<int:movie_id>', methods=['DELETE'])
def remove_from_watchlist(user_id, movie_id):
    user = User.query.get_or_404(user_id)
    movie = Movie.query.get_or_404(movie_id)
    
    if movie in user.watchlist:
        user.watchlist.remove(movie)
        db.session.commit()
    
    return jsonify({"message": "Movie removed from watchlist"}), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5555)
