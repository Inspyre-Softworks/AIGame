from aigame.llm.mock import MockLLMClient
from aigame.models.event import Event


def test_mock_client_returns_valid_event_json() -> None:
    client = MockLLMClient()

    payload = client.generate_event_json('generate event')
    event = Event.from_llm_json(payload)

    assert event.title
    assert len(event.choices) >= 2
