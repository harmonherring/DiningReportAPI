import os

IP = os.environ.get("DININGREPORT_IP", '127.0.0.1')
PORT = os.environ.get("DININGREPORT_PORT", 8080)
SERVER_NAME = os.environ.get("DININGREPORT_SERVER_NAME", 'diningreport-api.csh.rit.edu')

# SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DININGREPORT_DATABASE_URI")

# Socrata
SOCRATA_DATASET_ID = os.environ.get("DININGREPORT_DATASET_ID", None)
SOCRATA_APP_TOKEN = os.environ.get("DININGREPORT_APP_TOKEN", None)
