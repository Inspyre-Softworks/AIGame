from aigame.config import GameConfig
from aigame.engine.game_engine import GameEngine
from aigame.llm.base import LLMClientBase


class InvalidLLMClient(LLMClientBase):
    def generate_event_json(self, prompt: str) -> str:
        _ = prompt
        return '{"invalid":true}'


def test_game_engine_falls_back_after_invalid_llm_payload() -> None:
    engine = GameEngine(llm_client=InvalidLLMClient(), config=GameConfig(llm_max_retries=1))
    state = engine.start_new_game()

    event = engine.get_turn_event(state)

    assert event.title.startswith('Deterministic Fallback')
    assert len(event.choices) >= 2
