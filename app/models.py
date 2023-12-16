from ast import For
from sqlite3 import Timestamp
from .database import Base
from sqlalchemy import TIME, TIMESTAMP, Column, ForeignKey, ForeignKeyConstraint , Integer, String, Boolean
from sqlalchemy.sql.expression import null, text 
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False )

    owner = relationship('User')   


class User(Base):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )

    
class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer,  ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)

    


