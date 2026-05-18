'''Terminal user interface for the MVP.

Taylor B. | Inspyre-Softworks
'''

from pathlib import Path

from aigame.config import GameConfig
from aigame.engine.game_engine import GameEngine
from aigame.models.event import Event
from aigame.models.game_state import GameState
from aigame.persistence.save_manager import SaveManager


class TerminalApp:
    '''Interactive terminal application for one full presidential term.'''

    def __init__(self, engine: GameEngine, config: GameConfig | None = None) -> None:
        self.config = config or GameConfig()
        self.engine = engine
        self.save_manager = SaveManager()

    def run(self) -> None:
        '''Run the terminal gameplay loop.'''
        print('=== AIGame: Presidential Term Simulation ===')
        print('Taylor B. | Inspyre-Softworks')

        save_path = Path(self.config.save_file_name)
        state = self._load_or_new(save_path)

        while not self.engine.is_term_complete(state):
            self._show_stats(state)
            event = self.engine.get_turn_event(state)
            self._show_event(event)
            selected = self._prompt_choice(event)
            applied = self.engine.apply_choice(state, event, selected)
            print('\nApplied consequences:')
            if not applied:
                print('  - No validated stat changes were applied.')
            else:
                for item in applied:
                    print(f"  - {item['stat']}: {item['delta']:+d} ({item['reason']})")
            self.save_manager.save(save_path, state)
            print(f'\nTurn complete. Progress saved to {save_path.resolve()}\n')

        summary = self.engine.end_of_term_summary(state)
        print('=== End of Term Report ===')
        print(f"Country: {summary['country_name']}")
        print(f"Turns played: {summary['turns_played']}")
        print(f"Leader classification: {summary['classification']}")

    def _load_or_new(self, save_path: Path) -> GameState:
        if save_path.exists():
            response = input(f'Load existing save from {save_path}? [y/N]: ').strip().lower()
            if response == 'y':
                return self.save_manager.load(save_path)
        country = input('Enter country name (leave blank for default): ').strip()
        return self.engine.start_new_game(country_name=country or None)

    def _show_stats(self, state: GameState) -> None:
        print(f'\n--- Turn {state.turn}/{state.term_turns} ---')
        key_stats = [
            'economy',
            'public_approval',
            'stability',
            'democratic_integrity',
            'authoritarianism',
            'corruption',
            'international_reputation',
            'revolutionary_pressure',
        ]
        for stat in key_stats:
            print(f'  {stat}: {state.stats[stat]}')

    def _show_event(self, event: Event) -> None:
        print('\n=== Event Briefing ===')
        print(f'Title: {event.title}')
        print(f'Scale: {event.event_scale} | Tone: {event.tone}')
        print(f'Summary: {event.summary}')
        print(f'Narrative: {event.narrative}')
        print('\nChoices:')
        for idx, choice in enumerate(event.choices, start=1):
            print(f'  {idx}. {choice.label} ({choice.id})')
            print(f'     {choice.description}')

    def _prompt_choice(self, event: Event) -> str:
        while True:
            raw = input('Select choice number: ').strip()
            if raw.isdigit() and 1 <= int(raw) <= len(event.choices):
                return event.choices[int(raw) - 1].id
            print('Invalid choice. Please enter a valid number.')
