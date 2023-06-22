import pytest
from main import create_app
from config.default import TestConfig
from models.user import Users
from db import db
from flask_jwt_extended import JWTManager




@pytest.fixture()
def app():
    app = create_app(TestConfig)

   
    yield app

    


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()