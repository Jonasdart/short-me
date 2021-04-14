import os

from flask import Flask, g
import json

def create_app(test_config=None):
    # create and configure the app
    myapp = Flask(__name__, instance_relative_config=True)
    myapp.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(myapp.instance_path, 'dcommercial.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        myapp.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        myapp.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(myapp.instance_path)
    except OSError:
        pass

    from . import db, app
    
    myapp.register_blueprint(app_auth.bp)
    myapp.register_blueprint(app.bp)
    db.init_app(myapp)
           

    return myapp