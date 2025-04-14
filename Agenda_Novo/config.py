
import json
import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # App Config - the minimal footprint
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_9999')

    APP_NAME = "wilson"


    with open("data/menu.json", 'r') as f:
        content = f.read()
        contexto = json.loads(content)    
    SIDEBAR = contexto['itens'] 