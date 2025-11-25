# Agent Project Plan

This document outlines the phased approach to deliver the financial advisor chat agent MVP and its subsequent enhancements.

## Vision

Deliver a portfolio-aware conversational assistant that turns natural-language prompts into data-backed insights, reminders, and structured workflows while maintaining compliance-friendly messaging and user trust.

## Guiding Principles

- Evidence over hype: every insight references underlying data and caveats.
- Automation with control: reminders and routines require explicit user confirmation and include snooze/cancel paths.
- Modularity: agents and tools are loosely coupled to accommodate new data sources or personas.
- Transparency: log prompts, responses, and model confidence for auditability.

## Timeline & Milestones

| Phase | Focus | Target Outcome |
| --- | --- | --- |
| 0. Foundation | Repo setup, environment scaffolding, lint/test baselines | Project ready for rapid iteration |
| 1. Core Agent MVP | Portfolio ingestion, chat endpoint, analyst prompt template | User can request bull/bear analysis for a holding |
| 2. Reminder Engine | Intent detection for reminders, scheduler integration, notification stubs | Chat intents become scheduled trade nudges |
| 3. Insight Expansion | Earnings digests, stock comparisons, sector trend detection | Agent delivers multi-template insights with data citations |
| 4. Risk & Routine | Risk playbook, weekly research routine generator, user preferences | Agent provides discipline-focused guidance |
| 5. UX & Delivery | Web/CLI client, notification delivery (email/SMS), monitoring | End-user experience hardened |

## Phase Detail

### Phase 0: Foundation

- Define tech stack (Python 3.11, FastAPI, LangChain, PostgreSQL, Redis, APScheduler).
- Establish repo structure (`app/`, `agents/`, `data/`, `tests/`, `docs/`).
- Configure linting (ruff, mypy) and testing (pytest) pipelines.
- Add `.env.example` and secret management guidelines.

### Phase 1: Core Agent MVP

- Data ingestion: mock portfolio loader (CSV or manual entry) persisted to Postgres.
- Build FastAPI endpoint for chat sessions with request/response schema.
- Implement LangChain agent with system prompt, persona layering, and history buffer.
- Create bull/bear/warning prompt template using structured portfolio + market data.
- Add unit tests for agent tool functions (portfolio fetch, valuation metrics).

### Phase 2: Reminder Engine

- Implement intent classifier to detect reminder/trade scheduling requests.
- Design reminder schema (user_id, ticker, trigger_type, parameters, status).
- Integrate APScheduler for cron/date/price triggers with placeholder notification handler.
- Add chat follow-up prompts to confirm reminder creation and provide management commands.
- Cover scheduling logic with integration tests.

### Phase 3: Insight Expansion

- Earnings pipeline: fetch or mock last five reports, compute surprises/YOY trends, format summary.
- Comparative analysis: combine fundamentals, macro indicators, and risk factors for Stock A vs. B.
- Trend scout: sector momentum detection using price/volume/ETF flows; include confidence scores.
- Media summarizer: ingest external transcript (YouTube API / manual upload) and condense into cheat sheet.
- Add regression tests (golden prompts) for each template to detect drift.

### Phase 4: Risk & Routine

- Risk management module: concentration analysis, volatility checks, diversification suggestions.
- Weekly routine generator: 60-minute checklist with links to agent tools and data pulls.
- User preferences: store risk tolerance, reminder windows, communication channels.
- Expand analytics logging for compliance and future auditing.

### Phase 5: UX & Delivery

- Implement simple web dashboard or CLI for chat, reminder management, and portfolio view.
- Connect notification service (SendGrid email, Twilio SMS) with opt-in confirmations.
- Add observability (structured logs, metrics, error tracking) and cost monitoring for LLM usage.
- Conduct beta testing, collect feedback, and prioritize backlog for next iteration.

## Risks & Mitigations

- **Data latency or gaps:** cache last successful pull, clearly flag stale data to user.
- **Model hallucinations:** enforce response schema validation and evidence checks before sending replies.
- **Scheduling reliability:** use persistent job store and add health checks for scheduler workers.
- **Compliance concerns:** include disclaimers, avoid direct investment advice wording, maintain audit logs.

## Open Questions

- Which market data provider offers the required mix of pricing, fundamentals, and transcripts within budget?
- What notification channels are mandatory for the first release (email vs. SMS vs. calendar)?
- Do we need multi-user authentication and access control in MVP or can we defer?

## Next Actions

1. Confirm data providers (prices, fundamentals, transcripts), secure sandbox keys, and log usage constraints in `docs/`.
2. Draft the initial Postgres schema (users, holdings, reminders, research notes) and stub migrations for local dev.
3. Scaffold the FastAPI `app/` skeleton with a `/chat` endpoint and LangChain agent harness wired to mock tools.
4. Prototype the bull/bear analysis flow end-to-end using sample portfolio data to validate prompt assembly and response formatting.
