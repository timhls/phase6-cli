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

## RECENT UPDATES (SESSION SUMMARY)

### Vocabulary Management (2026-04-14)
- **Scope**: Bulk added 572 cards (286 unique entries) across two subjects:
  - `360 Standard Sentences in Chinese Conversations 1 (Chinese-English)`
  - `360 Standard Sentences in Chinese Conversations 1 (English-Chinese)`
- **Units**: Populated `Lesson 1-5 Vocabulary` and `Preply Lesson 1-4 Vocabulary`.
- **Methodology**:
  - Utilized `pyphase6 import` with temporary JSON files for high-volume additions.
  - Formatted the "Answer" field with HTML `<br/>` to separate Pinyin for proper Phase-6 multi-line rendering.
  - Relied on Phase-6 API's `DUPLICATED_CONTENT` detection to safely skip existing entries.
- **Technical Insight**: The CLI successfully handled large-scale imports (up to 65 cards per unit) while maintaining the saved session state from `~/.config/pyphase6/session.json`.
