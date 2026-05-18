from aigame.config import GameConfig
from aigame.engine.classification_engine import ClassificationEngine
from aigame.models.game_state import GameState


def test_classification_democratic_reformer() -> None:
    state = GameState.new(config=GameConfig())
    state.stats['democratic_integrity'] = 80
    state.stats['civil_liberties'] = 75

    assert ClassificationEngine().classify(state) == 'Democratic Reformer'


def test_classification_military_backed_autocrat() -> None:
    state = GameState.new(config=GameConfig())
    state.stats['authoritarianism'] = 85
    state.stats['military_loyalty'] = 75

    assert ClassificationEngine().classify(state) == 'Military-Backed Autocrat'
