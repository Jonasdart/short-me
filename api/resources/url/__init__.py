from flask import request
from flask_restful import Resource
from flask_api_cache import ApiCache
from werkzeug.exceptions import NotFound
from modules.db.mysql import Database
from commons import validate_url, validate_short_url, new_short_url
from commons.errors import DuplicatedEntryError

from os import path
from datetime import datetime

class Url(Resource):
    def __init__(self):
        self.header = [
            'URLName', 'requestedName', 'shortName', 'createdAt', 'expireAt'
        ]
        
        
    @ApiCache(expired_time=10)
    def get(self):        
        try:
            dbReturn = Database().execute_with_return('select * from urls', True, self.header)
        except:
            raise
        
        return {
            'URLs': dbReturn
            }, 200
        
        
    @ApiCache(expired_time=10)
    def _get(self, url):
        validate_url(url, prefix=False)
        
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
        try:
            data = request.get_json()
            
            validate_url(data['URLName'])
            
            parameters = {
                    'name': data['URLName'],
                    'requested_name': data.get('requestedName'),
                }
            
            if data.get('dateOfExpire'):
                parameters['column_expire_at'] = ', expire_at'
                parameters['value_expire_at'] = f', \'{data.get("dateOfExpire")}\''
            else:
                parameters['column_expire_at'] = ''
                parameters['value_expire_at'] = ''
            
            while True:
                try:
                    if not data.get('requestedName'):
                        parameters['short_name'] = new_short_url(data['URLName'])
                    else:
                        parameters['short_name'] = '-'.join(data['requestedName'].lower().split(' '))
                
                    query = Database().parameters_parse(
                        path.join(
                            'api', 'commons', 'queries', 'new_short_url.sql'
                        ),parameters
                    )
                    Database().execute_with_commit(query)

                except DuplicatedEntryError as e:
                    if 'for key \'name\'' in str(e):
                        shortUrl, expireAt = Database().execute_with_return(
                            f'select short_name, expire_at from urls where name=\'{data["URLName"]}\''
                        )[0]
                        
                        return {
                            'response': 'Esta URL já possui uma versão encurtada!',
                            'shortUrl': shortUrl,
                            'expireAt': datetime.strftime(expireAt, '%d-%m-%Y %H:%M:%S')
                        }, 303
                        
                    data['requestedName'] = None
                    
                else:
                    break
        except AssertionError:
            return {
                'response': 'Verifique os parâmetros!'
            }, 401
                
        return {
            'response': 'Endpoint criado com sucesso',
            'shortURL': parameters['short_name']
            }, 201