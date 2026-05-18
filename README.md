# AIGame

Taylor B. | Inspyre-Softworks

## Clarifying questions for next milestone

1. Should each turn represent a month or quarter by default?
2. Should the default term length remain 12 turns, or map to a specific constitutional duration?
3. Should ideology axes directly affect classification in milestone 2, or remain informational for now?

## Implemented milestone (terminal MVP)

### Proposed modular architecture

- `aigame/config.py`
- `aigame/models/`
- `aigame/engine/`
- `aigame/llm/`
- `aigame/prompts/`
- `aigame/persistence/`
- `aigame/ui/`
- `main.py`

### Current MVP scope

- Start a new presidency with configurable country name.
- Show key country stats each turn.
- Generate event JSON from `MockLLMClient` (or OpenAI-compatible local server).
- Validate strict JSON into typed event models.
- Present player choices in terminal.
- Apply deterministic engine-validated consequences with clamping.
- Persist game state each turn and reload saves.
- Finish term and generate leader classification.
- Fallback to deterministic event when invalid LLM output is returned.

### Main data models

- `GameState` with configurable political-economic levers and turn history.
- `PoliticalAxes` for multi-axis ideology tracking.
- `Event`, `Choice`, and `Consequence` for narrative+decision flow.

## Run locally

```bash
python main.py
```

By default, the CLI now uses **LM Studio-style OpenAI-compatible settings** (`http://127.0.0.1:1234/v1`) with a **120 second request timeout**.

Useful commands:

```bash
# Use LM Studio defaults
python main.py --llm lm-studio

# Override LM Studio model/base URL
python main.py --llm lm-studio --model your-model-id --base-url http://127.0.0.1:1234/v1

# Increase timeout for slower local models
python main.py --llm lm-studio --timeout-seconds 300

# Force mock mode for offline testing
python main.py --llm mock
```
