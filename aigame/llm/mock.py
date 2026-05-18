'''Mock LLM client for offline deterministic testing.

Taylor B. | Inspyre-Softworks
'''

import json

from aigame.llm.base import LLMClientBase


class MockLLMClient(LLMClientBase):
    '''Returns deterministic event JSON with meaningful tradeoffs.'''

    def generate_event_json(self, prompt: str) -> str:
        _ = prompt
        payload = {
            'title': 'Cabinet Fracture Over Industrial Policy',
            'summary': 'A policy split threatens your governing coalition.',
            'narrative': (
                'Your finance minister demands rapid deregulation while labor leaders '
                'warn of mass layoffs if state protections are removed.'
            ),
            'tone': 'tense',
            'event_scale': 'moderate',
            'tags': ['cabinet', 'economy', 'labor'],
            'choices': [
                {
                    'id': 'back_markets',
                    'label': 'Back the finance minister',
                    'description': 'Accelerate privatization and deregulation.',
                    'public_rationale': 'Growth requires market confidence.',
                    'private_implication': 'Labor groups may radicalize.',
                    'suggested_consequences': [
                        {'stat': 'economy', 'delta': 6, 'reason': 'Investor sentiment improves.'},
                        {'stat': 'labor_power', 'delta': -5, 'reason': 'Unions lose leverage.'},
                        {'stat': 'public_approval', 'delta': -3, 'reason': 'Working-class backlash.'},
                    ],
                },
                {
                    'id': 'back_labor',
                    'label': 'Broker a labor-security pact',
                    'description': 'Guarantee worker protections before reforms.',
                    'public_rationale': 'Transition must stay socially stable.',
                    'private_implication': 'Elite allies may call you weak.',
                    'suggested_consequences': [
                        {'stat': 'stability', 'delta': 4, 'reason': 'Street tensions cool.'},
                        {'stat': 'elite_approval', 'delta': -4, 'reason': 'Business bloc resists.'},
                        {'stat': 'economy', 'delta': 2, 'reason': 'Reforms proceed slower.'},
                    ],
                },
                {
                    'id': 'delay_decision',
                    'label': 'Delay and commission a review',
                    'description': 'Postpone reform for a quarter.',
                    'public_rationale': 'A full review prevents policy mistakes.',
                    'private_implication': 'Both camps see indecision.',
                    'suggested_consequences': [
                        {'stat': 'stability', 'delta': -2, 'reason': 'Uncertainty deepens.'},
                        {'stat': 'public_approval', 'delta': -2, 'reason': 'Perception of drift.'},
                        {'stat': 'corruption', 'delta': 2, 'reason': 'Lobbying intensifies.'},
                    ],
                },
            ],
        }
        return json.dumps(payload)
