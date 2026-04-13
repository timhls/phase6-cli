# CHANGELOG


## v0.2.0 (2026-04-13)

### Bug Fixes

- Resolve mypy type errors
  ([`7d1d46c`](https://github.com/timhls/phase6-cli/commit/7d1d46c9c4ce9e0816104a22c86d7e333d464c43))

### Chores

- Format code with ruff
  ([`e0d8be6`](https://github.com/timhls/phase6-cli/commit/e0d8be6e2050cdc826635c77e1ffd2a80588b6bd))

- Re-format with ruff
  ([`2bfe770`](https://github.com/timhls/phase6-cli/commit/2bfe7706a6c062dbe9596bc494549b0c02cabd41))

### Documentation

- Add GitHub Copilot instructions for future sessions
  ([`f946f48`](https://github.com/timhls/phase6-cli/commit/f946f48418b07675439b5caf4e6fcf65418e1c3c))

Add comprehensive copilot-instructions.md covering: - Build, test, and lint commands using uv -
  Three-layer architecture (CLI → Client → Models) - Key convention patterns for testing and API
  requests - Session management and Playwright usage patterns - Release process with
  semantic-release

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>

- Migrate CLAUDE.md to AGENTS.md
  ([`4b5ebf6`](https://github.com/timhls/phase6-cli/commit/4b5ebf66f287f4b8a1c02e3cddcd0ea18250ba53))

### Features

- Add unit management support and summarize session updates
  ([`7e46661`](https://github.com/timhls/phase6-cli/commit/7e466613f136f3d5d53819e6df28b54600f27d92))

### Testing

- Update cli tests to include unit_id parameter
  ([`fad5c00`](https://github.com/timhls/phase6-cli/commit/fad5c0075b3c0e71fc87acd4ecd696a66bf399d3))


## v0.1.3 (2026-03-06)

### Bug Fixes

- Remove unused httpx dep, add rich as direct dep, fix get_vocabulary limit/offset, add tests
  ([`7c4bbbb`](https://github.com/timhls/phase6-cli/commit/7c4bbbb9526786b4933e8cc93721b32a549f4380))

Co-authored-by: timhls <11960973+timhls@users.noreply.github.com>

### Chores

- **claude**: Allow adding renovate.json
  ([`274e5f7`](https://github.com/timhls/phase6-cli/commit/274e5f7d54338f21f4d2ae629ef18fc69ec041dc))

Automatically approve `git add renovate.json` commands for Claude.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.1.2 (2026-03-01)

### Bug Fixes

- **deps**: Configure renovate with pep621 manager for uv
  ([`e9a8666`](https://github.com/timhls/phase6-cli/commit/e9a8666ea7da341a0c1c7d3dcb8c96e20b0201c8))

The Renovate App failed to initialize because it does not recognize "uv" as an explicitly enabled
  manager. Renovate natively supports `uv` projects (and `uv.lock`) via the `pep621` manager.
  Replaced `"uv"` with `"pep621"` in `renovate.json`.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- **claude**: Update allowed permissions for git operations
  ([`bb02ef2`](https://github.com/timhls/phase6-cli/commit/bb02ef28ce37cd863ba0dbe66e2f1e4cf3928950))

Update `.claude/settings.json` to automatically allow specific git commands (commit, push, and
  targeted adds) so the assistant can perform version control tasks more smoothly.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **deps**: Configure renovate and strictly pin all dependencies
  ([`20409d0`](https://github.com/timhls/phase6-cli/commit/20409d0992defe727e3e3ed419a2b3048eb47b4d))

- Added `renovate.json` configuring the GitHub App to update `uv` packages and `github-actions`. -
  Set `rangeStrategy: pin` in the Renovate config to automatically replace ranges with strict
  versions. - Updated `pyproject.toml` to strictly pin `httpx`, `playwright`, `pydantic`, `typer`,
  `mypy`, `pytest`, `python-semantic-release`, and `ruff` to their exact resolved versions from
  `uv.lock`. - Synchronized `uv.lock` with strictly pinned `==` declarations.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Documentation

- Rewrite CLAUDE.md according to context engineering best practices
  ([`d4a899c`](https://github.com/timhls/phase6-cli/commit/d4a899c88cb7980b4493d2e4d57bdc613d08cfbe))

Refactored `CLAUDE.md` to be shorter and more focused based on best practices for coding agents. It
  now cleanly answers WHY, WHAT, and HOW without bloating the context window with resolved task
  lists or linters. Also committed a small `uv.lock` change reflecting the recent version bump.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Update README.md to use uv instead of poetry
  ([`28d0862`](https://github.com/timhls/phase6-cli/commit/28d08629343a372652058c223cf8b3e71a726eff))

Migrated the README installation, usage, and development instructions to use `uv sync` and `uv run`
  instead of `poetry`. Replaced the outdated `pre-commit` command with explicit `ruff` and `mypy`
  commands.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.1.1 (2026-03-01)

### Bug Fixes

- **ci**: Remove redundant build and unsupported registry publish
  ([`78db060`](https://github.com/timhls/phase6-cli/commit/78db0603062b7d88b1ff8b22207a799b2fcb6c15))

GitHub Packages does not natively support Python packages, so we removed the `uv publish` step that
  was failing with a 404 error. `semantic-release publish` natively runs the build command specified
  in `pyproject.toml` (`uv build`) and automatically uploads the resulting `.whl` and `.tar.gz`
  files to the GitHub Release. We removed the redundant `uv build` step to prevent the 422 asset
  collision error.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Continuous Integration

- Fix github packages publish url
  ([`c5fae10`](https://github.com/timhls/phase6-cli/commit/c5fae108266d761e0aa509d736dcddabe267386a))

Update the publish URL for GitHub Packages to the correct endpoint to avoid a 404 error during uv
  publish.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


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
