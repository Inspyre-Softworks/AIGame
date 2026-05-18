'''Prompt construction for event generation.

Taylor B. | Inspyre-Softworks
'''

import json

from aigame.models.game_state import GameState


class EventPromptBuilder:
    '''Builds strict JSON-generation prompts for local LLM clients.'''

    def build(self, state: GameState) -> str:
        '''Compose the event prompt with continuity and state context.'''
        recent = [
            {
                'turn': record.turn,
                'event_title': record.event_title,
                'choice_id': record.choice_id,
            }
            for record in state.history[-3:]
        ]
        context = {
            'country_name': state.country_name,
            'turn': state.turn,
            'term_turns': state.term_turns,
            'stats': state.stats,
            'ideology_axes': state.ideology.to_dict(),
            'recent_history': recent,
        }
        return (
            'Generate one fictional political event for a narrative presidential simulation. '
            'Do not reference real-world politicians. Keep tone serious and politically intelligent. '
            'Vary event scale and avoid constant apocalyptic framing. Preserve continuity. '
            '\nReturn strict JSON only, matching this schema exactly:\n'
            '{"title":"string","summary":"string","narrative":"string","tone":"string",'
            '"event_scale":"minor | moderate | major | crisis","tags":["string"],"choices":[{'
            '"id":"string","label":"string","description":"string","public_rationale":"string",'
            '"private_implication":"string","suggested_consequences":[{"stat":"string",'
            '"delta":0,"reason":"string"}]}]}\n\n'
            f'Current game context:\n{json.dumps(context, indent=2)}'
        )
