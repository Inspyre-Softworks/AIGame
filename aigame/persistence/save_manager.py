'''Save/load manager for terminal MVP.

Taylor B. | Inspyre-Softworks
'''

import json
from pathlib import Path

from aigame.models.game_state import GameState


class SaveManager:
    '''Persists game state as JSON on disk.'''

    def save(self, path: Path, state: GameState) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state.to_dict(), indent=2), encoding='utf-8')

    def load(self, path: Path) -> GameState:
        payload = json.loads(path.read_text(encoding='utf-8'))
        return GameState.from_dict(payload)
