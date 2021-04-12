from flask import request
from flask_restful import Resource
from modules.db.mysql import Database

from os import path
from datetime import datetime

import json

class Url(Resource):
    def __init__(self):
        self.header = [
            'URLName', 'requestedName', 'shortName', 'createdAt', 'expireAt'
        ]
        
    def get(self):        
        try:
            dbReturn = Database().execute_with_return('select * from urls', True, self.header)
        except:
            raise
        
        return {
            'response': dbReturn
            }, 200
        
    
    def _get(self, url):
        query = Database().parameters_parse(
            path.join(
                'api', 'commons', 'queries', 'get_full_url.sql'
            ),{
                'shortName': url
            }
        )
        response = Database().execute_with_return(query, True, self.header)
        
        return response
        
    
    def post(self):
        data = request.get_json()
        
        parameters = {
                'name': data['URLName'],
                'requested_name': data.get('requestedName'),
                'short_name': 'teste'
            }
        
        if data.get('dateOfExpire'):
            parameters['expire_at'] = data.get('dateOfExpire')
        
        query = Database().parameters_parse(
            path.join(
                'api', 'commons', 'queries', 'new_short_url.sql'
            ),parameters
        )
        
        print(query)
        
        Database().execute_with_commit(query)
        
        return {
            'response': 'Endpoint criado com sucesso'
            }, 200