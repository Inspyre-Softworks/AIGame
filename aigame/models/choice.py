'''Choice models.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import dataclass, field

from aigame.models.consequence import Consequence


@dataclass(slots=True)
class Choice:
    '''A player decision branch for a generated event.'''

    id: str
    label: str
    description: str
    public_rationale: str
    private_implication: str
    suggested_consequences: list[Consequence] = field(default_factory=list)
