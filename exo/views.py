from . import exo_app

@exo_app.route('/')
def hello():
    return 'Home page'

@exo_app.route('/login')
def hello():
    return 'Login Page'

@exo_app.route('/help')
def hello():
    return 'Help Page'

@exo_app.route('/root')
def hello():
    return 'Root Page'

@exo_app.route('/stats')
def hello():
    return 'Dashboard Page'
