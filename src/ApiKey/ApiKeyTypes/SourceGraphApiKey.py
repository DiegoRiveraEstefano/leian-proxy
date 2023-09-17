from ..AbstractApiKey import AbstractApiKey
import requests


class SourceGraphApiKey(AbstractApiKey):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.type = "SourceGraph"

    def check_status(self) -> bool:
        #rs = await session.get("")
        #return True if rs.status == 200 else False
        return True

    def get_completion(self, data: dict) -> list[str] or int:
        session = requests.session()
        [session.headers.__setitem__(i, self.headers[i]) for i in self.headers.keys()]

        rs = session.post(
            url="https://sourcegraph.com/.api/completions/stream",
            json={
                'model': data['model'],
                'prompt': data['prompt'],
                'maxTokensToSample': data['max_tokens_to_sample'],
                'temperature': data['temperature'],
                'stop_sequences': data['stop_sequences']
            },
            timeout=180000
        )
        if rs.status_code == 429:
            print("Error")
            return 429
        if rs.status_code == 400:
            self.enable = False
            return 400
        buffer = b""
        for i in rs.iter_content(chunk_size=1024):
            buffer += i
        lines = str(buffer).split("\\n")[:-1]
        data = list(map(lambda x: x.replace("data: ", ""), filter(lambda x: x.startswith("data: "), lines)))
        return data