#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3

import MySQLdb as db
import os

from datetime import datetime

# Import dos utilitários comuns
from modules.db.commons.errors import DatabaseConnectionError


class Database():
    """
        Connection with oracle database and query parser.

        :methods: 
            commit_with_return -> To get items of database
            commit_without_return -> To input items in database
    """
    def __init__(self):
        self.connected = False
        
    
    def _getConnection(self):
        if not self.connected:
            credencials = self.__authenticate()
            address = credencials.get('DatabaseAddress')
            name = credencials.get('DatabaseName')
            user = credencials.get('DatabaseUser')
            password = credencials.get('DatabaseUserPass')
        
            try:
                self.bank = db.connect(address, user, password, name)
            except:
                self.conected = False
                raise
            else:
                self.cursor = self.bank.cursor()
                self.conected = True

        return {
            'Database' : self.bank,
            'Cursor'   : self.cursor
        }
    
    def _closeConnection(self, database):
        if self.connected:
            try:
                database.close()
            except:
                raise Exception('Database connection not initialized')
        
        self.conected = False
        return True

    
    def __authenticate(self):
        '''
        Retorna as informações presentes nas variáveis de ambiente
        em forma de json

        Retorno -> dict
        '''
        
        return {
            'DatabaseAddress' : 'localhost',
            'DatabasePort' : '3306',
            'DatabaseName' : 'short-me-api',
            'DatabaseUser' : 'root',
            'DatabaseUserPass' : ''
        }
        #return {
        #    'DatabaseAddress' : os.environ['DB_HOST'],
        #    'DatabasePort' : os.environ['DB_PORT'],
        #    'DatabaseName' : os.environ['DB_NAME'],
        #    'DatabaseUser' : os.environ['DB_USER'],
        #    'DatabaseUserPass' : os.environ['DB_PASS']
        #}


    def execute_without_commit(self, query, cursor=None):
        """
        EN: 
            On the first call, the cursor parameter must not be passed because it will be returned, 
                next to the database commit caller.

            On the next calls, the cursor parameter must be informed. 
                To finish statement, call the 'commit' key in first response.
        
        PTBR:
            Na primeira chamada da função, o parâmetro cursor não deve ser informado porque é retornado 
                um cursor e o caller do commit ao pool de conexões.

            Nas próximas chamadas, o parâmetro cursor deve ser informado. 
                Para terminar a instrução, chame a chave 'commit' na primeira resposta. 

        :param query: Recebe uma string contendo a query a ser executada.
        :param parameters: Recebe o conjunto de chave e valor dos parâmetros, 
            onde chave é o parâmetro citado na query e valor o que será atribuído ao mesmo.
        :param cursor: None ou cursor de conexão.
        :return: dict -> Na primeira chamada 'commmit' e 'cursor' nas outras somente 'cursor'
        """ 
        toReturn = {}

        if not cursor:
            database, cursor = self._getConnection().values()
            toReturn['commit'] = database.commit
            
        try:
            cursor.execute(query)
        except:
            raise
        else:
            toReturn['cursor'] = cursor
        
        return toReturn


    def execute_with_commit(self, query):
        """
        :param query: Recebe uma string contendo a query a ser executada.
        :param parameters: Recebe o conjunto de chave e valor dos parâmetros, 
            onde chave é o parâmetro citado na query e valor o que será atribuído ao mesmo.
        :return: True
        """        
        database, cursor = self._getConnection().values()
        try:
            cursor.execute(query)
        except:
            raise
        else:
            database.commit()
            self._closeConnection(database)

        return True


    def execute_with_return(self, query, return_dict=False, header=None):
        """
        :param query: Recebe uma string contendo a query a ser executada.
        :param parameters: Recebe o conjunto de chave e valor dos parâmetros, 
            onde chave é o parâmetro citado na query e valor o que será atribuído ao mesmo.
        :param return_dict: True or False
            Se True, retorna um conjunto de chave e valor com os nomes de colunas do retorno.
            Se False, retorna um array de itens, sem chave, somente valores
        :return: dict or list or None
        """
        results = None
        database, cursor = self._getConnection().values()
        try:
            cursor.execute(query)
        except:
            raise
        else:
            response = cursor.fetchall()
            if return_dict:
                tempResponse = []
                for data in response:
                    info_results = {}
                    x = 0
                    for minorData in data:
                        if isinstance(minorData, datetime):
                            minorData = datetime.strftime(minorData, '%d-%m-%Y %H:%M:%S')
                        elif minorData != None:
                            minorData = str(minorData)
                        info_results[header[x]] = minorData
                        x += 1
                    tempResponse.append(info_results)

                response = tempResponse
            
            self._closeConnection(database)

        return response

    
    def parameters_parse(self, query, parameters={}):
        """
        :param query: string contendo o caminho do arquivo da query
        :param parameters: [Opcional] dicionário contendo os parâmetros que serão feitos replace.
        """
        
        print(parameters)
        try:
            with open(query, 'r') as sql:
                query = " ".join(sql.read().split())
                
            for parameter in parameters.keys():
                query = query.replace('{'+parameter+'}', str(parameters[parameter]))
        except:
            raise
        return query
