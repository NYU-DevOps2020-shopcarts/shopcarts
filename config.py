import logging
import os

SECRET_KEY = 'secret-for-dev'
LOGGING_LEVEL = logging.INFO

SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///../db/test.db"
)
SQLALCHEMY_DATABASE_URI = DATABASE_URI
