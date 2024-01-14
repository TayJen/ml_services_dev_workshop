from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('sqlite:///billing_service.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer)


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    price = Column(Integer)


class ModelAnswer(Base):
    __tablename__ = "models_answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer)
    query_id = Column(Integer)
    answer = Column(Float)


def insert_new_user(username: str, password: str):
    user = User(
        username=username,
        password=password,
        balance=100
    )
    session.add(user)
    session.commit()


Base.metadata.create_all(engine)


if __name__ == "__main__":
    insert_new_user("tayjen", "123")
    insert_new_user("erikgab", "404")
    insert_new_user("robert0", "admin")

    users = session.query(User).all()

    for user in users:
        print(user.id, user.username, user.password)

    user = session.query(User).filter(User.password == 'admin').first()
    print(user.id, user.username, user.password)

    user_new = session.query(User).filter(User.password == 'lll').first()
    print(user_new)
    if user_new is not None:
        print(user_new.id, user_new.username, user_new.password)
