import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    posts = relationship('Post', back_populates='user') 
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='followed')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower')
    likes = relationship('Like', back_populates='user')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    post = relationship('Post', back_populates='media')

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')



class Follower(Base):
    __tablename__ = 'follower'

    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    
    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
