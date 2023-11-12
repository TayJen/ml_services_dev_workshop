from fastapi import FastAPI


app = FastAPI()


# http://127.0.0.1:8000/
@app.get("/")
def index():
    return {"message": "Hello World!"}


models_list = [{"id": 1, "name": "LogisticRegression"},
               {"id": 2, "name": "DecisionTree"},
               {"id": 3, "name": "RandomForest"},
               {"id": 4, "name": "XGBoost"}]


@app.get("/models")
def read_models():
    return models_list


@app.get("/models/{model_id}")
def read_model(model_id: int):
    for model in models_list:
        if model["id"] == model_id:
            return model
    return {"message": f"Model with id {model_id} was not found"}
