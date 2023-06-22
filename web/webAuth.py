from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from web.forms import LoginForm, SignupForm, UpdateUserForm
from models.user import Users
from werkzeug.security import check_password_hash, generate_password_hash


webAuth = Blueprint("webAuth", __name__)


def load_user(user_id):
    return Users.query.get(user_id)



@webAuth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email = email).first()

        if (user):
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect("/")
            else:
                form.email.errors.append("Email or password is incorrect")
        else:
            form.email.errors.append("Email or password is incorrect")
            
    return render_template("login.html", form=form)

@webAuth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        
        user = Users(
            last_name = last_name,
            first_name = first_name,
            email = email,
            password = generate_password_hash(password)
        )

        user.save()

        login_user(user)
        return redirect("/")
        
    
    return render_template("signup.html", form=form)

@webAuth.route("/profile", methods=["POST", "GET"])
@login_required
def profile():

    user = current_user
  
    form = UpdateUserForm(id = user.id, first_name = user.first_name, last_name = user.last_name, email = user.email)

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        updated_data = {
            "first_name": first_name, 
            "last_name": last_name,
            "email": email,
            "password": generate_password_hash(password)}
        
        if password == "":
            updated_data.pop("password")

        user = user.bm_update(updated_data)

      
      

        return redirect(url_for("webShortUrl.index"))
    
    return render_template("profile.html", user = current_user.to_json(), form = form)



@webAuth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("webAuth.login"))