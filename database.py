import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

from db_models import Base, User, Model, Data, Prediction, UserHistory


class Database:
    def __init__(self):
        engine = create_engine('sqlite:///main_db.db', echo=True)
        self.session = sessionmaker(bind=engine)()

        if database_exists(engine.url):
            Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)

        self._add_models()

    def _add_models(self):
        lr_model = Model(model_name="LogisticRegression", price=1)
        tree_model = Model(model_name="DecisionTreeClassifier", price=3)
        forest_model = Model(model_name="RandomForestClassifier", price=5)

        self.session.add(lr_model)
        self.session.add(tree_model)
        self.session.add(forest_model)

        self.session.commit()

    def get_model(self, model_name: str):
        return self.session.query(Model).filter(Model.model_name == model_name).first()

    def insert_new_user(self, username: str, hashed_password: str) -> int:
        user = User(
            username=username,
            password=hashed_password,
            balance=100
        )
        self.session.add(user)
        self.session.commit()
        return user.user_id

    def get_user(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def update_user_balance(self, user: User, user_balance: int):
        user.balance = user_balance
        self.session.commit()

    def insert_new_data(self, user_id: int, **features) -> int:
        data = Data(
            user_id=user_id,
            date_created=datetime.datetime.now(),
            **features
        )
        self.session.add(data)
        self.session.commit()
        return data.data_id

    def insert_prediction(self, model_id: int, data_id: int, prediction_time: int, answer: bool) -> int:
        prediction = Prediction(
            model_id=model_id,
            data_id=data_id,
            prediction_time=prediction_time,
            answer=answer
        )
        self.session.add(prediction)
        self.session.commit()
        return prediction.prediction_id

    def insert_user_history(self, user_id: int, prediction_id: int) -> int:
        user_history = UserHistory(
            user_id=user_id,
            prediction_id=prediction_id
        )
        self.session.add(user_history)
        self.session.commit()
        return user_history.user_history_id