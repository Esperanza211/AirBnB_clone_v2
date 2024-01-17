#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")
# associated table that presents the relationship
# Many-To-Many between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
    ),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if storage_type == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', cascade="all,delete", backref="place")
        amenities = relationship(
            'Amenity',
            secondary='place_amenity',
            viewonly=False,
            back_populates='place_amenities'
        )

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter for reviews related to this Place"""
            from models import storage
            reviews_List = []
            All_reviews = storage.all(Review)
            for review in All_reviews.values():
                if review.place_id == self.id:
                    reviews_List.append(review)
            return reviews_List

        @property
        def amenities(self):
            """getter for amenities related to this Place"""
            from models import storage
            amenities_List = []
            All_amenities = storage.all(Amenity)
            for Am in All_amenities.values():
                for amenity_id in Am.amenity_ids:
                    if amenity_id == self.id:
                        amenities_List.append(Am)
            return amenities_List

        @amenities.setter
        def amenities(self, obj):
            """ Add an Amenity.id to the attribute amenity_ids """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
