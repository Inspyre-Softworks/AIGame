from aigame.config import GameConfig
from aigame.engine.game_engine import GameEngine
from aigame.llm.mock import MockLLMClient


def test_choice_application_updates_state_and_history() -> None:
    engine = GameEngine(llm_client=MockLLMClient(), config=GameConfig())
    state = engine.start_new_game()
    event = engine.get_turn_event(state)

    original_turn = state.turn
    original_economy = state.stats['economy']

    applied = engine.apply_choice(state, event, event.choices[0].id)

    assert state.turn == original_turn + 1
    assert len(state.history) == 1
    assert state.stats['economy'] != original_economy
    assert applied
