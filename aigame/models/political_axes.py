'''Political ideology axis models.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class PoliticalAxes:
    '''Tracks ideology across multiple axes on a -100 to 100 scale.'''

    economic_left_vs_right: int = 0
    authoritarian_vs_libertarian: int = 0
    nationalist_vs_globalist: int = 0
    secular_vs_theocratic: int = 0
    reformist_vs_traditionalist: int = 0
    militarist_vs_diplomatic: int = 0
    populist_vs_institutionalist: int = 0

    def clamp(self) -> None:
        '''Clamp all ideology values to the allowed range.'''
        for axis_name, axis_value in asdict(self).items():
            bounded = max(-100, min(100, axis_value))
            setattr(self, axis_name, bounded)

    def to_dict(self) -> dict[str, int]:
        '''Convert to a serializable dictionary.'''
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, int]) -> 'PoliticalAxes':
        '''Construct axis model from persisted payload.'''
        axes = cls(**payload)
        axes.clamp()
        return axes
