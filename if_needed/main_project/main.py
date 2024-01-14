from typing import Any, List, Dict

from fastapi import FastAPI, UploadFile


app = FastAPI()

models_list = [
    {"id": 1, "name": "LogisticRegression"},
    {"id": 2, "name": "DecisionTree"},
    {"id": 3, "name": "RandomForest"}
]


# http://127.0.0.1:8000/
@app.get("/")
def home():
    """
        Домашняя страница

        :params: None
        :return: None
    """


@app.post("/sign-up")
async def sign_up(username: str, password: str):
    """
        Регистрация пользователя на платформе

        :param username: str, ник пользователя
        :param password: str, пароль пользователя
        :return: None
    """
    pass


@app.post("/sign-in")
async def sign_in(username: str, password: str) -> str:
    """
        Логин пользователя на платформу

        :param username: str, ник пользователя
        :param password: str, пароль пользователя
        :return: str, ответ на вход (успешный или безуспешный)
    """
    pass


@app.post("/predict")
async def predict(api_token: str, model_name: str, data: UploadFile) -> float:
    """
        Главная функция предикта моделью (по API также будет доступ)

        :param api_token: str, токен юзера
        :param model_name: str, название модели
        :param data: file, данные для предикта
        :return: float, ответ модели
    """
    pass


@app.get("/user_history")
async def get_user_history(api_token: str):
    """
        Получение истории предиктов юзера по его апи токену

        :param api_token: str, токен юзера
    """
    pass
