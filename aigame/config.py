'''Configuration models for the AIGame MVP.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import dataclass, field


@dataclass(slots=True)
class GameConfig:
    '''Global configuration for the political simulation MVP.'''

    term_turns: int = 12
    starting_turn: int = 1
    llm_max_retries: int = 2
    lm_studio_base_url: str = 'http://127.0.0.1:1234/v1'
    lm_studio_model: str = 'local-model'
    lm_studio_api_key: str = 'lm-studio'
    lm_studio_timeout_seconds: int = 300
    save_file_name: str = 'presidency_save.json'
    default_country_name: str = 'The Republic of Vespera'
    min_stat_value: int = 0
    max_stat_value: int = 100
    stat_bounds: dict[str, tuple[int, int]] = field(
        default_factory=lambda: {
            'debt': (0, 200),
            'gdp_growth': (-20, 20),
            'inflation': (-5, 60),
            'unemployment': (0, 60),
        }
    )
