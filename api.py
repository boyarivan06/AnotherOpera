import json

from requests import get

from config import API_ROOT


def get_songs():
    res = get(API_ROOT).text
    print(res)
    return json.loads(res)