#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3

try:
    from modules.config.parser import ConfigParser
except ImportError:
    raise ImportError('Instale o utilitário Config Parser ->\ngit clone https://gitlab.com/jamef-developer/modules/config-parser.git modules/config')

import cx_Oracle as db
import os


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
        self.inPool = False
        
    
    def _make_dsn(self, credencials):
        address = credencials.get('DatabaseAddress')
        port = credencials.get('DatabasePort')
        name = credencials.get('DatabaseName')

        self.dsn = db.makedsn(address,
                        port,
                        service_name=name
                    )

        return self.dsn

    
    def _make_connection_pool(self):
        if not self.inPool:
            configs = ConfigParser().read('global')
            configs = configs['db']['oracle']

            credencials = configs.get('connection')
            if not credencials:
                credencials = self.__authenticate()

            self._make_dsn(credencials)

            user = credencials.get('DatabaseUser')
            password = credencials.get('DatabaseUserPass')
            try:
                self.connectionPool = db.SessionPool(user,
                    password,
                    dsn=self.dsn,
                    min=configs['minPool'], 
                    max=configs['maxPool'], 
                    increment=configs['increment'],
                    threaded=configs['threaded']
                )
            except:
                self.inPool = False
                raise
            else:
                self.inPool = True

        return self.connectionPool

    
    def __clearPool(self):
        self.connectionPool.close()
        self.inPool = False


    def _getConnection(self):
        try:
            database = self._make_connection_pool().acquire()
        except:
            raise
        else:
            cursor = database.cursor()
        return {
            'Database' : database,
            'Cursor'   : cursor
        }

    
    def _closeConnection(self, database):
        try:
            self.connectionPool.release(database)
        except:
            raise DatabaseConnectionError('Database connection not initialized')
        
        return True

    
    def __authenticate(self):
        '''
        Retorna as informações presentes nas variáveis de ambiente
        em forma de json

        Retorno -> dict
        '''
        
        return {
            'DatabaseAddress' : os.environ['DB_HOST'],
            'DatabasePort' : os.environ['DB_PORT'],
            'DatabaseName' : os.environ['DB_NAME'],
            'DatabaseUser' : os.environ['DB_USER'],
            'DatabaseUserPass' : os.environ['DB_PASS']
        }

    
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


    def execute_with_return(self, query, return_dict=True):
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
            if return_dict:
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))

            results = cursor.fetchall()
            
            self._closeConnection(database)

        return results

    
    def parameters_parse(self, query, parameters={}):
        """
        :param query: string contendo o caminho do arquivo da query
        :param parameters: [Opcional] dicionário contendo os parâmetros que serão feitos replace.
        """
        try:
            with open(query, 'r') as sql:
                query = " ".join(sql.read().split())
                
            for parameter in parameters.keys():
                query = query.replace('{'+parameter+'}', parameters[parameter])
        except:
            raise
        return query