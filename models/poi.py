

class BasePOI:

    def __init__(self, lat, lng,value):
        self.lat = lat
        self.lng = lng
        self.value = value


    def __repr__(self):
        return ','.join(list(map(str, (self.lat, self.lng, self.value))))


# models realted to the db tables
class Anemity(BasePOI):

    def __init__(self, lat, lng, anemity_type, name):
        BasePOI.__init__(self, lat, lng, anemity_type)
        self.name = name

    def __repr__(self):
        return ','.join(list(map(str, (self.lat, self.lng, self.value, self.name))))

