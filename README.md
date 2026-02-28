# pyphase6

A modern, blazingly fast Python client and Command Line Interface (CLI) for managing vocabulary in the Phase-6 web application.

This tool reverse-engineers the private Phase-6 Single Page Application API, combining robust browser automation (via Playwright) for complex authentication with lightning-fast native REST API calls for vocabulary CRUD operations.

## Features

- **Automated Login**: Uses a headless Playwright instance to perform the login flow and extract the required `x-jauthtoken` session tokens.
- **Fast CRUD API**: Direct JSON requests to the Phase-6 backend, skipping slow browser UI navigation entirely.
- **Bulk Import**: Quickly upload hundreds of vocabulary cards from CSV or JSON files.
- **Rich Terminal UI**: Beautiful console output and progress bars built with `typer` and `rich`.

## Installation

Ensure you have Python 3.11+ installed. We recommend using `poetry` or `uv` to manage your environment.

```bash
# Clone the repository
git clone https://github.com/timhls/phase6-cli.git
cd phase6-cli

# Install dependencies using Poetry
poetry install

# Install Playwright browsers (needed for the login flow)
poetry run playwright install chromium
```

## Usage

### 1. Authenticate

Before doing anything, you need to log in to generate your session token. This opens a headless Chromium browser in the background.

```bash
poetry run pyphase6 login
```
*You will be prompted securely for your Phase-6 email and password.*

### 2. View Your Subjects

List all the subjects (vocabulary books or lists) you currently own:

```bash
poetry run pyphase6 subjects
```
*Take note of the `Subject ID` from the output, as you will need it to manage cards within that subject.*

### 3. List Vocabulary

View all vocabulary items inside a specific subject:

```bash
poetry run pyphase6 vocab <SUBJECT_ID>
```
*(Use `--limit <N>` to change the number of items fetched).*

### 4. Manage Single Cards

Add, update, or delete a single vocabulary card:

```bash
# Add a new card
poetry run pyphase6 add <SUBJECT_ID> "Your Question" "Your Answer"

# Update an existing card
poetry run pyphase6 update <SUBJECT_ID> <CARD_ID> "New Question" "New Answer"

# Delete a card
poetry run pyphase6 delete <CARD_ID>
```

### 5. Bulk Import

You can bulk import many cards at once using a CSV or JSON file.

**CSV Format (`import.csv`)**
```csv
question,answer
"Hello","Hallo"
"Goodbye","Auf Wiedersehen"
```

**JSON Format (`import.json`)**
```json
[
  {"question": "Dog", "answer": "Hund"},
  {"question": "Cat", "answer": "Katze"}
]
```

Run the import command:
```bash
poetry run pyphase6 import <SUBJECT_ID> import.csv
```

## Development

This project uses `ruff` for linting/formatting, `mypy` for static type checking, and `pytest` for unit testing.

```bash
# Run all tests
poetry run pytest

# Run pre-commit checks
poetry run pre-commit run --all-files
```

## License
MIT License
