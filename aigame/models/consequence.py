'''Consequence models.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import dataclass


@dataclass(slots=True)
class Consequence:
    '''A deterministic stat change that the engine can validate and apply.'''

    stat: str
    delta: int
    reason: str
