# pyphase6

## Project Description
`pyphase6` is a modern Python client and Command Line Interface (CLI) for managing vocabulary in the Phase-6 web application. 

This project combines reverse-engineering the private API used by the Phase-6 Single Page Application (`https://lernen.phase-6.de/v2/#/manage`) with robust browser automation using Playwright. This allows `pyphase6` to handle complex authentication and website remote control while still quickly and reliably managing vocabulary items via HTTP where possible.

### Core Technologies
* **Dependency Management:** `uv` (for blazingly fast virtual environments and package resolution)
* **Browser Automation:** `playwright` (for remote controlling the browser, website interactions, and authentication)
* **HTTP Client:** `httpx` (for modern, asynchronous network requests)
* **Data Validation:** `pydantic` (for parsing and typing JSON API responses)
* **CLI Framework:** `typer` (for building an intuitive command-line interface)
* **Code Quality:** `pre-commit` hooks running `ruff` (linting/formatting) and `mypy` (static typing)
* **CI/CD:** GitHub Actions (for automated testing and quality checks)

---

## Step-by-Step Project Plan

### Phase 1: API Reconnaissance & Reverse Engineering
*Objective: Understand how the Phase-6 web app communicates with its backend servers.*
- [ ] Log into `https://lernen.phase-6.de/v2/#/manage` and open browser Developer Tools (Network tab).
- [ ] Isolate the authentication mechanism (e.g., Bearer token or session cookies).
- [ ] Identify and document the endpoint, HTTP method, and JSON payload required to **Read** the vocabulary list.
- [ ] Identify and document the endpoint required to **Create** a new vocabulary word.
- [ ] Identify and document the endpoint required to **Update** an existing word.
- [ ] Identify and document the endpoint required to **Delete** a word.
- [ ] Save sample JSON responses for all endpoints to use for data modeling.

### Phase 2: Modern Project Setup
*Objective: Initialize the repository with best-in-class Python tooling.*
- [ ] Initialize the project using `uv init pyphase6`.
- [ ] Update `pyproject.toml` with project metadata and core dependencies (`httpx`, `pydantic`, `typer`, `playwright`).
- [ ] Run `playwright install` to download required browser binaries.
- [ ] Add development dependencies (`pytest`, `ruff`, `mypy`, `pre-commit`).
- [ ] Create a `.pre-commit-config.yaml` to enforce `ruff` formatting/linting and `mypy` type-checking.
- [ ] Initialize Git, run `pre-commit install`, and make the first commit.

### Phase 3: Core Library Development
*Objective: Build the internal Python API client.*
- [ ] **Data Models:** Create Pydantic classes (e.g., `VocabItem`, `VocabList`) based on the JSON samples gathered in Phase 1.
- [ ] **Client Class:** Create a `Phase6Client` class that wraps `httpx.Client` for fast API calls and integrates a Playwright context for automated browser interactions.
- [ ] **Authentication:** Implement a `login(username, password)` method using Playwright to handle the browser login flow and extract the authorized session token/cookies.
- [ ] **CRUD Operations:** Implement the core API methods:
  - [ ] `get_vocabulary()`
  - [ ] `add_vocabulary(item)`
  - [ ] `update_vocabulary(item_id, data)`
  - [ ] `delete_vocabulary(item_id)`
- [ ] **Error Handling:** Define custom exceptions (e.g., `AuthError`, `APIConnectionError`) for robust failure states.

### Phase 4: CLI Implementation
*Objective: Make the tool usable from the terminal.*
- [ ] Initialize a Typer app instance.
- [ ] Create a `login` command that securely prompts for a password and saves a temporary session token.
- [ ] Create a `list` command to print vocabulary to the terminal (consider using the `rich` library for nice tables).
- [ ] Create an `add` command to add a single word via terminal arguments.
- [ ] Create a `sync` or `import` command to bulk-upload vocabulary from a local CSV or JSON file.

### Phase 5: Testing & CI/CD Pipeline
*Objective: Ensure code reliability and automate quality checks.*
- [ ] Write `pytest` unit tests for data models and mocked API responses.
- [ ] Create a `.github/workflows/ci.yml` file.
- [ ] Configure the GitHub Action to check out code, install `uv`, and run `pre-commit` on every pull request.
- [ ] Configure the GitHub Action to run the `pytest` test suite.
- [ ] Finalize `README.md` with installation and usage instructions.