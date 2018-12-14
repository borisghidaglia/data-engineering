from flask import jsonify, render_template
from . import app
from os.path import abspath

# The database Mongo is based over there because I first developped tripadvisor_crawler,
# and then I integrated it into this flask project.
from tripadvisor_crawler.utils import TripadvisorMongoDB
from main.elasticsearch_models import ElasticsearchDB

db_mongo = TripadvisorMongoDB()
db_elastic = ElasticsearchDB()

# Main routes
@app.route('/')
def home():
    reviews = db_mongo.lazy_load('tripadvisor_review')
    col_1 = reviews[::3]
    col_2 = reviews[1::3]
    col_3 = reviews[2::3]
    return render_template(
        'main/home.html',
        col_1=col_1,
        col_2=col_2,
        col_3=col_3
    )

@app.route('/search')
def search():
    data = db_elastic.test()
    return render_template(
        'main/search.html',
        data = data
    )



# API routes
@app.route('/api/fetch-raw-reviews/<begin_at>')
def fetch_raw_reviews(begin_at=0):
    reviews = db_mongo.lazy_load('tripadvisor_review', begin_at=int(begin_at))
    return jsonify(reviews)
