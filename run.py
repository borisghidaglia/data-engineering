import jinja2
from main import app as main_app

if __name__ == '__main__':
    apps = [main_app]
    for app in apps:
        my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(['templates']),
        ])
        app.jinja_loader = my_loader
        app.static_folder = '../static'
        app.run('0.0.0.0')
