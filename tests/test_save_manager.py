from pathlib import Path

from aigame.config import GameConfig
from aigame.models.game_state import GameState
from aigame.persistence.save_manager import SaveManager


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    config = GameConfig()
    state = GameState.new(config=config, country_name='Arcadia')
    state.stats['economy'] = 67
    path = tmp_path / 'save.json'

    manager = SaveManager()
    manager.save(path, state)
    loaded = manager.load(path)

    assert loaded.country_name == 'Arcadia'
    assert loaded.stats['economy'] == 67
    assert loaded.turn == state.turn
