from fastapi import FastAPI
from typing import Any, List, Dict


app = FastAPI()

models_list = [{"id": 1, "name": "LogisticRegression"},
               {"id": 2, "name": "DecisionTree"},
               {"id": 3, "name": "RandomForest"},
               {"id": 4, "name": "XGBoost"}]


# http://127.0.0.1:8000/
@app.get("/")
def index():
    return {"message": "Hello World!"}


@app.get("/models")
def read_models() -> List[Dict[str, Any]]:
    """
        Получение списка моделей
        :params: None
        :return: list of dicts with models ids and names
    """
    return models_list


@app.get("/models/{model_id}")
def read_model(model_id: int):
    for model in models_list:
        if model["id"] == model_id:
            return model
    return {"message": f"Model with id {model_id} was not found"}
