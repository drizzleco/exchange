import random, os

DEBUG = True
PORT = os.getenv("PORT") or 8080
ORIGINS = ["http://localhost:" + str(PORT), "http://127.0.0.1:" + str(PORT)]


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///exchange.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or "".join(
        [chr(random.randint(65, 92)) for _ in range(50)]
    )
