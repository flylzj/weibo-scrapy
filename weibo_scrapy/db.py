# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class WeiboUser(Base):

    __tablename__ = 'weibo_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(12), unique=True, nullable=False)
    username = Column(String(32), nullable=False)
    sexual = Column(String(4), default='')
    location = Column(String(32), default='')
    raw_birth = Column(String(32))
    birth = Column(Date)
    desc = Column(String(256), default='')
    raw_sign_up_date = Column(String(32))
    sign_up_date = Column(Date)



class Weibo(Base):

    __tablename__ = 'weibo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(32), nullable=False)
    user_id = Column(String(12), ForeignKey(WeiboUser.user_id), nullable=False, unique=True)
    content = Column(Text)
    raw_pub_time = Column(String(32))
    pub_time = Column(DateTime)
    post_count = Column(Integer)
    comment_count = Column(Integer)
    like_count = Column(Integer)
    from_url = Column(String(256), default='')

    user = relationship('WeiboUser', backref='weibos')

if __name__ == '__main__':
    ENGINE = create_engine('sqlite:///../data.db')
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)