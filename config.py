import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-example")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_ROOT = "https://api.jamendo.com/v3.0/"
try:
    API_CLIENT_ID = os.environ.get("API_CLIENT_ID")

    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
except Exception:
    raise EnvironmentError("Не обнаружено API_CLIENT_ID и/или TG_BOT_TOKEN")
