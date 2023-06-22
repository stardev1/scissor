from flask import Blueprint, request, jsonify
from models.user import Users
from db import db

from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

user = Blueprint("user", __name__)

@user.route("/users")
@user.route("/user")
@jwt_required()
def index():
    """ 
        Get all user info
    """
    query_user = Users.query.filter_by(id=get_jwt_identity()).first()

    return jsonify(status="ok",  data = query_user.to_json()), 200

@user.route("/user", methods=["POST"])
def create():
    """ 
        Create a user
    """
    
    data = request.form
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    user = Users(first_name=first_name, last_name = last_name, email=email, password=password)
    return jsonify(status="ok", message="User created successfully", data = user.to_json()), 200


@user.route("/user/edit", methods=["PATCH"])
@jwt_required()
def edit_user():
    """ 
        Edit a user
  """
    req_data = request.json

    user = Users.query.filter_by(id=get_jwt_identity()).first()
    password = req_data.get("password")

    if password and password != '':
        req_data['password'] = generate_password_hash(password)
    else:
        if password or password == "":
            req_data.pop("password")

    
    try:
        user.bm_update(req_data)
        return jsonify(status="ok", message="User updated successfully", data = user.to_json()), 200
    
    except: 
        return jsonify(status="error", message="User update failed"), 400
