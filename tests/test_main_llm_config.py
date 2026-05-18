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
    assert args.timeout_seconds == config.lm_studio_timeout_seconds
    assert args.endpoint_path == config.openai_compatible_endpoint_path
    assert args.message_content_format == config.openai_compatible_message_content_format


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
    assert client._timeout_seconds == config.lm_studio_timeout_seconds
    assert client._endpoint_path == config.openai_compatible_endpoint_path


def test_build_llm_client_respects_timeout_override() -> None:
    config = GameConfig()
    args = parse_args(config, ['--llm', 'lm-studio', '--timeout-seconds', '300'])

    client = build_llm_client(args)

    assert isinstance(client, OpenAICompatibleLLMClient)
    assert client._timeout_seconds == 300


def test_build_llm_client_respects_openai_compatible_overrides() -> None:
    config = GameConfig()
    args = parse_args(
        config,
        [
            '--llm',
            'openai-compatible',
            '--endpoint-path',
            '/api/v1/chat/completions',
            '--message-content-format',
            'content-parts',
        ],
    )

    client = build_llm_client(args)

    assert isinstance(client, OpenAICompatibleLLMClient)
    assert client._endpoint_path == '/api/v1/chat/completions'
    assert client._message_content_format == 'content-parts'
