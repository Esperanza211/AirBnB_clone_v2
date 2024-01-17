#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """This class manages storage of hbnb models in database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates database engine"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host_name = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        db_url = f"mysql+mysqldb://{user}:{password}@{host_name}/{db_name}"

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name
        """
        all_cls_dict = {}

        if cls is not None:
            result = self.__session.query(cls).all()
            for obj in result:
                key = f"{obj.__class__.__name__}.{obj.id}"
                all_cls_dict[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            # possible bug here do not add all classes if they didn't
            # inherite from Base or if they haven't a __tablename__
            # attribute and a primary key attribute
            for clss in classes:
                result = self.__session.query(clss).all()
                for obj in result:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    all_cls_dict[key] = obj

        return all_cls_dict

    def new(self, obj):
        """add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and the current session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()

    def close(self):
        """remove session"""
        self.__session.remove()
