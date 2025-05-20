from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_smorest import Blueprint, abort
from iWater.app.models.user import UserModel
from passlib.hash import pbkdf2_sha256

from iWater.app.schemas import UserSchema

blp = Blueprint("authentication", "auth", description="User Authentication")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(sefl, user_data):
        if UserModel.find_by_username(user_data["username"]):
            abort(400, message="A user with that username already exists")

        user = UserModel(
            username=user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"]),
        )

        user.save_to_db()

        return {"message": "User Created Successfully"}
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.find_by_username(user_data["username"])

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    # current_user = get_jwt_identity()
    return jsonify(logged_in_as="Amar"), 200