from flask import Flask
import logging
logging.basicConfig(level=logging.DEBUG)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
CORS(app)

# ✅ Correct Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecure_random_key_123'  # Needed for JWT auth

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Import models and resources AFTER initializing app, db, api
from models import db
from resources.movie import MovieListResource, MovieResource
from resources.user import UserListResource, UserResource, UserLoginResource, ProtectedResource
from resources.watchlist import WatchlistResource

# ✅ API Routes
api.add_resource(MovieListResource, '/movies')
api.add_resource(MovieResource, '/movies/<int:movie_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserLoginResource, '/login')  # ✅ Login Route
api.add_resource(ProtectedResource, '/protected')  # ✅ Protected Route
api.add_resource(WatchlistResource, '/users/<int:user_id>/watchlist', '/users/<int:user_id>/watchlist/<int:movie_id>')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5555)
