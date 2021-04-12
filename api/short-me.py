from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import NotFound

from resources import Url

import json


app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/<short_url>')
def redirect_to_short_url(short_url):
    if short_url == 'favicon.ico': raise NotFound
    
    return json.dumps(
        Url()._get(short_url), indent=2
    )

api.add_resource(Url, '/url')

app.run(debug=True)