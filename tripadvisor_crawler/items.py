# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Attraction(scrapy.Item):
    # Link to an Attraction :
    # https://www.tripadvisor.fr/Attractions-g{{g_value}}
    # ex : Paris has g_value=187147
    name = scrapy.Field()
    g_value = scrapy.Field()

class AttractionReview(scrapy.Item):
    # Link to an AttractionReview :
    # https://www.tripadvisor.fr/Attraction_Review-g{{g_value}}-d{{d_value}}
    # ex : Eiffel Tower has g_value=187147 and d_value=188151
    name = scrapy.Field()
    g_value = scrapy.Field()
    d_value = scrapy.Field()

class Review(scrapy.Item):
    review_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    grade = scrapy.Field()
    attraction_review_name = scrapy.Field()
    attraction_review_g_d = scrapy.Field()
    username = scrapy.Field()


class User(scrapy.Item):
    username = scrapy.Field()
    uid = scrapy.Field()
    src = scrapy.Field()
    nb_contributions = scrapy.Field()
    nb_cities_visited = scrapy.Field()
    attraction_review_name = scrapy.Field()
