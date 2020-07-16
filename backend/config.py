import random

DEBUG = True
ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///exchange.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "".join([chr(random.randint(65, 92)) for _ in range(50)])
