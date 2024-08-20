import os
from flask import Flask, render_template

def create_app(test_config=None):
    '''
        Creating and configuring the application
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cimis_flask.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    '''
        Routes used for this application
    '''
    @app.route('/')
    def index():
        return render_template('home.html')

    from . import weather_data
    app.register_blueprint(weather_data.bp)

    '''
        Initialize the database for the application
    '''
    from . import db
    db.init_app(app)

    return app
