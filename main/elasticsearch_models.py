from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from tripadvisor_crawler.utils import TripadvisorMongoDB
mongo = TripadvisorMongoDB()

class ElasticsearchDB():

    def __init__(self, *args, **kwargs):
        self.client = Elasticsearch("http://elastic:9200")
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

    def autocomplete_username(self, query):
        # https://www.elastic.co/guide/en/elasticsearch/guide/current/_query_time_search_as_you_type.html#
        query = {
            "size" : 30,
            "query" : {
                "match_phrase_prefix" : {
                    "username" : {
                        "query": query,
                        "max_expansions": 5
                    }
                }
            }
        }
        res = None
        if self.client.indices.exists(index="tripadvisor_user"):
            res = self.client.search(index="tripadvisor_user", body=query, filter_path=['hits.hits'])
        return res

    def autocomplete_review(self, query):
        # multi_match : https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
        # fuzziness : https://stackoverflow.com/questions/29632339/elasticsearch-multi-match-query-over-multiple-fields-with-fuzziness
        query = {
            "size" : 30,
            "query" : {
                "multi_match" : {
                    "fields" : ["title^10", "content", "attraction_review_name^5", "username^10"],
                    "query" : query,
                    # "type" : "phrase_prefix",
                    "max_expansions": 50,
                    "fuzziness": "AUTO",
                    "prefix_length" : 2
                }
            }
        }
        res = None
        if self.client.indices.exists(index="tripadvisor_review"):
            res = self.client.search(index="tripadvisor_review", body=query, filter_path=['hits.hits'])
        return res
