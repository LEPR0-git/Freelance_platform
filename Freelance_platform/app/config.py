import os
from dotenv import load_dotenv

# chargement du env

load_dotenv()


class config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'lepro1234'

    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
