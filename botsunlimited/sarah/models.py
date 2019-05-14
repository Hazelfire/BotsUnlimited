"""
File: models.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Models that Sarah can access
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# pylint: disable=R0903
class Event(BASE):
    """ Represents a club event """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)

    def __repr__(self):
        return "<Event({})>".format((self.name))
