from flask import render_template
from . import app
from os.path import abspath

@app.route('/')
def home():

    return render_template('main/home.html')

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
