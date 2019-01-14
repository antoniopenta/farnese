

from flask import  Blueprint
from flask_restful import Api



from api.poiApi import RetrivePoiFromCoord


def create_api(app,conf,datasource):
    API_NAME = 'poi'
    api_poi_bp = Blueprint('poi_api', __name__)
    url_prefix = '{prefix}/{name}'.format(prefix=conf.PARAM['URL_PREFIX'], name=API_NAME)
    api_poi = Api(api_poi_bp, prefix=url_prefix)
    api_poi.add_resource(RetrivePoiFromCoord, '/poifromcoord',resource_class_kwargs={'datasource': datasource,'conf':conf})
    app.register_blueprint(api_poi_bp)

