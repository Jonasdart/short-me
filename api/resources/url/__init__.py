from flask import request
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from modules.db.mysql import Database
from commons import validate_short_url, new_short_url
from commons.errors import DuplicatedEntryError

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
            'URLs': dbReturn
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
        
        if not response: raise NotFound
        response = validate_short_url(response[0])
        
        return response
        
    
    def post(self):
        data = request.get_json()
        
        parameters = {
                'name': data['URLName'],
                'requested_name': data.get('requestedName'),
            }
        
        if data.get('dateOfExpire'):
            parameters['expire_at'] = data.get('dateOfExpire')
        
        while True:
            try:
                parameters['short_name'] = new_short_url(data['URLName'])
            
                query = Database().parameters_parse(
                    path.join(
                        'api', 'commons', 'queries', 'new_short_url.sql'
                    ),parameters
                )
            
                Database().execute_with_commit(query)

            except DuplicatedEntryError as e:
                if 'for key \'name\'' in str(e): raise e
                pass
            else:
                break
            
        return {
            'response': 'Endpoint criado com sucesso'
            }, 201