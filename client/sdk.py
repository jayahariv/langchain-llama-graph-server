import requests

class LangChainClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def query(self, input_text):
        response = requests.post(f'{self.base_url}/query', json={'input': input_text})
        return response.json()
