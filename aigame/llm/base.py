'''LLM abstraction layer.

Taylor B. | Inspyre-Softworks
'''

from abc import ABC, abstractmethod

from aigame.models.event import Event


class LLMClientBase(ABC):
    '''Base contract for local or mock LLM providers.'''

    @abstractmethod
    def generate_event_json(self, prompt: str) -> str:
        '''Return strict JSON for event generation.'''

    def parse_event(self, payload: str) -> Event:
        '''Parse and validate event JSON payload.'''
        return Event.from_llm_json(payload)
