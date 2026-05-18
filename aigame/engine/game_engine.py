'''Main deterministic game loop orchestration.

Taylor B. | Inspyre-Softworks
'''

from pydantic import ValidationError

from aigame.config import GameConfig
from aigame.engine.classification_engine import ClassificationEngine
from aigame.engine.rules_engine import RulesEngine
from aigame.llm.base import LLMClientBase
from aigame.models.choice import Choice
from aigame.models.consequence import Consequence
from aigame.models.event import Event
from aigame.models.game_state import GameState, TurnRecord
from aigame.prompts.event_prompt_builder import EventPromptBuilder
from aigame.utils.logging import Loggable


class GameEngine(Loggable):
    '''Coordinates event generation, choice resolution, and turn progression.'''

    def __init__(
        self,
        llm_client: LLMClientBase,
        config: GameConfig | None = None,
        rules_engine: RulesEngine | None = None,
        classification_engine: ClassificationEngine | None = None,
        prompt_builder: EventPromptBuilder | None = None,
    ) -> None:
        self.config = config or GameConfig()
        self.llm_client = llm_client
        self.rules_engine = rules_engine or RulesEngine(self.config)
        self.classification_engine = classification_engine or ClassificationEngine()
        self.prompt_builder = prompt_builder or EventPromptBuilder()

    def start_new_game(self, country_name: str | None = None) -> GameState:
        '''Create a fresh state for a new presidential term.'''
        state = GameState.new(config=self.config, country_name=country_name)
        self.logger.info('Started new game for %s', state.country_name)
        return state

    def is_term_complete(self, state: GameState) -> bool:
        '''Check whether the presidency has reached end of term.'''
        return state.turn > state.term_turns

    def get_turn_event(self, state: GameState) -> Event:
        '''Generate an event with retry+fallback behavior on invalid payloads.'''
        prompt = self.prompt_builder.build(state)
        for _ in range(self.config.llm_max_retries + 1):
            try:
                payload = self.llm_client.generate_event_json(prompt)
            except Exception as exc:  # noqa: BLE001
                self.logger.warning('LLM request failed. Retrying... (%s)', exc)
                continue
            try:
                return self.llm_client.parse_event(payload)
            except ValidationError:
                self.logger.warning('Invalid LLM payload encountered. Retrying...')
        self.logger.warning('Using deterministic fallback event after failed validation.')
        return self._fallback_event()

    def apply_choice(self, state: GameState, event: Event, choice_id: str) -> list[dict[str, int | str]]:
        '''Resolve selected choice and advance the turn.'''
        choice = self._find_choice(event.choices, choice_id)
        applied = self.rules_engine.apply_consequences(state, choice.suggested_consequences)
        state.history.append(
            TurnRecord(
                turn=state.turn,
                event_title=event.title,
                choice_id=choice.id,
                applied_changes=applied,
            )
        )
        state.turn += 1
        return applied

    def end_of_term_summary(self, state: GameState) -> dict[str, object]:
        '''Build final summary and classification.'''
        return {
            'country_name': state.country_name,
            'turns_played': len(state.history),
            'classification': self.classification_engine.classify(state),
            'final_stats': state.stats,
        }

    def _find_choice(self, choices: list[Choice], choice_id: str) -> Choice:
        for choice in choices:
            if choice.id == choice_id:
                return choice
        raise ValueError(f'Unknown choice id: {choice_id}')

    def _fallback_event(self) -> Event:
        fallback_choices = [
            Choice(
                id='transparency_push',
                label='Launch a transparency campaign',
                description='Open procurement records and invite civil monitors.',
                public_rationale='Public trust needs visible accountability.',
                private_implication='Elite allies may resist scrutiny.',
                suggested_consequences=[
                    Consequence(stat='corruption', delta=-5, reason='Oversight curbs rent-seeking.'),
                    Consequence(stat='public_approval', delta=4, reason='Citizens reward transparency.'),
                    Consequence(stat='elite_approval', delta=-3, reason='Patronage networks lose influence.'),
                ],
            ),
            Choice(
                id='quiet_deal',
                label='Cut a quiet deal with power brokers',
                description='Stabilize the coalition through private concessions.',
                public_rationale='A united government prevents broader paralysis.',
                private_implication='Risk of long-term institutional decay.',
                suggested_consequences=[
                    Consequence(stat='stability', delta=4, reason='Elite conflict is temporarily reduced.'),
                    Consequence(stat='corruption', delta=4, reason='Informal deals expand.'),
                    Consequence(stat='democratic_integrity', delta=-3, reason='Opaque bargains weaken trust.'),
                ],
            ),
        ]
        return Event(
            title='Deterministic Fallback: Integrity Commission Debate',
            summary='Your advisors split over immediate anti-corruption reforms.',
            narrative='Without reliable intelligence from your briefing system, your cabinet turns to a known contingency agenda.',
            tone='measured',
            event_scale='minor',
            tags=['fallback', 'governance'],
            choices=fallback_choices,
        )
