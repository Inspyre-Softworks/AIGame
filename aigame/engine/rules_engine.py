'''Deterministic rules engine.

Taylor B. | Inspyre-Softworks
'''

from aigame.config import GameConfig
from aigame.models.consequence import Consequence
from aigame.models.game_state import GameState


class RulesEngine:
    '''Validates, clamps, and applies consequences to game state.'''

    def __init__(self, config: GameConfig) -> None:
        self._config = config

    def _bounds_for(self, stat: str) -> tuple[int, int]:
        return self._config.stat_bounds.get(
            stat,
            (self._config.min_stat_value, self._config.max_stat_value),
        )

    def apply_consequences(
        self,
        state: GameState,
        consequences: list[Consequence],
    ) -> list[dict[str, int | str]]:
        '''Apply valid consequences and return normalized applied change records.'''
        applied_changes: list[dict[str, int | str]] = []
        for consequence in consequences:
            if consequence.stat not in state.stats:
                continue
            old_value = state.stats[consequence.stat]
            lower, upper = self._bounds_for(consequence.stat)
            new_value = max(lower, min(upper, old_value + consequence.delta))
            if new_value == old_value:
                continue
            state.stats[consequence.stat] = new_value
            applied_changes.append(
                {
                    'stat': consequence.stat,
                    'delta': new_value - old_value,
                    'reason': consequence.reason,
                }
            )
        return applied_changes
