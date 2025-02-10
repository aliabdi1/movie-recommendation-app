from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, User

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        args = parser.parse_args()
        if User.query.filter_by(username=args['username']).first():
            return {"error": "Username already exists"}, 400

        new_user = User(username=args['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
