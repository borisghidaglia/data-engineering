from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from tripadvisor_crawler.utils import TripadvisorMongoDB
mongo = TripadvisorMongoDB()

class ElasticsearchDB():

    def __init__(self, *args, **kwargs):
        self.client = Elasticsearch()
        bulk(self.client, self.bulk_index_mongo('tripadvisor_user'))
        bulk(self.client, self.bulk_index_mongo('tripadvisor_review'))

    def bulk_index_mongo(self, index):
        data = list(mongo.db[index].find())
        for elt in data:
            doc_id = str(elt['_id'])
            del elt['_id']
            obj = {
                "_index" : index,
                "_type" : index+"_document",
                "_id" : doc_id,
                "_source" : elt
            }
            yield obj

    def test(self):
        query = {
            "query": {
               "regexp": { "username": ".*fran.*"} 
            }
        }
        res = self.client.search(index="tripadvisor_user", body=query)
        print(res)
        return res
