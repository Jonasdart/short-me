#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3


class DatabaseConnectionError(Exception):
    def __str__(self):
        return 'Erro de conexão ao banco de dados'