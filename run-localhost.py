
import sys
import config
from flask_cors import CORS
from flask import Flask
from application import create_api
from datasource.PostgresDataSources import PostgresDataSources

# get the configuration
conf = config.Config()
conf.loadconfig(sys.argv[1])


# get the db instance
datasource = PostgresDataSources(conf)

# get the application
app = Flask(__name__)
CORS(app)
create_api(app,conf,datasource)


# run the application
app.run(host=conf.PARAM['APPLICATION_HOST'],debug=conf.PARAM['DEBUG'],port=conf.PARAM['PORT'],use_reloader=False)