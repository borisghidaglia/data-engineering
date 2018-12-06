# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import Attraction, AttractionReview, Review, User
from ..utils import get_d_values, get_g_values, TripadvisorMongoDB

class TripadvisorAttractionSpider(Spider):
    """ Crawl all the attractions indexed by their d_values in the file data.py

    The g_values_to_crawl object could be a list of int, a range() of some value or anything else as long as
    it's iterable and contains int
    """
    name='tripadvisor_attraction'
    allowed_domains = ['tripadvisor.fr']

    def start_requests(self):
        for i in get_g_values():
            link = "https://tripadvisor.fr/Attraction_Review-g%s"%i
            yield Request(link, callback=self.parse_attractions, meta={ 'g_value':i })

    def parse_attractions(self, response):
        name = response.xpath('//*[@id="HEADING"]/text()').extract()[0]\
            .replace(' : les meilleures activités', '')\
            .replace('\n', '')\
            .replace('\u200e', '')
        g_value = response.meta['g_value']
        yield Attraction(
            name = name,
            g_value = g_value
        )


class TripadvisorAttractionReviewSpider(Spider):
    name='tripadvisor_attraction_review'
    allowed_domains = ['tripadvisor.fr']

    def __init__(self, category=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attractions = TripadvisorMongoDB().get_collection('tripadvisor_attraction')

    def start_requests(self):
        """ For each attraction in database, start crawling the attraction_review indexed by their
        d_values in the "d_values_by_attraction.json" file
        """
        for attraction in self.attractions:
            d_values = get_d_values(attraction['name'])
            if d_values:
                for d_value in d_values:
                    link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s"%(attraction['g_value'], d_value)
                    yield Request(
                        link,
                        callback = self.parse_attraction_review,
                        meta = {
                            'g_value' : attraction['g_value'],
                            'd_value' : d_value
                        }
                    )

    def parse_attraction_review(self, response):
        name = response.xpath('//*[@id="HEADING"]/text()').extract()[0]
        yield AttractionReview(
            name = name,
            g_value = response.meta['g_value'],
            d_value = response.meta['d_value']
        )


class TripadvisorReviewSpider(Spider):
    name = 'tripadvisor_review'
    allowed_domains = ['tripadvisor.fr']

    def __init__(self, category=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.users = TripadvisorMongoDB().get_collection('tripadvisor_user')

    def start_requests(self):
        for user in self.users:
            link = "https://www.tripadvisor.fr/Profile/%s"%(user['username'])
            yield Request(
                link,
                callback=self.parse_review,
                meta={'username' : user['username']}
            )

    def parse_review(self, response):
        review_ids = [ review_id.split('-')[3].replace('r','') for review_id in response\
            .xpath('//*[@class="social-sections-ReviewSection__review_wrap--1Gzlk"]/a/@href')\
            .extract()]
        titles = response.xpath('//*[@class="social-sections-ReviewSection__title--HIMCX"]/text()')\
            .extract()
        contents = response.xpath('//*[@class="social-sections-ReviewSection__quote--1AUX1"]/text()')\
            .extract()
        grades = [ int(grade.replace('ui_bubble_rating bubble_', '')) for grade in response\
            .xpath('//*[contains(@class,"ui_bubble_rating ")]/@class').extract()]
        attraction_review_names = [ attraction_review_name.replace('ui_bubble_rating bubble_', '') for attraction_review_name in response\
            .xpath('//*[contains(@class,"social-common-POIObject__poi_name--39wh4")]/text()').extract()]
        attraction_review_gs_ds = ['-'.join(attraction_review_g_d.split('-')[1:3]) for attraction_review_g_d\
            in response.xpath('//*[@class="social-sections-POICarousel__item--1Sbpp"]/div/a/@href')\
            .extract()]
        username = response.meta['username']

        for review_id, title, content, grade, attraction_review_name, attraction_review_g_d\
            in zip(review_ids, titles, contents, grades, attraction_review_names, attraction_review_gs_ds):
            return Review(
                review_id = review_id,
                title = title,
                content = content,
                grade = grade,
                attraction_review_name = attraction_review_name,
                attraction_review_g_d = attraction_review_g_d,
                username = username
            )


class TripadvisorUserSpider(Spider):
    name = 'tripadvisor_user'
    allowed_domains = ['tripadvisor.fr']

    def __init__(self, category=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attraction_reviews = TripadvisorMongoDB().get_collection('tripadvisor_attraction_review')

    def start_requests(self):
        for attraction_review in self.attraction_reviews:
            link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s"%(attraction_review['g_value'], attraction_review['d_value'])
            yield Request(
                link,
                callback=self.parse_review_pages,
                meta={'attraction_review' : attraction_review}
            )

    def parse_review_pages(self, response):
        attraction_review = response.meta['attraction_review']
        nb_pages = int(response.xpath('//*[@id="taplc_location_reviews_list_resp_ar_responsive_0"]/div/div[15]/div/div/div/a[8]/text()').extract()[0])
        for i in range(nb_pages):
            link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s-Reviews-or%s-Eiffel_Tower-Paris_Ile_de_France.html"\
                %(attraction_review['g_value'], attraction_review['d_value'], i*10)
            yield Request(
                link,
                callback=self.parse_uid_and_src,
                meta = { 'attraction_review_name' : attraction_review['name'] }
            )

    def parse_uid_and_src(self, response):
        html_ids = response.xpath('//*[@class="member_info"]/div/@id').extract()

        for html_id in html_ids:
            [uid, src] = html_id.replace('UID_','').replace('SRC_','').split('-')
            link = "https://www.tripadvisor.fr/MemberOverlay?uid=%s&src=%s"%(uid, src)
            yield Request(
                link,
                callback = self.parse_user,
                meta = {
                    'uid' : uid,
                    'src' : src,
                    'attraction_review_name' : response.meta['attraction_review_name']
                }
            )

    def parse_user(self, response):
        username = response.xpath('//*[contains(@class,"memberOverlayRedesign")]/a/@href').extract()[0]\
            .replace('/Profile/', '')
        nb_contributions = response.xpath('//*[@class="countsReviewEnhancements"]/li[1]/span[2]/text()').extract()[0]\
            .replace('\xa0contributions','')
        nb_cities_visited = response.xpath('//*[@class="countsReviewEnhancements"]/li[2]/span[2]/text()').extract()[0]\
            .replace('\xa0villes visitées', '')

        return User(
            username = username,
            uid = response.meta['uid'],
            src = response.meta['src'],
            nb_contributions = nb_contributions,
            nb_cities_visited = nb_cities_visited,
            attraction_review_name = response.meta['attraction_review_name']
        )
