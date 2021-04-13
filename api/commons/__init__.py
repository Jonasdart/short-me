import random
from datetime import datetime

from werkzeug.exceptions import NotFound


def new_short_url(url):
    __hash = str(random.getrandbits(len(url)))
    __hash = __hash[:5]
    
    __hash += url.split('://')[1][:1]
    __hash += str(random.getrandbits(6))
    
    return __hash


def validate_url(url):
    assert isinstance(url, str)
    assert ('https://' or 'http://') in url[:8]
    
    
def validate_short_url(shortURL):
    if datetime.strptime(shortURL['expireAt'], '%d-%m-%Y %H:%M:%S') <= datetime.now():
        raise NotFound
    
    return shortURL
    
    
    