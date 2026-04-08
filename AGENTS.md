# pyphase6

## WHY

`pyphase6` is a modern Python client and Command Line Interface (CLI) for managing vocabulary in the Phase-6 web application (`https://lernen.phase-6.de/v2/#/manage`). It solves complex authentication flows using browser automation and falls back to direct, fast HTTP calls to reliably manage vocabulary items.

## WHAT

- **Core Library & CLI (`pyphase6/`)**: Contains Typer CLI commands, the `Phase6Client`, and Pydantic data models.
- **Testing & Scripts (`tests/`, `scripts/`)**: Includes pytest suites mocking API responses and ad-hoc execution scripts.
- **Tech Stack**:
  - Dependency & Build Management: `uv` (exclusively)
  - Browser Automation: `playwright`
  - HTTP Client: `httpx`
  - Validation: `pydantic`
  - CLI Framework: `typer`
  - CI/CD: GitHub Actions (with `semantic-release` directly to GitHub Releases)

## HOW

- **Commands**: Run all scripts and tests through `uv` (e.g., `uv run`, `uv sync`, `uv add`). Do not use `pip` or `poetry`.
- **Code Quality**: The agent should not act as a linter. Use existing automated tools to ensure code style and types:
  - Format: `uv run ruff format .`
  - Lint: `uv run ruff check . --fix`
  - Typecheck: `uv run mypy .`
- **Testing**: Verify changes using `uv run pytest`.

Note: Keep instructions here universally applicable. Task-specific instructions should be kept outside this file or discovered via context.
