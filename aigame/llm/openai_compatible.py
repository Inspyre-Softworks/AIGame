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
        endpoint_path: str = '/chat/completions',
        message_content_format: str = 'string',
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._model = model
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds
        self._endpoint_path = f'/{endpoint_path.strip("/")}' if endpoint_path else '/chat/completions'
        if message_content_format not in {'string', 'content-parts'}:
            raise ValueError("message_content_format must be 'string' or 'content-parts'")
        self._message_content_format = message_content_format

    def generate_event_json(self, prompt: str) -> str:
        endpoint = f'{self._base_url}{self._endpoint_path}'
        body = {
            'model': self._model,
            'messages': [
                {'role': 'system', 'content': self._build_message_content('You are a political simulation event generator.')},
                {'role': 'user', 'content': self._build_message_content(prompt)},
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

    def _build_message_content(self, text: str) -> str | list[dict[str, str]]:
        if self._message_content_format == 'content-parts':
            return [{'type': 'text', 'text': text}]
        return text
