'''Core game state model.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import asdict, dataclass, field

from aigame.config import GameConfig
from aigame.models.political_axes import PoliticalAxes


DEFAULT_STATS: dict[str, int] = {
    'economy': 50,
    'inflation': 8,
    'unemployment': 10,
    'public_approval': 55,
    'elite_approval': 50,
    'military_loyalty': 50,
    'opposition_strength': 45,
    'media_freedom': 60,
    'civil_liberties': 60,
    'corruption': 40,
    'stability': 55,
    'international_reputation': 50,
    'diplomatic_leverage': 45,
    'debt': 75,
    'gdp_growth': 3,
    'inequality': 55,
    'authoritarianism': 35,
    'democratic_integrity': 60,
    'nationalist_sentiment': 45,
    'labor_power': 45,
    'corporate_power': 55,
    'religious_influence': 40,
    'populist_energy': 50,
    'revolutionary_pressure': 30,
}


@dataclass(slots=True)
class TurnRecord:
    '''Persisted record of a completed turn.'''

    turn: int
    event_title: str
    choice_id: str
    applied_changes: list[dict[str, int | str]]


@dataclass(slots=True)
class GameState:
    '''Serializable game state for a full presidential term.'''

    country_name: str
    term_turns: int
    turn: int
    stats: dict[str, int] = field(default_factory=lambda: DEFAULT_STATS.copy())
    ideology: PoliticalAxes = field(default_factory=PoliticalAxes)
    history: list[TurnRecord] = field(default_factory=list)

    @classmethod
    def new(cls, config: GameConfig, country_name: str | None = None) -> 'GameState':
        '''Create a fresh game state for a new presidency.'''
        return cls(
            country_name=country_name or config.default_country_name,
            term_turns=config.term_turns,
            turn=config.starting_turn,
        )

    def to_dict(self) -> dict[str, object]:
        '''Serialize state to dict for persistence.'''
        return {
            'country_name': self.country_name,
            'term_turns': self.term_turns,
            'turn': self.turn,
            'stats': self.stats,
            'ideology': self.ideology.to_dict(),
            'history': [asdict(entry) for entry in self.history],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> 'GameState':
        '''Hydrate game state from persisted dictionary.'''
        history_payload = payload.get('history', [])
        return cls(
            country_name=str(payload['country_name']),
            term_turns=int(payload['term_turns']),
            turn=int(payload['turn']),
            stats={key: int(value) for key, value in dict(payload.get('stats', {})).items()},
            ideology=PoliticalAxes.from_dict(dict(payload.get('ideology', {}))),
            history=[
                TurnRecord(
                    turn=int(entry['turn']),
                    event_title=str(entry['event_title']),
                    choice_id=str(entry['choice_id']),
                    applied_changes=list(entry['applied_changes']),
                )
                for entry in history_payload
            ],
        )
