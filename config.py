import os
from dotenv import load_dotenv, dotenv_values

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
MEDIA_ROOT = os.path.join(os.getcwd(), 'media/')

API_ROOT = 'https://api.jamendo.com/v3.0/'

# SECRET_KEY = dotenv_values()['SECRET_KEY']
API_CLIENT_ID = 'e6ffd643'
