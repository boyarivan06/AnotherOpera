import json
import os
from typing import Any
# from config import SECRET_KEY

from requests import get, post, delete
from config import API_ROOT
from special import MetaControl, log_action


class APIConnect(metaclass=MetaControl):  # Strategy pattern? + mixin
    @classmethod
    @log_action
    def get_all(cls):
        res = get(API_ROOT + f'/{cls.__name__.lower()}')
        if res.status_code == 403:
            print("server doesn't working")
            quit()
        return json.loads(res.text)

    @classmethod
    @log_action
    def get_object_by_args(cls, **kwargs):
        # request_json = json.dumps(kwargs)
        resp = get(API_ROOT + f'/{cls.__name__.lower()}/one', kwargs)
        data = json.loads(resp.text)
        return cls.load(data)

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
