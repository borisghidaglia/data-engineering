from flask import render_template
from . import app
from os.path import abspath

# The databases are based over there because I first developped tripadvisor_crawler,
# and then I integrated it into this flask project.
from tripadvisor_crawler.utils import TripadvisorMongoDB
db = TripadvisorMongoDB()

@app.route('/')
def home():
    users = db.make_query(collection_name='tripadvisor_review')
    return render_template('main/home.html', users=users)

@app.route('/login')
def login():
    return 'Login Page'

@app.route('/help')
def help():
    return 'Help Page'

@app.route('/root')
def root():
    return 'Root Page'

@app.route('/stats')
def stats():
    return 'Dashboard Page'
