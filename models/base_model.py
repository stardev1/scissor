from datetime import datetime
import sqlalchemy as sa
from uuid import uuid4
from db import db
from cache import cache
import json

class BaseModel:
    id = sa.Column(sa.String(36), primary_key=True, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, *args, **kwargs):
       
       if kwargs:
            self.__set_attributes(kwargs)
       else:

            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
    
    def __set_attributes(self, attr_dict):
        """
            private: converts attr_dict values to python class attributes
        """
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if "url" in attr_dict:
            if not attr_dict["url"].startswith("http://") and not attr_dict["url"].startswith("https://"):
                attr_dict["url"] = "http://" + attr_dict["url"]

        for attr, val in attr_dict.items():
            setattr(self, attr, val)
    
    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False
    
    @classmethod
    @cache.memoize()
    def find_by_short_url(cls, url):
        """
            finds a basemodel by id
        """
        print(f" ------- recalculate {url} cache -----------")
        data = cls.query.filter_by(short_url=url).first_or_404()
        return data
    

    def bm_update(self, attr_dict=None) -> dict:
        """
            updates the basemodel and sets the correct attributes
        """
        IGNORE = [
            'id', 'created_at', 'updated_at',
             'user_id', 'visitors', 'short_url_id'
        ]
        data = {}
        if attr_dict:
            updated_dict = {
                k: v for k, v in attr_dict.items() if k not in IGNORE and v and v != ""
            }
            for key, value in updated_dict.items():
                setattr(self, key, value)
            data = self.save()
        return data

    
    def save(self):
        """
            updates attribute updated_at to current time
        """
        
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        

    def to_json(self):
        """
            returns json representation of self
        """
        obj_class = self.__class__.__name__
        bm_dict = {
            k: v if self.__is_serializable(v) else str(v)
            for k, v in self.__dict__.items()
        }
        bm_dict.pop('_sa_instance_state', None)
        if obj_class == "Users":
            bm_dict.pop('password', None)
        if obj_class == "ShortUrl":
            bm_dict['qr'] = self.qr
            
        return(bm_dict)

    def __str__(self):
        """
            returns string type representation of object instance
        """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
            deletes current instance from storage
        """
        db.session.execute(sa.delete(self.__class__).where(self.__class__.id == self.id))
        db.session.commit()
        return True