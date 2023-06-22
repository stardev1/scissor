from sqlalchemy.orm import relationship 
from flask_login import UserMixin
import sqlalchemy as sa
from models.base_model import BaseModel
from db import db

class Users(BaseModel, db.Model, UserMixin ):

    first_name = sa.Column(sa.String(100), nullable=False)
    last_name = sa.Column(sa.String(100), nullable=False)
    email = sa.Column(sa.String(100), nullable=False)
    password =  sa.Column(sa.String(100), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    short_urls = relationship("ShortUrl", back_populates="user", lazy=True)