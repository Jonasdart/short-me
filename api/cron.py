from datetime import datetime
from time import sleep
from modules.db.mysql import Database

while True:
    try:
        thisMoment = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S')
        Database().execute_with_commit(f'delete from urls where expire_at <= \'{thisMoment}\'')
        sleep(3600)
    except Exception as e:
        print(e)