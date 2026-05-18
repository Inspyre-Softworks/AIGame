import json

from aigame.llm.openai_compatible import OpenAICompatibleLLMClient


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def __enter__(self) -> '_FakeResponse':
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        _ = (exc_type, exc, tb)
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode('utf-8')


def test_openai_compatible_client_supports_content_parts_format(monkeypatch) -> None:
    observed: dict[str, object] = {}

    def _fake_urlopen(req, timeout):  # noqa: ANN001
        observed['url'] = req.full_url
        observed['timeout'] = timeout
        observed['body'] = json.loads(req.data.decode('utf-8'))
        return _FakeResponse({'choices': [{'message': {'content': '{"title":"ok"}'}}]})

    monkeypatch.setattr('aigame.llm.openai_compatible.request.urlopen', _fake_urlopen)

    client = OpenAICompatibleLLMClient(
        base_url='https://lightning.ai',
        endpoint_path='/api/v1/chat/completions',
        model='openai/gpt-5',
        api_key='test-key',
        timeout_seconds=45,
        message_content_format='content-parts',
    )

    payload = client.generate_event_json('Hello, world!')

    assert payload == '{"title":"ok"}'
    assert observed['url'] == 'https://lightning.ai/api/v1/chat/completions'
    assert observed['timeout'] == 45
    assert observed['body'] == {
        'model': 'openai/gpt-5',
        'messages': [
            {
                'role': 'system',
                'content': [{'type': 'text', 'text': 'You are a political simulation event generator.'}],
            },
            {'role': 'user', 'content': [{'type': 'text', 'text': 'Hello, world!'}]},
        ],
        'temperature': 0.7,
    }
