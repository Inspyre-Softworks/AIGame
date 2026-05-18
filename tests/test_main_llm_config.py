from aigame.config import GameConfig
from aigame.llm.mock import MockLLMClient
from aigame.llm.openai_compatible import OpenAICompatibleLLMClient
from main import build_llm_client, parse_args


def test_parse_args_defaults_to_lm_studio() -> None:
    config = GameConfig()
    args = parse_args(config, [])

    assert args.llm == 'lm-studio'
    assert args.base_url == config.lm_studio_base_url
    assert args.model == config.lm_studio_model


def test_build_llm_client_selects_mock() -> None:
    config = GameConfig()
    args = parse_args(config, ['--llm', 'mock'])

    client = build_llm_client(args)

    assert isinstance(client, MockLLMClient)


def test_build_llm_client_selects_openai_compatible() -> None:
    config = GameConfig()
    args = parse_args(config, ['--llm', 'lm-studio'])

    client = build_llm_client(args)

    assert isinstance(client, OpenAICompatibleLLMClient)
