import random
import string
from datetime import datetime

from werkzeug.exceptions import NotFound


def new_short_url(url):
    letters = string.ascii_letters
    
    __hash = ''.join(random.choice(letters) for _ in range(random.randint(0, 3)))
    __hash += str(random.getrandbits(len(url)))
    __hash = __hash[:5]
    __hash += ''.join(random.choice(letters) for _ in range(random.randint(0, 3)))
    
    return __hash


def validate_url(url):
    assert isinstance(url, str)
    assert ' ' not in url
    
    assert ('\'' or '"') not in url
    assert ('AND' or 'and' and '1') not in url
    assert ('OR' or 'or' and '1') not in url
    
    assert ('SELECT' or 'select' and 'urls') not in url
    assert ('DROP' or 'drop' and 'short-me-api') not in url
    assert ('INSERT' or 'insert' and 'urls') not in url
    assert ('UPDATE' or 'update' and 'urls') not in url
    
    
def validate_short_url(shortURL):
    if datetime.strptime(shortURL['expireAt'], '%d-%m-%Y %H:%M:%S') <= datetime.now():
        raise NotFound
    
    return shortURL
    
    
    