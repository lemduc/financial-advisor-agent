# Copilot Instructions

## Repository Snapshot
- Core aim: build a portfolio-aware financial advisor chat agent (see `README.md`).
- Planning reference: follow milestones and deliverables documented in `docs/agent-project-plan.md`.
- Current tree is minimal; scaffold new modules under `app/`, `agents/`, `data/`, `tests/`, `docs/` per the project plan.

## Development Stack
- Primary runtime: Python 3.11+ with FastAPI for the chat API, LangChain (or similar) for agent orchestration, APScheduler/Celery for reminders.
- Persistence targets: PostgreSQL for holdings/reminders, Redis for state caching, vector store for research notes.
- When mocking integrations, isolate API adapters in `app/integrations/` so providers can be swapped without touching agent logic.

## Workflows
- Create a virtualenv, install packages via `pip install -r requirements.txt` (to be added alongside stack work).
- Formatting and linting: adopt `ruff` + `mypy`; ensure markdown files satisfy MD022/MD032 (leave blank lines around headings and lists).
- Tests should live in `tests/` with `pytest`; provide fixtures for portfolio snapshots and API responses.
- Add `make` targets for `make dev` (FastAPI + scheduler) and `make test` once the commands exist; keep docs in sync when commands change.

## Agent Patterns
- Build reusable prompt templates per capability (bull/bear, earnings digest, comparisons, etc.) under `agents/prompts/`.
- Keep prompts data-driven: supply structured tables (prices, fundamentals, surprises) instead of free-form text.
- Implement tool abstractions for market data, reminders, and summarization; inject via LangChain tools with clear IO contracts.
- Enforce response post-processing that adds disclaimers, cites metrics, and flags missing data before returning to the user.

## Scheduling & Notifications
- Reminders should persist in the database, enqueue jobs via APScheduler/Celery, and integrate with notification stubs (email/SMS) under `app/notifications/`.
- Provide chat confirmation flows for creating/updating/canceling reminders; document any cron syntax exposed to users.

## Documentation Expectations
- Update `README.md` when high-level architecture or onboarding changes.
- Extend `docs/agent-project-plan.md` with phase progress, risks, and decisions as milestones evolve.
- Include run/test instructions in PR descriptions; capture new prompts or workflows in `docs/` for future agents.

## Miscellaneous
- Default to ASCII in files unless an existing file uses emojis (current README uses ✅/🚧/📅; keep consistency).
- Log prompts/responses and tag them with session IDs to support future compliance reviews.
- When unsure about provider selections or notification channels, surface as TODOs referencing the "Open Questions" section of the project plan.
