# pyphase6

## Project Overview

`pyphase6` is a Python client and CLI for managing vocabulary in the Phase-6 web
application (`https://lernen.phase-6.de/v2/#/manage`). It reverse-engineers the
private SPA API: Playwright browser automation handles the login flow, and fast
direct JSON REST calls (via Playwright request contexts) handle vocabulary CRUD.

The repo is packaged as an **agent skill**: the entire project lives inside
`.agents/skills/phase6/` and is discovered by opencode and other
skill-aware agents via its `SKILL.md`.

## Skill Structure

```
Skill path:     .agents/skills/phase6/
SKILL.md:       .agents/skills/phase6/SKILL.md
Source code:    .agents/skills/phase6/scripts/pyphase6/
Tests:          .agents/skills/phase6/tests/
```

When asked about Phase-6 vocabulary management (subjects, units, cards,
imports), consult the `phase6` skill and invoke the CLI with
`uv run pyphase6 ...`.

## Build/Lint/Test Commands

All commands run through `uv` from the repo root. Never use `pip` or `poetry`.

```bash
# Install dependencies (editable install of the skill package)
uv sync

# Install Playwright browsers (required for login)
uv run playwright install chromium

# Format and lint
uv run ruff format .
uv run ruff check . --fix

# Typecheck (scoped to the skill package — mypy skips hidden dirs in discovery)
uv run mypy .agents/skills/phase6/scripts/pyphase6

# Security scan
uv run bandit -r .agents/skills/phase6/scripts

# Tests
uv run pytest
```

Do not act as a linter; rely on the tools above.

## Code Style

- Python 3.14, ruff (line length 100), mypy (default strictness)
- snake_case functions, PascalCase classes, Pydantic v2 models mirror the API's
  camelCase JSON field names
- CLI output: Rich tables for humans, `--json` (via `console.print_json`) for
  agents — keep new read commands agent-parseable

## Skills

Skills live in `.agents/skills/<name>/`. `SKILL.md` uses YAML frontmatter
(`name`, `description`, `license`, `compatibility`, `metadata`) followed by
Markdown body sections: When to use, How to invoke, Configuration,
Authentication, Gotchas, Further reading. Scripts go in `scripts/`, tests in
`tests/`, reference docs in `references/`. The Python package is wheeled from
the skill's `scripts/` dir via `[tool.hatch.build.targets.wheel]` in
`pyproject.toml`.

## Architecture

### Three-Layer Structure

1. **CLI Layer** (`scripts/pyphase6/cli.py`): Typer commands. Rich terminal
   I/O, validates auth state before delegating to the client.
2. **Client Layer** (`scripts/pyphase6/client.py`): `Phase6Client` — Playwright
   browser login, session in `~/.config/pyphase6/session.json`, Playwright
   request contexts for all API calls. Raises `AuthError` / `APIConnectionError`.
3. **Model Layer** (`scripts/pyphase6/models.py`): Pydantic models mirroring
   the Phase-6 API structure.

### Authentication Flow

1. `login()` → opens headless Chromium → saves `context.storage_state()` to
   `~/.config/pyphase6/session.json`
2. `_get_api_headers()` → reads saved session → extracts tokens from the
   double-encoded `persist:user` localStorage entry
3. Every API method → `with sync_playwright() as p: ctx = p.request.new_context(...)`

### CLI Command Pattern

```python
@app.command()
def command_name(...):
    client = get_authenticated_client()
    with console.status("Loading..."):
        try:
            result = client.api_method(...)
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)
```

## Git Workflow

Trunk-based development on `main`. Conventional commits are required —
`semantic-release` versions and publishes to GitHub Releases from `main`.

## Dependencies & Security

- Dependency updates are automated by Renovate (pinned versions).
- Never commit secrets. Credentials come from `PHASE6_USERNAME` /
  `PHASE6_PASSWORD` env vars (direnv + KeePassXC, see `.envrc`) or interactive
  prompts.
- Tests must stay offline: mock Playwright and the API (see existing tests).
