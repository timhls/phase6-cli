# CHANGELOG


## v0.1.0 (2026-03-01)

### Bug Fixes

- Resolve mypy typing errors in scripts
  ([`3a404ca`](https://github.com/timhls/phase6-cli/commit/3a404ca62cfc6e24dfca66d3a2b5846b2e714bd2))

Provide empty strings as fallbacks for os.environ.get() in test scripts so mypy doesn't complain
  about passing Optional[str] to functions expecting str.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Build System

- Switch to uv native build backend
  ([`935dfab`](https://github.com/timhls/phase6-cli/commit/935dfab9b7b2ff872381d36e4ac099f7b7fdad43))

Update pyproject.toml to use uv_build as the project build system. This enables proper packaging and
  installation of the CLI entry point in the local environment.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- Add claude settings configuration
  ([`2176599`](https://github.com/timhls/phase6-cli/commit/217659906835fdf27163cf1740ebbedadf2839a9))

Add `.claude/settings.json` to persist allowed command permissions for Claude.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add gitignore and remove build artifacts
  ([`452ebb1`](https://github.com/timhls/phase6-cli/commit/452ebb1f5bbc1c758892090c95a550aa71d983e8))

- Clean up debug artifacts and format scripts
  ([`2c93df5`](https://github.com/timhls/phase6-cli/commit/2c93df5b53a400faf930442a044b92f8ee06df6b))

- Remove temporary screenshots, HTML dumps, and JSON responses generated during the
  reverse-engineering process. - Ignore `.envrc` in `.gitignore`. - Apply `ruff` auto-formatting to
  exploration and test scripts.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Remove build artifacts from git
  ([`8a762f6`](https://github.com/timhls/phase6-cli/commit/8a762f6cc8c6c4a3298594a1dbe1a61f7c784f84))

### Continuous Integration

- Add GitHub Actions pipeline and update docs
  ([`b65fbe7`](https://github.com/timhls/phase6-cli/commit/b65fbe77c9d0d2a0b5217b5f7212e109d2f29d8d))

- Create .github/workflows/ci.yml for automated testing and linting - Update README.md with
  comprehensive installation and usage instructions - Mark all remaining tasks as completed in
  CLAUDE.md

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Rewrite pipeline with uv and semantic-release
  ([`f097353`](https://github.com/timhls/phase6-cli/commit/f097353c4fd0b78c723b087860d10f469f553995))

- Replace pre-commit and poetry with uv for testing and linting - Integrate python-semantic-release
  to automatically bump versions and generate changelogs based on conventional commits - Add release
  job to build the package with uv and publish it to GitHub Packages PyPI registry - Fix linting
  errors in script files

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Documentation

- Complete checkboxes in CLAUDE.md project plan
  ([`cf9dd3b`](https://github.com/timhls/phase6-cli/commit/cf9dd3b3dcd317d525d34e5897f872d5dc3403e8))

### Features

- Implement bulk import command for CSV and JSON files
  ([`4e2c03d`](https://github.com/timhls/phase6-cli/commit/4e2c03d1465d858cea9631fecb4664bfaffa08e5))

- Implement direct API integration for vocabulary management
  ([`2b774c0`](https://github.com/timhls/phase6-cli/commit/2b774c0d80d696a947d7bffc0372e284db79dc9d))

- Refactor Phase6Client to use APIRequestContext and direct JSON REST calls instead of UI automation
  for major performance gains. - Implement add_vocabulary, update_vocabulary, and delete_vocabulary
  in Phase6Client. - Add `add`, `update`, and `delete` commands to the CLI. - Update `vocab` command
  to automatically strip HTML tags and audio snippets from console output. - Update CardContent and
  VocabItem Pydantic models to support new payload references like `unitIdToOwner`.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Project setup with CLI and client skeleton
  ([`e9030c0`](https://github.com/timhls/phase6-cli/commit/e9030c033c249e942bb4392446cd09339ba87e27))

- Initialize uv project with dependencies (httpx, pydantic, typer, playwright) - Setup pre-commit
  (ruff, mypy) - Setup initial models and client structure - Implement Typer CLI entrypoint

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Testing

- Write comprehensive pytest unit tests for models, client, and CLI
  ([`54e8044`](https://github.com/timhls/phase6-cli/commit/54e80442480f56d592eadc73c35204a532eadbe7))
