from json import loads

import requests
from requests import delete, get, post

from config import API_CLIENT_ID, API_ROOT

from .custom_exc import APIFailException
# from .models import Descriptor
from .special import MetaControl, log_action, Descriptor


class APIConnect(metaclass=MetaControl):
    slots = []
    name = Descriptor()

    def __init__(self, data):
        for field in self.slots:
            setattr(self, field, data[field])

    @classmethod
    @log_action
    def get_all(cls, limit: int | str = 15, **kwargs):
        if limit is str:
            limit = "all"
        else:
            limit = limit if limit >= 10 else 10
            limit = limit if limit <= 200 else 200
        data = {"client_id": API_CLIENT_ID, "format": "json", "limit": limit, **kwargs}
        resp = None
        try:
            resp = get(API_ROOT + f"{cls.__name__.lower()}s/", data)
        except requests.exceptions.ConnectionError or resp.status_code != 200 or not resp:
            print("Нет доступа к API, проверьте интернет-соединение и всё такое")
            quit()
        resp_data = loads(resp.text)
        result = []
        if resp_data["headers"]["status"] == "success":
            for elem in resp_data["results"]:
                obj = cls(elem)
                result.append(obj)
            return result
        else:
            raise APIFailException

    @classmethod
    @log_action
    def get_one(cls, **kwargs):
        data = {"client_id": API_CLIENT_ID, "format": "json", **kwargs}
        resp = get(API_ROOT + f"{cls.__name__.lower()}s/", data)
        resp_data = loads(resp.text)
        result = []
        if resp_data["headers"]["status"] == "success":
            for elem in resp_data["results"]:
                obj = cls(elem)
                result.append(obj)
            return result[0] if result else None
        raise APIFailException

    @log_action
    def new_object(self) -> int:
        resp = post(
            API_ROOT + f"/{self.__class__.__name__.lower()}/one", data=self.__dict__
        )
        return resp.status_code

    @log_action
    def delete_object(self) -> int:
        resp = delete(
            API_ROOT + f"/{self.__class__.__name__.lower()}/one", data=self.__dict__
        )
        return resp.status_code

    def get_dict(self):
        return {self.__dict__[k] for k in self.slots}

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"
