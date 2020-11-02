import logging
import os
import json

SECRET_KEY = 'secret-for-dev'
LOGGING_LEVEL = logging.INFO

SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

SQLALCHEMY_DATABASE_URI = DATABASE_URI
