'''Event and LLM response schema models.

Taylor B. | Inspyre-Softworks
'''

from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from aigame.models.choice import Choice
from aigame.models.consequence import Consequence


class LLMConsequence(BaseModel):
    '''LLM consequence payload schema.'''

    stat: str
    delta: int
    reason: str


class LLMChoice(BaseModel):
    '''LLM choice payload schema.'''

    id: str
    label: str
    description: str
    public_rationale: str
    private_implication: str
    suggested_consequences: list[LLMConsequence] = Field(default_factory=list)


class LLMEventPayload(BaseModel):
    '''Strict expected LLM response payload schema.'''

    title: str
    summary: str
    narrative: str
    tone: str
    event_scale: Literal['minor', 'moderate', 'major', 'crisis']
    tags: list[str] = Field(default_factory=list)
    choices: list[LLMChoice]


@dataclass(slots=True)
class Event:
    '''In-engine event model used by terminal UI and game engine.'''

    title: str
    summary: str
    narrative: str
    tone: str
    event_scale: str
    tags: list[str] = field(default_factory=list)
    choices: list[Choice] = field(default_factory=list)

    @classmethod
    def from_llm_json(cls, payload_json: str) -> 'Event':
        '''Validate and map JSON payload into engine event model.'''
        parsed = LLMEventPayload.model_validate_json(payload_json)
        return cls(
            title=parsed.title,
            summary=parsed.summary,
            narrative=parsed.narrative,
            tone=parsed.tone,
            event_scale=parsed.event_scale,
            tags=parsed.tags,
            choices=[
                Choice(
                    id=choice.id,
                    label=choice.label,
                    description=choice.description,
                    public_rationale=choice.public_rationale,
                    private_implication=choice.private_implication,
                    suggested_consequences=[
                        Consequence(stat=item.stat, delta=item.delta, reason=item.reason)
                        for item in choice.suggested_consequences
                    ],
                )
                for choice in parsed.choices
            ],
        )


def is_valid_event_json(payload_json: str) -> bool:
    '''Quick validity checker used by tests and fallback logic.'''
    try:
        LLMEventPayload.model_validate_json(payload_json)
    except ValidationError:
        return False
    return True
