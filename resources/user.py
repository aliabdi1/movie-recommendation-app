from flask_restful import Resource, reqparse
from flask import jsonify, request
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# ✅ Request Parsers
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

# ✅ User Registration
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"error": "Username already exists"}, 400

        new_user = User(username=args['username'], email=args['email'])
        new_user.set_password(args['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict(), 201

# ✅ Single User Operations
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

# ✅ Login Route
class UserLoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args["username"]).first()

        if user and user.check_password(args["password"]):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)

        return jsonify({"message": "Invalid credentials"}), 401

# ✅ Protected Route
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify({"message": f"Hello User {current_user}"})
