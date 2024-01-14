from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer)


class Model(Base):
    __tablename__ = "models"
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    price = Column(Integer)


class Data(Base):
    __tablename__ = "data"
    user_id = Column(Integer)
    data_id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(Date)


class Prediction(Base):
    __tablename__ = "predictions"
    model_id = Column(Integer)
    data_id = Column(Integer)
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_time = Column(Integer)
    answer = Column(Boolean)


class UserHistory(Base):
    __tablename__ = "users_history"
    user_id = Column(Integer)
    prediction_id = Column(Integer)
    user_history_id = Column(Integer, primary_key=True, autoincrement=True)
