from flask import jsonify, render_template
from . import app
from os.path import abspath

# The databases are based over there because I first developped tripadvisor_crawler,
# and then I integrated it into this flask project.
from tripadvisor_crawler.utils import TripadvisorMongoDB
db = TripadvisorMongoDB()

@app.route('/')
def home():
    reviews = db.lazy_load('tripadvisor_review')
    col_1 = reviews[::3]
    col_2 = reviews[1::3]
    col_3 = reviews[2::3]
    return render_template(
        'main/home.html',
        col_1=col_1,
        col_2=col_2,
        col_3=col_3
    )

@app.route('/api/fetch-raw-reviews/<begin_at>')
def fetch_raw_reviews(begin_at=0):
    reviews = db.lazy_load('tripadvisor_review', begin_at=int(begin_at))
    return jsonify(reviews)
