from .AbstractApiKey import AbstractApiKey
from .ApiKeyTypes.SourceGraphApiKey import SourceGraphApiKey


class ApiKeyFactory:
    def __init__(self):
        self.api_keys_types = {"SourceGraph": SourceGraphApiKey}

    def create_api_key(self, token: str, api_key_type: str) -> AbstractApiKey or None:
        if not api_key_type in self.api_keys_types.keys():
            return None

        return self.api_keys_types[api_key_type](token)
