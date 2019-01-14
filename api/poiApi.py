
import json
from flask import request, Response
from flask_restful import Resource
from datasource.DAOPoi import DAOPoi
from geojson import Feature, Point,FeatureCollection




class RetrivePoiFromCoord(Resource):

    def __init__(self, datasource,conf):
        self.datasource = datasource
        self.conf = conf

    def post(self):
        postdata = request.get_json()
        if not self.validate(postdata):
             return Response(response = "{error:'the input data are incorrect'}",
                             status = 400,
                             mimetype= "application/json")
        dat = self.process(postdata)
        resp = Response(response=dat,
                        status=201, \
                        mimetype="application/json")
        return (resp)

    def validate(self, data):
        if set(data.keys()) == {'lat','lng','radius'}:
            return True
        else:
            return False

    def process(self,jsondata):
        # pointLowLeft
        # pointUpRight
        lat = jsondata['lat']
        lng = jsondata['lng']
        radius = jsondata['radius']
        dao = DAOPoi(self.datasource, self.conf)

        l_anemity = dao.retrieve_anemity_circle_lng_lat( lng, lat, radius)
        if self.conf.PARAM['DEBUG']:
            print('Retrived Anemity')
            print(l_anemity)
        #list_type_anemity = [ item.value for item in l_anemity ]



        list_geo_features_word = []
        for index, model in enumerate(l_anemity):
            geodata = Point((model.lng, model.lat))
            list_geo_features_word.append(Feature(geometry=geodata, id=index, properties={'value': model.value}))

        geojson = FeatureCollection(list_geo_features_word)

        # this will return a counter too
        #dict_value = Counter(list_type_anemity)
        #json.dumps({'geojson': geojson, 'counter': dict(dict_value)})

        return json.dumps(geojson)
