from flask import Flask, redirect
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import NotFound

from resources import Url

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/<short_url>')
def redirect_to_short_url(short_url):
    if short_url == 'favicon.ico': raise NotFound
    
    try:
        URLName = Url()._get(short_url)['URLName']
    except AssertionError:
        return {
            'response': 'URL inválida!'
        }, 401
        
    return redirect(
        URLName
    )

api.add_resource(Url, '/urls')

app.run(debug=False)