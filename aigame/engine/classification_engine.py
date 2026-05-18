'''Leader classification rules.

Taylor B. | Inspyre-Softworks
'''

from aigame.models.game_state import GameState


class ClassificationEngine:
    '''Classifies presidency outcomes from final state values.'''

    def classify(self, state: GameState) -> str:
        stats = state.stats
        if stats['stability'] < 20 and stats['public_approval'] < 25:
            return 'Crisis President'
        if stats['authoritarianism'] >= 80 and stats['military_loyalty'] >= 65:
            return 'Military-Backed Autocrat'
        if stats['authoritarianism'] >= 75 and stats['economy'] >= 60:
            return 'Authoritarian Modernizer'
        if stats['authoritarianism'] >= 70 and stats['corruption'] >= 70:
            return 'Corrupt Oligarchic President'
        if stats['democratic_integrity'] >= 75 and stats['civil_liberties'] >= 70:
            return 'Democratic Reformer'
        if stats['economy'] >= 70 and stats['international_reputation'] >= 70:
            return 'Globalist Economic Architect'
        if stats['nationalist_sentiment'] >= 75 and stats['diplomatic_leverage'] < 45:
            return 'Nationalist Isolationist'
        if stats['public_approval'] >= 75 and stats['stability'] >= 70:
            return 'Beloved Statesperson'
        if stats['authoritarianism'] >= 80 and stats['democratic_integrity'] <= 30:
            return 'Managed-Democracy Ruler'
        if stats['revolutionary_pressure'] >= 75 and stats['stability'] <= 35:
            return 'Revolutionary President'
        return 'Technocratic Capitalist'
