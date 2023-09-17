from .AbstractApiKey import AbstractApiKey
from .ApiKeyFactory import ApiKeyFactory
from dotenv import load_dotenv
from random import choice
import json
import os


class ApiKeyManager:
    def __init__(self):
        load_dotenv()
        self.key_types = ['SourceGraph']
        self.keys = []
        self.last_use_api_key = {}
        self.key_factory = ApiKeyFactory()
        self._load_keys()

    def _load_balancer(self, key_type) -> AbstractApiKey or None:

        keys = []
        enable_keys = list(filter(lambda x: x.enable is True and x.type == key_type, self.keys))

        if len(enable_keys) == 0:
            return None

        if len(enable_keys) == 1:
            keys.append(
                enable_keys[0]
            )
        elif self.last_use_api_key[key_type] is None:
            [keys.append(i) for i in enable_keys]

        else:
            [keys.append(i) for i in filter(lambda x: x != self.last_use_api_key[key_type], enable_keys)]

        if len(enable_keys) == 0:
            return None

        key: AbstractApiKey = choice(list(keys))
        if key.check_status() is False:
            return self._load_balancer(key_type)
        else:
            return key

    def _check_keys(self, key_type: str):
        for i in list(filter(lambda x: x.type == key_type, self.keys)):
            if i.check_status():
                i.enable = True
            else:
                i.enable = False

    def _load_keys(self):
        for i in self.key_types:
            self.keys += [self.key_factory.create_api_key(j, i) for j in os.getenv(f"{i}_keys").split(" ")]

    def get_completion(self, key_type: str, data: dict):
        key: AbstractApiKey or None = self._load_balancer(key_type=key_type)
        if key is None:
            return None

        rs = key.get_completion(data=data)
        if type(rs) == int:
            return rs
        full_content = ""
        for i in rs:
            try:
                json_data = json.loads(str(i))
                if 'completion' in json_data.keys():
                    # dict_keys(['max_tokens_to_sample', 'model', 'prompt', 'stop_sequences', 'temperature'])
                    full_content = json_data['completion']
            except Exception as e:
                continue
        return full_content

