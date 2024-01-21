from datetime import datetime, timedelta
from typing import Any, Annotated, List, Dict

import os
import time

import pickle
import pandas as pd
from jose import JWTError

import uvicorn
from fastapi import Depends, FastAPI, File, Body, UploadFile, status, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from base_models import User
from database import Database

from util.jwt_util import create_access_token, decode_access_token
from util.pwd_util import get_password_hash, verify_password


models = {
    "LogisticRegression": pickle.load(open(os.path.join(os.getcwd(), "models", "lr_model.pkl"), 'rb')),
    "DecisionTreeClassifier": pickle.load(open(os.path.join(os.getcwd(), "models", "tree_model.pkl"), 'rb')),
    "RandomForestClassifier": pickle.load(open(os.path.join(os.getcwd(), "models", "forest_model.pkl"), 'rb'))
}

app = FastAPI()
db = Database()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home")
async def home():
    return FileResponse('static/html/home.html')


@app.get("/register")
async def register():
    return FileResponse('static/html/register.html')


@app.get("/login")
async def login():
    return FileResponse('static/html/login.html')


def register_user(username: str, password: str):
    user = db.get_user(username)
    if user:
        return False

    hashed_password = get_password_hash(password)
    new_user = {
        "username": username,
        "hashed_password": hashed_password,
    }
    db.insert_new_user(**new_user)

    return True


@app.post("/register")
async def register_for_access_token(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    if not register_user(username, password):
        ans = "fail"
        print('Failed registration')
    else:
        ans = "success"
        print('Successfully registered')

    return {"result": ans}


def authenticate_user(username: str, password: str):
    user = db.get_user(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@app.post("/login")
async def login_for_access_token(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    print(username)
    user = authenticate_user(username, password)
    if not user:
        res = "fail"
        access_token = None
    else:
        res = "success"
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

    print(res)

    return {"result": res, "access_token": access_token, "token_type": "bearer"}


@app.post("/current_user")
async def get_current_user(token: Annotated[str, Body()]):
    res = {
        "result": "fail",
        "username": None,
        "balance": None
    }
    print(token)
    if token:
        try:
            payload = decode_access_token(token)
            username: str = payload.get("sub")
            print(f"user with username {username}")
            if username is not None:
                user = db.get_user(username=username)
                if user is not None:
                    res["result"] = "success"
                    res["username"] = user.username
                    res["balance"] = user.balance
        except JWTError:
            print("JWT Error")

    return res


@app.post("/predict")
async def predict(
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
    model_choice: str = "LogisticRegression"
):
    if model_choice not in models:
        return False

    user = db.get_user(username=current_user.username)
    user_id = user.user_id
    user_balance = user.balance

    model_db = db.get_model(model_name=model_choice)
    model_id = model_db.model_id
    model_price = model_db.price
    loaded_model = models.get(model_db.model_name)

    df = pd.read_csv(file.file)
    all_answers = []
    for _, row in df.iterrows():
        if model_price > user_balance:
            break

        start = time.time()
        row_values = row.values
        print(row_values)

        features = dict({col: value for col, value in zip(df.columns, row_values.tolist())})
        print(features)

        data_id = db.insert_new_data(user_id=user_id, **features)

        answer = loaded_model.predict([row_values])[0]
        answer = 1 if answer >= 0.5 else 0

        prediction_time = time.time() - start

        db.insert_prediction(model_id, data_id, prediction_time, answer)

        user_balance -= model_price
        all_answers.append(answer)

    db.update_user_balance(user, user_balance)
    return {"prediction": all_answers}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
