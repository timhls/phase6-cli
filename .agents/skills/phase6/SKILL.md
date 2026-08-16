---
name: phase6
description: >
  Manage Phase-6 vocabulary (lernen.phase-6.de) — list subjects and units, browse
  vocabulary cards, add/update/delete single cards, and bulk import cards from
  CSV or JSON files. Handles the Phase-6 browser-based login flow and wraps the
  private server.integration REST API.
license: MIT
compatibility: Requires Python 3.14.7, uv, Playwright Chromium
  (uv run playwright install chromium), and a Phase-6 account.
metadata:
  author: timoh
  version: "1.1.0"
---

# phase6

`pyphase6` is a Python client and CLI for the Phase-6 vocabulary platform
(`https://lernen.phase-6.de`). It reverse-engineers the private SPA API: a
headless Playwright browser performs the login flow and saves the session, then
all vocabulary CRUD runs as fast direct JSON REST calls through Playwright
request contexts.

## When to use

- "Show me my Phase-6 subjects / vocabulary books"
- "Add this word to my Chinese vocabulary list"
- "Import these 200 words into Phase-6 unit Lesson 3"
- "Update / delete a vocabulary card in Phase-6"
- "List the cards in subject X as JSON"
- "Which units exist in subject X?"

## How to invoke

All commands use the `uv run pyphase6` entry point from the repo root.

### Authentication

```bash
# Interactive (prompts for credentials)
uv run pyphase6 login

# Non-interactive (flags or PHASE6_USERNAME / PHASE6_PASSWORD env vars)
uv run pyphase6 login --username user@example.com --password 'secret'
```

Saves the session to `~/.config/pyphase6/session.json`. Must be re-run whenever
the session expires (see Gotchas).

### Subjects

```bash
# Rich table
uv run pyphase6 subjects

# Agent-parseable JSON (full IDs, no truncation)
uv run pyphase6 subjects --json
```

### Vocabulary

```bash
# Rich table (card IDs truncated to 8 chars, HTML stripped)
uv run pyphase6 vocab <SUBJECT_ID>

# Agent-parseable JSON (full card IDs, raw HTML content preserved)
uv run pyphase6 vocab <SUBJECT_ID> --json

# Fetch more items
uv run pyphase6 vocab <SUBJECT_ID> --limit 500
```

### Cards

```bash
# Add (auto-wraps plain text in <p>...</p>; pass raw HTML to control formatting)
uv run pyphase6 add <SUBJECT_ID> "Question" "Answer"
uv run pyphase6 add <SUBJECT_ID> "Question" "Answer" --unit "Lesson 3"

# Update
uv run pyphase6 update <SUBJECT_ID> <CARD_ID> "New Question" "New Answer"

# Delete
uv run pyphase6 delete <CARD_ID>

# Delete a unit
uv run pyphase6 delete-unit <UNIT_ID>
```

### Bulk import

```bash
uv run pyphase6 import <SUBJECT_ID> cards.json --unit "Lesson 3"
uv run pyphase6 import <SUBJECT_ID> cards.csv
```

Accepted formats (`.csv` with headers, or `.json` array of objects). Keys may be
`question`/`front`/`q` and `answer`/`back`/`a`. Units are looked up by name and
created on demand (`--unit`).

**JSON example:**

```json
[
  {"question": "Hello", "answer": "Hallo"},
  {"question": "<p>儿子</p>", "answer": "<p>son<br/>érzi</p>"}
]
```

## Configuration

| Env var | Purpose | Default |
|---|---|---|
| `PHASE6_USERNAME` | Login email (used when `--username` not passed) | prompt |
| `PHASE6_PASSWORD` | Login password (used when `--password` not passed) | prompt |

Credentials can be supplied via direnv + KeePassXC (see `.envrc`); no secrets
are stored in the repo.

## Authentication & session

- `login` drives a headless Chromium through the Phase-6 login form and stores
  a Playwright `storage_state` at `~/.config/pyphase6/session.json`.
- Every API call reads that file, extracts `jossoSessionId` (`x-jauthtoken`),
  `email` (`x-lbtoken`), and `userDnsId` (`owner_id` in REST paths) from the
  double-JSON-encoded `persist:user` localStorage entry.
- There is **no expiry detection**: a stale session surfaces later as
  `AuthError` or `APIConnectionError`. The remedy is always
  `uv run pyphase6 login` again.

## Gotchas

1. **Rich-text contract**: the server stores `question`/`answer` as HTML. The
   CLI wraps plain text in `<p>...</p>` only when it does not already start
   with `<p>`. Pass raw HTML to control formatting exactly.
2. **Multi-line answers**: separate lines (e.g. translation + Pinyin) with
   `<br/>` inside the HTML — Phase-6 renders them as separate lines.
3. **Duplicates are rejected server-side** (`DUPLICATED_CONTENT`): during bulk
   imports, existing items fail individually with `APIConnectionError` and the
   batch continues. A final `N/M imported` with N < M usually just means the
   duplicates were skipped — safe to ignore for re-runs.
4. **Table output truncates card IDs** to the first 8 chars. Use `--json` when
   you need the full UUID for `update`/`delete`.
5. **Audio markers**: card content may contain junk like
   `Sohn[{~hefei_huang_verlag*...~}]`. The table view strips everything from
   `[` when `~` is present; `--json` keeps the raw string.
6. **Default unit**: cards added without `--unit` land in the synthetic unit
   `0000-{subject_id}` (the subject's "unfiled" unit), not a real unit entity.
7. **Double status check**: every API response is validated twice — HTTP
   status and the JSON envelope's `httpCode` field. Both must be 200.
8. **IDs are client-generated UUIDs** minted by the CLI; card/unit REST paths
   are prefixed with the account's `owner_id` (`userDnsId`).
9. **No session refresh**: if commands suddenly fail mid-session, re-run
   `login` — do not retry the same failing call in a loop.
10. **`--json` keeps raw HTML** (`<p>`, `<br/>`, audio markers); strip or parse
    it client-side as needed.

## Further reading

- `scripts/pyphase6/` — source code (`cli.py`, `client.py`, `models.py`)
- `tests/` — offline test suite (Playwright fully mocked)
- Phase-6 web app: `https://lernen.phase-6.de/v2/#/manage`
