'''CLI entrypoint for AIGame MVP.

Taylor B. | Inspyre-Softworks
'''

import argparse

from aigame.config import GameConfig
from aigame.engine.game_engine import GameEngine
from aigame.llm.mock import MockLLMClient
from aigame.llm.openai_compatible import OpenAICompatibleLLMClient
from aigame.ui.terminal_app import TerminalApp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Narrative political simulation MVP.')
    parser.add_argument('--llm', choices=['mock', 'openai-compatible'], default='mock')
    parser.add_argument('--base-url', default='http://localhost:1234/v1')
    parser.add_argument('--model', default='local-model')
    parser.add_argument('--api-key', default='local-dev-key')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GameConfig()
    if args.llm == 'mock':
        llm_client = MockLLMClient()
    else:
        llm_client = OpenAICompatibleLLMClient(
            base_url=args.base_url,
            model=args.model,
            api_key=args.api_key,
        )
    engine = GameEngine(config=config, llm_client=llm_client)
    TerminalApp(engine=engine, config=config).run()


if __name__ == '__main__':
    main()
