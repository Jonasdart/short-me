import os
import json
import unittest

from time import sleep
from datetime import datetime

from modules.db.oracle import Database

TODAY = datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M-%S')
class Case1(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        try:
            os.makedirs(f'results/{TODAY}')
        except:pass


    def test_1_execute_with_return_as_list(self):
        query = self.db.parameters_parse('queries/test_with_return.sql')
        retorno = self.db.execute_with_return(query, return_dict=False)
        
        with open(f'results/{TODAY}/{self._testMethodName}.json', 'w') as log:
            log.write(
                json.dumps(
                    retorno,
                    indent=2
                )
            )
    
    
    def test_2_execute_with_return_as_dict(self):
        query = self.db.parameters_parse('queries/test_with_return.sql')
        retorno = self.db.execute_with_return(query)
        
        with open(f'results/{TODAY}/{self._testMethodName}.json', 'w') as log:
            log.write(
                json.dumps(
                    retorno,
                    indent=2
                )
            )


    def test_3_execute_without_commit(self):
        raise NotImplementedError


    def test_4_execute_with_commit(self):
        raise NotImplementedError
       

unittest.main()


