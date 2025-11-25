# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Financial Advisor Agent is a portfolio-aware conversational assistant that helps individual investors monitor holdings, receive trade reminders, and get evidence-backed market insights. The system uses LangChain agent orchestration with FastAPI for the chat API, structured data retrieval, and scheduling logic.

## Development Commands

### Environment Setup
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Running the Application
```bash
make dev                    # Start FastAPI server with hot reload (uvicorn app.main:app --reload)
uvicorn app.main:app --reload  # Alternative direct command
```

### Testing & Quality
```bash
make test                   # Run pytest test suite
pytest                      # Direct pytest invocation
pytest tests/test_health.py # Run specific test file

make lint                   # Run ruff linter
ruff check .                # Direct ruff invocation

make typecheck              # Run mypy type checking
mypy app                    # Direct mypy invocation
```

### Docker Operations
```bash
make docker-build           # Build image as financial-advisor-agent:dev
make docker-run             # Run container on port 8000
docker run --rm -p 8000:8000 financial-advisor-agent:dev
```

### Kubernetes Deployment
```bash
make kube-apply             # Apply k8s/deployment.yaml
make kube-delete            # Delete deployment

# Prerequisites: Create secret with database-url, redis-url, openai-api-key
kubectl create secret generic financial-advisor-agent-secrets \
  --from-literal=database-url=<DSN> \
  --from-literal=redis-url=<REDIS_URL> \
  --from-literal=openai-api-key=<API_KEY>
```

## Architecture

### Intended Module Structure
The codebase follows a phased development plan (see `docs/agent-project-plan.md`). Expected directory layout:

- `app/` - FastAPI application, endpoints, service layer
- `agents/` - LangChain agent orchestration, prompt templates
- `agents/prompts/` - Reusable templates (bull/bear analysis, earnings digest, stock comparisons, risk guidance, weekly routines)
- `app/integrations/` - Data provider adapters (market data, earnings transcripts, news sentiment, macro indicators)
- `app/notifications/` - Notification stubs for email/SMS delivery
- `data/` - Data loading, portfolio ingestion, mock datasets
- `tests/` - pytest test suite with fixtures for portfolio snapshots and API responses
- `docs/` - Planning documents, workflow guides, prompt documentation

### Data Flow Architecture
1. User sends natural language request to `/chat` endpoint (FastAPI)
2. LangChain agent analyzes intent, routes to appropriate tools/prompts
3. Tools fetch data via adapters in `app/integrations/` (prices, fundamentals, transcripts)
4. Structured data flows into prompt templates in `agents/prompts/`
5. Agent response includes citations, disclaimers, and flags for missing/stale data
6. Reminder intents persist to PostgreSQL and schedule via APScheduler/Celery
7. Scheduled jobs trigger notifications through `app/notifications/`

### Storage & Caching
- PostgreSQL: portfolio holdings, cost basis, reminder tasks, user preferences
- Redis: short-term conversation memory, session state caching
- Vector store: research notes and historical analysis (future phase)

### Agent Design Patterns
- Prompts must be data-driven: supply structured tables (prices, fundamentals, surprises) rather than free-form text
- All agent responses require post-processing to add disclaimers, cite metrics, and flag missing data
- Tool abstractions injected via LangChain tools with clear input/output contracts
- System maintains guardrails via analyst persona and tool routing constraints

### Reminder & Scheduling
- Reminders persist in database with schema: user_id, ticker, trigger_type, parameters, status
- APScheduler/Celery handles cron/date/price triggers
- Chat provides confirmation flows for creating/updating/canceling reminders
- Notification delivery via SendGrid (email) or Twilio (SMS)

## Development Guidelines

### Code Quality
- Use `ruff` for linting and `mypy` for type checking
- All new features require pytest tests
- Provide fixtures for portfolio snapshots and API responses in tests
- Log prompts/responses with session IDs for compliance auditing

### Prompt Development
- Create reusable templates per capability under `agents/prompts/`:
  - Bull/bear case analysis
  - Earnings digest (last five reports, surprises, YOY trends)
  - Stock comparisons (fundamentals, macro, risk factors)
  - Sector trend detection (price/volume/ETF flows with confidence scores)
  - Media cheat sheets (transcript summarization)
  - Risk guidance (concentration, volatility, diversification)
  - Weekly research routines (60-minute checklists)
- Include golden prompt regression tests to detect model drift

### Data Integration
- Isolate API adapters in `app/integrations/` so providers can be swapped without touching agent logic
- Cache last successful data pull and clearly flag stale data to users
- Enforce response schema validation to prevent hallucinations
- Surface data provider decisions as TODOs when uncertain

### Documentation Standards
- Update `README.md` for architectural or onboarding changes
- Extend `docs/agent-project-plan.md` with phase progress, risks, and decisions
- Document new prompts or workflows in `docs/` for future reference
- Include run/test instructions in PR descriptions
- Maintain markdown formatting: leave blank lines around headings and lists (MD022/MD032)

### Style Conventions
- Use ASCII in files unless existing file contains emojis (README uses ✅/🚧/📅)
- Follow project's phased milestones (Phase 0-5) documented in `docs/agent-project-plan.md`
- Reference planning document for open questions about provider selection or notification channels

## Configuration & Secrets

Create `.env` file with:
- Database DSN (PostgreSQL)
- Redis URL
- LLM credentials (OpenAI API key or alternative)
- Market data provider API keys
- Notification service credentials (SendGrid/Twilio)

For Kubernetes deployment, create `financial-advisor-agent-secrets` secret containing `database-url`, `redis-url`, and `openai-api-key` keys.

## Compliance & Risk
- Include disclaimers in all responses
- Avoid direct investment advice wording
- Flag uncertainty or missing data explicitly
- Maintain audit logs with prompt/response tagging
- Cache data and mark staleness to handle latency/gaps
- Use persistent job store and health checks for scheduler reliability
