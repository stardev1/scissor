from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Regexp, ValidationError, EqualTo, optional
from utils.depend import validateUrl, validCustomUrl, checkDB, daily_limits
from models.user import Users


class LoginForm(FlaskForm):
    """ Form for login"""
    email = StringField("Email", validators= [
        InputRequired(), Regexp(r'^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$', message='Invalid URL')]
    )
    password = PasswordField("Password", validators= [
        InputRequired(), Length(min=4, max=20)
        ])
    
    

class SignupForm(FlaskForm):
    """ Form for signup"""
    first_name = StringField("first_name", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    last_name = StringField("last_name", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    email = StringField("Email", validators= [
        InputRequired()
    ])
    password = PasswordField("Password", validators= [
        InputRequired(), Length(min=4, max=20)
        ])
    
    confirm_password = PasswordField("Password", validators= [
        InputRequired(), Length(min=4, max=20), EqualTo('password')
        ])
    
    def validate_email(self, email):
         user = Users.query.filter_by(email = email.data).first()
         if user:
            raise ValidationError("Email already in use")
         
class UpdateUserForm(FlaskForm):
    """ Form for update user"""
    id = HiddenField("id")

    first_name = StringField("first_name", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    last_name = StringField("last_name", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    email = StringField("Email", validators= [
        InputRequired()
    ])
    password = PasswordField("Password", validators= [
           optional(), Length(min=4, max=20) 
        ])
    
    confirm_password = PasswordField("Password", validators= [
         optional(), Length(min=4, max=20), EqualTo('password')
        ])
    
    def validate_email(self, email):
         user = Users.query.filter_by(email = email.data).first()
         if user and user.id != self.id.data:
            raise ValidationError("Email already in use")
         

class NewUrl(FlaskForm):
    """ Form for new url"""
    user_id = HiddenField("user_id")
    url = StringField("url", validators=[
        InputRequired(), 
        # Regexp(r'^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$', message='Invalid URL')
    ])
    custom_url = StringField("custom_url")


    def validate_url(self, url):

        if daily_limits(self.user_id.data)['status']:
            raise ValidationError("Daily limit reached")

        check_url = validateUrl(url.data)
        
        if not check_url:
            raise ValidationError("URL not working")
    
    def validate_custom_url(self, custom_url):

        validation_func(custom_url.data)


class UpdateUrl(FlaskForm):
    """ Form for update url"""
    id = HiddenField("id")

    url = StringField("url", validators=[
        InputRequired(), 
        # Regexp(r'^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$', message='Invalid URL')
    ])

    short_url = StringField("short_url")

    def validate_url(self, url):
        check_url = validateUrl(url.data)

        if not check_url:
            raise ValidationError("URL not working")

    def validate_short_url(self, custom_url):
        validation_func(custom_url.data, self.id.data)

def validation_func(data, id = None):
   """ validate data """
   if data:
        
        short_custom_url = validCustomUrl(data)
        db_check = checkDB(short_custom_url, id)
        if db_check:
            raise ValidationError("Custom url already in use") 
    