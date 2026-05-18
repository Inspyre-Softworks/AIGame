'''CLI entrypoint for AIGame MVP.

Taylor B. | Inspyre-Softworks
'''

import argparse

from aigame.config import GameConfig
from aigame.engine.game_engine import GameEngine
from aigame.llm.base import LLMClientBase
from aigame.llm.mock import MockLLMClient
from aigame.llm.openai_compatible import OpenAICompatibleLLMClient
from aigame.ui.terminal_app import TerminalApp


def parse_args(config: GameConfig, argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Narrative political simulation MVP.')
    parser.add_argument('--llm', choices=['mock', 'openai-compatible', 'lm-studio'], default='lm-studio')
    parser.add_argument('--base-url', default=config.lm_studio_base_url)
    parser.add_argument('--model', default=config.lm_studio_model)
    parser.add_argument('--api-key', default=config.lm_studio_api_key)
    parser.add_argument('--timeout-seconds', type=int, default=config.lm_studio_timeout_seconds)
    parser.add_argument('--endpoint-path', default=config.openai_compatible_endpoint_path)
    parser.add_argument(
        '--message-content-format',
        choices=['string', 'content-parts'],
        default=config.openai_compatible_message_content_format,
    )
    return parser.parse_args(argv)


def build_llm_client(args: argparse.Namespace) -> LLMClientBase:
    '''Create an LLM client from parsed CLI arguments.'''
    if args.llm == 'mock':
        return MockLLMClient()
    return OpenAICompatibleLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=args.timeout_seconds,
        endpoint_path=args.endpoint_path,
        message_content_format=args.message_content_format,
    )


def main() -> None:
    config = GameConfig()
    args = parse_args(config)
    llm_client = build_llm_client(args)
    engine = GameEngine(config=config, llm_client=llm_client)
    TerminalApp(engine=engine, config=config).run()


if __name__ == '__main__':
    main()
