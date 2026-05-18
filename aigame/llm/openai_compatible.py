'''OpenAI-compatible HTTP client for local model servers.

Taylor B. | Inspyre-Softworks
'''

import json
from urllib import request

from aigame.llm.base import LLMClientBase


class OpenAICompatibleLLMClient(LLMClientBase):
    '''Calls a local OpenAI-compatible /chat/completions endpoint.'''

    def __init__(
        self,
        base_url: str = 'http://localhost:1234/v1',
        model: str = 'local-model',
        api_key: str = 'local-dev-key',
        timeout_seconds: int = 300,
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._model = model
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds

    def generate_event_json(self, prompt: str) -> str:
        endpoint = f'{self._base_url}/chat/completions'
        body = {
            'model': self._model,
            'messages': [
                {'role': 'system', 'content': 'You are a political simulation event generator.'},
                {'role': 'user', 'content': prompt},
            ],
            'temperature': 0.7,
        }
        payload = json.dumps(body).encode('utf-8')
        req = request.Request(
            endpoint,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_key}',
            },
            method='POST',
        )
        with request.urlopen(req, timeout=self._timeout_seconds) as response:
            parsed = json.loads(response.read().decode('utf-8'))
        return str(parsed['choices'][0]['message']['content'])
