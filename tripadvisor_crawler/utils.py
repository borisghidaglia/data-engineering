import pymongo
import json

# Databases management

class DatabaseMongo:

    def __init__(self, db_name):
        self.db_name =db_name
        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        """Return a collection from database

        Keyword arguments:
        filters -- a dict like so : { key1 : value1, key2 : value2, ..., keyN : valueN }
        """
        return self.make_query(collection_name)

    def make_query(self, collection_name, filters=None):
        """Allows to perform a query on the database

        Keyword arguments:
        filters -- a dict like so : { key1 : value1, key2 : value2, ..., keyN : valueN }
        """
        return self.db[collection_name].find(filters) if filters else self.db[collection_name].find()


class TripadvisorMongoDB(DatabaseMongo):

    def __init__(self, *args, **kwargs):
        super().__init__(db_name='tripadvisor', *args, **kwargs)

# Attractions and Attraction_Review

def get_d_values(attraction_name):
    """Return d_values related to this attraction name

    Returned d_values are fetched from the json 'd_values_by_attraction.json'.
    This file allows to chose specific d_values we want to crawl.

    Keyword arguments:
    attraction_name -- name of the attraction related to the d_values wanted
    """
    try:
        with open('./tripadvisor_crawler/spiders/d_values_by_attraction.json') as file:
            data = json.load(file)
        return data['attraction'][attraction_name]
    except Exception as e:
        raise Exception('Exception : %s -- did you created "d_values_by_attraction.json" ?'%(e))

def get_g_values():
    """Return g_values

    Returned g_values are fetched from the json 'g_values.json'.
    This file allows to chose specific g_values we want to crawl.
    """
    try:
        with open('./tripadvisor_crawler/spiders/g_values.json') as file:
            data = json.load(file)
        return data['g_values']
    except Exception as e:
        raise Exception('Exception : %s -- did you created "g_values.json" ?'%(e))
