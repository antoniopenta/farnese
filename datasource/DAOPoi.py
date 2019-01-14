

from models.poi import Anemity
import psycopg2


# this class is used to retrieve POI from the database
class DAOPoi:

    def __init__(self, data_source, conf):
        self.data_source = data_source
        self.conf = conf

    def retrieve_anemity_bb_lowleft_upright_lng_lat(self, bb):
        try:
            self.data_source.create_connection()
            conn = self.data_source.get_connection()
            point_low_left_lng = str(bb[0][0])
            point_low_left_lat = str(bb[0][1])
            point_up_right_lng = str(bb[1][0])
            point_up_right_lat = str(bb[1][1])
            string_query = "SELECT * from poi.anemity " \
                           "WHERE ST_Contains( " \
                           "ST_SetSRID( ST_MakeBox2D(" \
                           "ST_Point(%s,%s)," \
                           "ST_Point(%s,%s)),4326), geom4326)" % (point_low_left_lng,
                                                                  point_low_left_lat,
                                                                  point_up_right_lng,
                                                                  point_up_right_lat)
            if self.conf.PARAM['DEBUG']:
                print("Query:  "+string_query)
            cur = conn.cursor()
            cur.execute(string_query)
            rows = cur.fetchall()
            list_anemity = []
            for row in rows:
                #id,lat,lng,anemity_type,name
                an = Anemity(row[1], row[2], row[3], row[4])
                list_anemity.append(an)
            cur.close()
            self.data_source.close_connection()
            return list_anemity
        except ValueError as e:
            raise ValueError(str(e))
        except psycopg2.Error as e:
            raise ValueError(str(e.pgerror))

    # retrive data within a cirlcle
    def retrieve_anemity_circle_lng_lat(self,lng, lat, radius):
        try:
            self.data_source.create_connection()
            conn = self.data_source.get_connection()
            point_lng = str(lng)
            point_lat = str(lat)
            radius = str(radius)
            string_query = 'SELECT * from poi.anemity WHERE  ' \
                           'ST_DWithin(st_transform(geom4326,26986),' \
                           'st_transform(ST_SetSRID(' \
                           'ST_Point(%s,%s),4326),26986),%s)' % (point_lng, point_lat, radius)
            if self.conf.PARAM['DEBUG']:
                print("Query:  " + string_query)
            cur = conn.cursor()
            cur.execute(string_query)
            rows = cur.fetchall()
            list_anemity = []
            for row in rows:
                # id,lat,lng,anemity_type,name
                an = Anemity(row[1], row[2], row[3], row[4])
                list_anemity.append(an)
            cur.close()
            self.data_source.close_connection()
            return list_anemity
        except ValueError as e:
            raise ValueError(str(e))
        except psycopg2.Error as e:
            raise ValueError(str(e.pgerror))

    def count_anemity_circle_lng_lat_where(self, lng, lat, radius, list_anemity):
        try:
            self.data_source.create_connection()
            conn = self.data_source.get_connection()
            point_lng = str(lng)
            point_lat = str(lat)
            radius = str(radius)

            if len(list_anemity) == 0 or list_anemity is None:
                string_query = 'SELECT count(*) from poi.anemity WHERE  ' \
                               'ST_DWithin(st_transform(geom4326,26986),' \
                               'st_transform(ST_SetSRID(' \
                               'ST_Point(%s,%s),4326),26986),%s) ' % (
                                point_lng, point_lat, radius)
            else:
                string_where = ' or '.join("%s='%s'" % ('amenity_type', j) for j in list_anemity)
                string_query = 'SELECT count(*) from poi.anemity WHERE  ' \
                               'ST_DWithin(st_transform(geom4326,26986),' \
                               'st_transform(ST_SetSRID(' \
                               'ST_Point(%s,%s),4326),26986),%s) and (%s)' % (point_lng, point_lat, radius, string_where)
            if self.conf.PARAM['DEBUG']:
                print("Query:  " + string_query)
            cur = conn.cursor()
            cur.execute(string_query)
            rows = cur.fetchall()
            count = 0
            for row in rows:
                count = row[0]
            cur.close()
            self.data_source.close_connection()
            return count
        except ValueError as e:
            raise ValueError(str(e))
        except psycopg2.Error as e:
            raise ValueError(str(e.pgerror))

