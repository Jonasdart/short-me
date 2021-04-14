import os

os.system('set FLASK_APP=dcommercial')
os.system('set FLASK_ENV=development')
os.system('flask run -h 0.0.0.0 -p 8000 --reload')