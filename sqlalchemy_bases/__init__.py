from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass
