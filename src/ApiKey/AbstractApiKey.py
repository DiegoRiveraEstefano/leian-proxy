
class AbstractApiKey:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.enable = True
        self.type = None
        self.headers = {
            #"Content-Type": "application/json",
            "Authorization": f"token {self.api_key}",
            "Accept": "text/event-stream",
            "Connection": "keep-alive",
            'Transfer-Encoding': 'chunked',
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream; charset=utf-8',
        }

    def __eq__(self, other) -> bool:
        if type(other) != AbstractApiKey:
            return False
        if self.api_key != other.api_key:
            return False
        return True

    def check_status(self) -> bool:
        pass

    def get_completion(self, data: dict) -> str:
        pass
