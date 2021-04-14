import requests, json

URL = 'http://127.0.0.1:5000/auth/user'

def api_login(username, password, company):
    payload = json.dumps({
            'username' : username,
            'senha'    : password,
            'empresa'  : company
        })
        
    headers = {
            'Content-Type': 'application/json'
        }
    try:
        user = requests.request('GET', URL, headers=headers, data=payload)
    except:
        raise
    else:
        if user.status_code >= 400:
            raise user.text 
        
        return json.loads(user.text)