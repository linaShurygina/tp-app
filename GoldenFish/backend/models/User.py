from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

from backend.config import Base
from backend.models.Friend import friends_association
from backend.models.FriendRequest import friend_requests_association
from backend.models.Dream import Dream



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthday = Column(Date)

    friends = relationship("User", secondary=friends_association,
                           primaryjoin=id == friends_association.c.friend_one_id,
                           secondaryjoin=id == friends_association.c.friend_two_id)
    friend_requests = relationship("User", secondary=friend_requests_association,
                                   primaryjoin=id == friend_requests_association.c.recipient_id,
                                   secondaryjoin=id == friend_requests_association.c.sender_id)
    dreams = relationship("Dream", backref="user", lazy=True)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.username = kwargs.get('username')
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.birthday = kwargs.get('birthday')

    def get_id(self) -> int:
        return self.id

    def get_email(self) -> str:
        return self.email

    def set_email(self, _email):
        self.email = _email

    def get_friends(self):
        return self.friends

    def check_password(self, _password):
        return bcrypt.verify(_password, self.password)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

