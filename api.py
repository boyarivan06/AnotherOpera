import json

from requests import get, post, delete
from models.sqlalch_models import Song
from config import API_ROOT


def get_songs():
    res = get(API_ROOT).text
    return json.loads(res)


def get_song_by_args(**kwargs) -> Song:
    # request_json = json.dumps(kwargs)
    resp = get(API_ROOT+'/song', kwargs)
    data = json.loads(resp.text)
    return Song.load(data)


def new_song(song: Song) -> int:
    resp = post(API_ROOT+'/song', data=song.get_dict())
    return resp.status_code

def delete_song(song: Song) -> int:
    resp = delete(API_ROOT+'/song', data=song.get_dict())
    return resp.status_code