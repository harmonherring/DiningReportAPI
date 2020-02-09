from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sodapy import Socrata

import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
socrata_client = Socrata("health.data.ny.gov", app.config['SOCRATA_APP_TOKEN'])

from dining_report.routes import populate_bp
app.register_blueprint(populate_bp, url_prefix="/populate")
