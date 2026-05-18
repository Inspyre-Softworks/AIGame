from aigame.config import GameConfig
from aigame.engine.rules_engine import RulesEngine
from aigame.models.consequence import Consequence
from aigame.models.game_state import GameState


def test_rules_engine_applies_and_clamps_stats() -> None:
    config = GameConfig()
    state = GameState.new(config=config)
    engine = RulesEngine(config)
    state.stats['economy'] = 98

    applied = engine.apply_consequences(
        state,
        [Consequence(stat='economy', delta=20, reason='boom')],
    )

    assert state.stats['economy'] == 100
    assert applied == [{'stat': 'economy', 'delta': 2, 'reason': 'boom'}]


def test_rules_engine_skips_unknown_stat() -> None:
    config = GameConfig()
    state = GameState.new(config=config)
    engine = RulesEngine(config)

    applied = engine.apply_consequences(
        state,
        [Consequence(stat='unknown_stat', delta=5, reason='n/a')],
    )

    assert applied == []
