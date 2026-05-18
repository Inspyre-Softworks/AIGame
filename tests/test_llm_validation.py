import pytest
from pydantic import ValidationError

from aigame.models.event import Event, is_valid_event_json


def test_valid_json_is_accepted() -> None:
    payload = (
        '{"title":"t","summary":"s","narrative":"n","tone":"serious",'
        '"event_scale":"minor","tags":["x"],"choices":[{"id":"a","label":"l",'
        '"description":"d","public_rationale":"p","private_implication":"i",'
        '"suggested_consequences":[]}]}'
    )
    event = Event.from_llm_json(payload)
    assert event.title == 't'
    assert is_valid_event_json(payload)


def test_invalid_json_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Event.from_llm_json('{"title":"missing fields"}')
