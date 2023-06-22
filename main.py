
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from api import apiRoutes
from db import db
from flask_login import LoginManager
from web.short_url import webShortUrl
from flask_swagger_ui import get_swaggerui_blueprint

from web.webAuth import webAuth, load_user
from cache import cache







SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/swagger_file'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "URL Shortener application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)


def create_app(config):


    app = Flask(__name__, template_folder="web/templates", static_folder="web/static", instance_relative_config=True)

    
    app.url_map.strict_slashes = False
    
    
    # global strict slashes
   

    # app.make_config.
    jwt = JWTManager(app)
    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_message_category = "info"
    login_manager.session_protection = "strong"
    login_manager.user_loader(load_user)

    login_manager.login_view = "webAuth.login"

    app.config.from_object(config)
    
    app.register_blueprint(apiRoutes)

    app.register_blueprint(swaggerui_blueprint)

    app.register_blueprint(webShortUrl)


    app.register_blueprint(webAuth)

    cache.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app
