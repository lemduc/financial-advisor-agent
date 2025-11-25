# Financial Advisor Agent

An agent-first research and reminder assistant that helps individual investors monitor their portfolio, receive timely trade nudges, and surface evidence-backed market insights. The initial milestone focuses on a chat-based AI interface that can orchestrate data retrieval, structured analysis prompts, and scheduling logic while maintaining clear disclaimers.

## Key Capabilities (Target)

- Portfolio-aware chat assistant that remembers holdings, cost basis, and user preferences.
- Prompt templates for bull vs. bear cases, earnings digests, stock comparisons, macro trend calls, media cheat sheets, risk guidance, and weekly routines.
- Trade reminder engine that turns chat intents into scheduled notifications.
- Insight delivery that cites underlying metrics and flags uncertainty or missing data.

## System Overview

- **Interface:** REST/gRPC chat endpoint (FastAPI) plus optional CLI or UI client.
- **Agent Orchestration:** LangChain (or similar) managing system guardrails, analyst persona, and tool routing.
- **Data Services:** Market data providers (prices, fundamentals), earnings transcripts, news sentiment, macro indicators.
- **Storage:** PostgreSQL for portfolio state and reminder tasks, Redis for short-term conversation memory, vector store for research notes.
- **Scheduling:** APScheduler or Celery beat for reminders, weekly routines, and data refreshes.
- **Notifications:** Email/SMS push (SendGrid/Twilio) or calendar integrations for trade alerts.

## Getting Started

1. Clone the repository and ensure Python 3.11+ is available.
2. Create a virtual environment and install dependencies via `pip install -r requirements.txt`.
3. Create a `.env` file (copy from local template) and fill API keys, database DSN, and LLM credentials.
4. Launch the development server with `make dev`; run the test suite with `make test`.

## Project Status

- ✅ Repository initialization and planning documents.
- 🚧 Agent service scaffolding, data integrations, and reminder engine.
- 📅 Future work: UI integrations, advanced analytics, backtesting modules.

## Container & Deployment

- Build the Docker image locally with `docker build -t financial-advisor-agent:dev .`.
- Run the container via `docker run --rm -p 8000:8000 financial-advisor-agent:dev` and hit `http://localhost:8000/health`.
- Push images to `ghcr.io/lemduc/financial-advisor-agent` (or your chosen registry) for Kubernetes use.
- Apply the sample manifest in `k8s/deployment.yaml` after creating a `financial-advisor-agent-secrets` secret containing `database-url`, `redis-url`, and `openai-api-key` keys.

## Contributing

1. Fork and branch from `main`.
2. Add tests for new features.
3. Open a PR with a clear summary, screenshots (if UI), and test results.

## License

TBD.
