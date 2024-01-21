from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

from db_models import Base, User, Model, Data, Prediction


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

    def insert_new_data(self, user_id: int, date_created: str, **features) -> int:
        data = Data(
            user_id=user_id,
            date_created=date_created,
            **features
        )
        self.session.add(data)
        self.session.commit()
        return data.data_id

    def insert_prediction(self, user_id: int, model_id: int, data_id: int, prediction_time: int, answer: bool) -> int:
        prediction = Prediction(
            user_id=user_id,
            model_id=model_id,
            data_id=data_id,
            prediction_time=prediction_time,
            answer=answer
        )
        self.session.add(prediction)
        self.session.commit()
        return prediction.prediction_id

    def get_user_history(self, user_id: int):
        if self.session.query(Prediction).filter(Prediction.user_id == user_id).first() is None:
            return []

        all_predictions = self.session \
        .query(
            Data.date_created,
            Model.model_name,
            Prediction.prediction_time,
            Prediction.answer
        ).filter(
            Prediction.user_id == user_id
        ).join(
            Model,
            Prediction.model_id == Model.model_id,
            isouter = True
        ).join(
            Data,
            Prediction.data_id == Data.data_id,
            isouter = True
        ).all()

        res_dict = {}
        for pred in all_predictions:
            date_created = pred.date_created
            model_name = pred.model_name
            prediction_time = pred.prediction_time
            answer = pred.answer

            default_pred_times_and_answer = {
                "predictions_time": [],
                "answers": []
            }
            pred_times_and_answers = res_dict.get((date_created, model_name), default_pred_times_and_answer)
            pred_times_and_answers["predictions_time"].append(round(prediction_time, 3))
            pred_times_and_answers["answers"].append(int(answer))

            res_dict[(date_created, model_name)] = pred_times_and_answers

        res = []
        for date_created, model_name in res_dict.keys():
            res.append({
                "date": date_created,
                "model_name": model_name,
                "predictions_time": res_dict[(date_created, model_name)]["predictions_time"],
                "answers": res_dict[(date_created, model_name)]["answers"]
            })

        return res
