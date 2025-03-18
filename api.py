import json
import os
from typing import Any
from json import loads
from requests import get, post, delete
from config import API_ROOT, API_CLIENT_ID
from special import MetaControl, log_action


class APIConnect(metaclass=MetaControl):
    slots = []
    def __init__(self, data):
        for field in self.slots:
            setattr(self, field, data[field])
    @classmethod
    @log_action
    def get_all(cls, limit=10, **kwargs):
        limit = limit if limit >= 10 else 10
        limit = limit if limit <= 200 else 200
        data = {'client_id':API_CLIENT_ID, 'format':'json', 'limit':limit}
        resp = get(API_ROOT + f'/{cls.__name__.lower()}s/', {**data, **kwargs})
        if resp.status_code != 200:
            print('Нет доступа к API, проверьте интернет-соединение и всё такое')
            quit()
        resp_data = loads(resp.text)
        result = []
        if resp_data['headers']['status'] == 'success':
            for elem in resp_data['results']:
                obj = cls(elem)
                result.append(obj)
        return result

    @classmethod
    @log_action
    def get_object_by_name(cls, name):
        # request_json = json.dumps(kwargs)
        data = {'client_id': API_CLIENT_ID, 'format': 'json', 'name':name}
        resp = get(API_ROOT + f'/{cls.__name__.lower()}s/', data)
        resp_data = loads(resp.text)
        result = []
        if resp_data['headers']['status'] == 'success':
            for elem in resp_data['results']:
                obj = cls(elem)
                result.append(obj)
        return result[0]

    @log_action
    def new_object(self) -> int:
        resp = post(API_ROOT + f'/{self.__class__.__name__.lower()}/one'
                    , data=self.__dict__)
        return resp.status_code

    @log_action
    def delete_object(self) -> int:
        resp = delete(API_ROOT + f'/{self.__class__.__name__.lower()}/one',
                      data=self.__dict__)
        return resp.status_code

    @classmethod
    def load(cls, data: dict[str, Any]):
        new_s = cls.__new__(cls)
        new_s.__init__()
        for k in data:
            new_s.__dict__[k] = data[k]
        return new_s
