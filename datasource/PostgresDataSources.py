

import psycopg2


class PostgresDataSources:

    def __init__(self, conf):
        self.conf = conf
        self.conn = None

    def create_connection(self):

        try:
            string_connection = "dbname='%s' user='%s' host='%s' password='%s'" % \
                                                    (self.conf.PARAM['DBNAME'], self.conf.PARAM['USER'],
                                                     self.conf.PARAM['SERVER_DB'], self.conf.PARAM['PWD'])
            if self.conf.PARAM['DEBUG']:
                print("String_connection:  " + string_connection)

            self.conn = psycopg2.connect(string_connection)

        except Exception as e:
            raise ValueError('The connection is not created '+str(e))

    def get_connection(self):
        if self.conn is None:
            raise ValueError('The connection is not created yet ')
        return self.conn

    def close_connection(self):
        if self.conn is None:
            raise ValueError('The connection is not created yet')
        try:
            self.conn.close()
        except Exception as e:
            raise ValueError('Connection is not closed properly')

    def commit(self):
        if self.conn is None:
            raise ValueError('The connection is not created yet')
        try:
            self.conn.commit()
        except Exception as e:
            raise ValueError('The commit is not done properly '+str(e))
