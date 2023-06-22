from typing import List
from db import db
import sqlalchemy as sa
from sqlalchemy.orm import relationship, mapped_column, Mapped
from models.base_model import BaseModel

class ShortUrl(BaseModel, db.Model):

    
    url = sa.Column(sa.String(255), nullable=False)
    short_url = sa.Column(sa.String(10), nullable=False)
    clicks = sa.Column(sa.Integer, nullable=False, default=0)
    is_custom = sa.Column(sa.Boolean, nullable=False, default=False)
    user_id: Mapped[str] = mapped_column(sa.ForeignKey("users.id"))
    user = relationship("Users", back_populates="short_urls", lazy=True)
    visitors : Mapped[List["Visitor"]] = relationship(back_populates="short_url", lazy=True)


    @property
    def qr(self):
        return f"https://quickchart.io/qr?text=http://localhost:5000/{self.short_url}"

class Visitor(BaseModel, db.Model ):

    ip_address = sa.Column(sa.String(20), nullable=False)
    agent_version = sa.Column(sa.String(100), nullable=True)
    agent_platform = sa.Column(sa.String(100), nullable=True)
    is_mobile = sa.Column(sa.Boolean, nullable=True)
    short_url_id: Mapped[str] = mapped_column(sa.ForeignKey("short_url.id"), nullable=False)
    short_url: Mapped["ShortUrl"] = relationship(back_populates="visitors", lazy=True)

 


## create sqlalchemy onetomany relationship using shorturl to user

