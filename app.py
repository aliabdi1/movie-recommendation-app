from flask import Flask
import logging
logging.basicConfig(level=logging.DEBUG)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models import db



app = Flask(__name__)
CORS(app)

# ✅ Correct Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Import models and resources AFTER initializing app, db, api
from models import db
from resources.movie import MovieListResource, MovieResource
from resources.user import UserListResource, UserResource
from resources.watchlist import WatchlistResource

# ✅ API Routes
api.add_resource(MovieListResource, '/movies')
api.add_resource(MovieResource, '/movies/<int:movie_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(WatchlistResource, '/users/<int:user_id>/watchlist', '/users/<int:user_id>/watchlist/<int:movie_id>')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
