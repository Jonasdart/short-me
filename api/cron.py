from datetime import datetime
from time import sleep
from modules.db.mysql import Database

while True:
    try:
        Database().execute_with_commit(f'delete from urls where expire_at <= NOW()')
        sleep(10)
    except Exception as e:
        print(e)