from flask import Blueprint, request, jsonify
from models.user import Users
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token

authRoute = Blueprint("auth", __name__)


# route for logging user in
@authRoute.route('/login', methods =['POST'])
def login():
    """ login using email and password
    """
    # creates dictionary of form data
    auth = request.json
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return jsonify({
            "status":"error",
            "message":'Required value not found',
        }), 422
            
  
    user = Users.query.filter_by(email = auth.get('email')).first()
  
    if not user:
        # returns 401 if user does not exist
        return jsonify({
            "status":"error",
            "message":"Could not verify, email does not match any record"
        }), 401
            
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        
        access_token = create_access_token(identity=user.id)
  
        return jsonify({
             "status":"ok",
             **user.to_json(),
            'token' : access_token}), 201
    
    # returns 403 if password is wrong
    return jsonify({
        "status":"error",
        "message": 'Could not verify, Wrong Password',
        }), 401
# signup route
@authRoute.route('/signup', methods =['POST'])
def signup():
    """ singup function
        parameters:
            first_name: string
            last_name: string
            email: string
            password: string
        returns:
            status: ok or error
            message: ok or error message
            token: JWT Token if user is created successfully
            user: user details if user is created successfully
            code: 201 if user is created successfully
            code: 409 if user already exists
            code: 422 if required parameters are missing
            code: 401 if user already exists
            code: 403 if password is wrong
            code: 500 if any other error occurs
        """
    # creates a dictionary of the form data
    data = request.get_json()
  
    # gets name, email and password
    first_name, last_name, email = data.get('first_name'), data.get('last_name'), data.get('email')
    password = data.get('password')

    if first_name == None or last_name == None or email == None or password == None:
        return jsonify({
            "status": "error",
            "message": "first_name, last_name, email and password is required"
        }), 422

    
  
    # checking for existing user
    user = Users.query.filter_by(email = email).first()
    if not user:
        # database ORM object
        user = Users(
            last_name = last_name,
            first_name = first_name,
            email = email,
            password = generate_password_hash(password)
        )

        user.save()
  
        return jsonify({
            "status": "ok",
            "message": "user created successfully"
                    }), 201
    else:
        # returns 202 if user already exists
        return jsonify({
            "status":"error",
            "message": "User already exists. Please Log in."
            }), 409