
import sys
import config
from flask_cors import CORS
from flask import Flask
from application import create_api
from datasource.PostgresDataSources import PostgresDataSources
import os

# get the configuration
conf = config.Config()
# get the db instance
datasource = PostgresDataSources(conf)
# get the application
app = Flask(__name__)



# run the application

def load_app(cfg_file):
    conf.loadconfig(cfg_file)
    CORS(app)
    create_api(app, conf, datasource)
    # Bind to PORT if defined, otherwise default to 5000.
    return app
