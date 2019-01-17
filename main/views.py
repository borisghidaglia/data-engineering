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
    """Returns the homepage prefilled with the first few reviews of the database,
    the rest can be fetched by the client using js and api function `fetch_raw_reviews` """
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
    data = db_elastic.autocomplete_username(query="")
    return render_template(
        'main/search.html',
        data = data
    )

@app.route('/grade-hist')
def grade_hist():
    """Returns the template, the plotting happens in js on the client's side"""
    return render_template('plotting.html')


# API routes
@app.route('/api/fetch-raw-reviews/<begin_at>')
def fetch_raw_reviews(begin_at=0):
    """Returns first 10 reviews following the `begin_at` index """
    reviews = db_mongo.lazy_load('tripadvisor_review', begin_at=int(begin_at))
    return jsonify(reviews)

@app.route('/api/fetch-users-autocomplete/<query>')
def fetch_user_autocomplete(query):
    data = db_elastic.autocomplete_username(query)
    return jsonify(data)

@app.route('/api/fetch-review-autocomplete/<query>')
def fetch_review_autocomplete(query):
    data = db_elastic.autocomplete_review(query)
    return jsonify(data)

@app.route('/api/all-reviews')
def get_all_reviews():
    all_reviews = db_mongo.db['tripadvisor_review'].find(None,{'_id':False})
    return jsonify(list(all_reviews))


@app.route('/api/grades')
def get_grades():
    """Returns a list of all reviews grades"""
    grades = db_mongo.db['tripadvisor_review'].find(None, {'grade': True, '_id':False})
    grade_list = [grade_dict['grade'] for grade_dict in grades]

    return jsonify(grade_list)
    # return jsonify(dict(grades))
