# Financial Advisor Agent

[![Tests](https://github.com/lemduc/financial-advisor-agent/workflows/Tests/badge.svg)](https://github.com/lemduc/financial-advisor-agent/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file (copy from local template) and fill API keys, database DSN, and LLM credentials.
4. Launch the development server:
   ```bash
   make dev
   # Server runs at http://localhost:8000
   # API docs at http://localhost:8000/docs
   ```
5. Run the test suite:
   ```bash
   make test
   ```

## Project Status

### Phase 1: Core Agent MVP ✅ (Complete)
- ✅ Chat API endpoint with FastAPI (`POST /chat`)
- ✅ Financial advisor agent with mock LLM responses
- ✅ Bull/bear case analysis templates
- ✅ Portfolio data models (Pydantic schemas)
- ✅ Session management and conversation history
- ✅ Comprehensive test suite (68 tests passing)

### Phase 2: Reminder Engine 📅 (Planned)
- Intent detection for trade reminders
- APScheduler/Celery integration
- Notification delivery (email/SMS)
- Reminder management endpoints

### Phase 3+: Advanced Features 📅 (Future)
- Real LangChain + LLM integration
- Portfolio storage (SQLite/PostgreSQL)
- Data provider integrations (market data, earnings, news)
- UI integrations and advanced analytics

## Configuration

### CORS Settings

The API includes CORS middleware to allow frontend applications to connect. By default, it allows common development ports:

- `http://localhost:3000` (React, Next.js default)
- `http://localhost:3001` (Alternative React port)
- `http://localhost:5173` (Vite default)
- `http://localhost:8080` (General web dev)

To customize allowed origins, set the `CORS_ORIGINS` environment variable:

```bash
# .env file
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

For production, specify your exact domains:

```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## API Usage

### Chat Endpoint

Send a message to the financial advisor agent:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the bull case for AAPL?",
    "user_id": "user-123"
  }'
```

**Response:**
```json
{
  "message": "**Bull Case for AAPL**\n\n**Strengths:**\n- Strong revenue growth...",
  "session_id": "session-abc123",
  "timestamp": "2025-11-24T10:00:00Z",
  "analysis_type": "bull_bear",
  "confidence": "medium",
  "citations": [
    "P/E Ratio: 22.5 (mock data)",
    "Revenue Growth YoY: +15% (mock data)",
    "Profit Margin: 28% (mock data)"
  ],
  "disclaimer": "This is not financial advice..."
}
```

### Available Analysis Types

- **Bull/Bear Cases**: "What's the bull case for MSFT?"
- **Earnings Analysis**: "Show me the earnings for GOOGL"
- **Risk Assessment**: "What are the risks of TSLA?"
- **Stock Comparison**: "Compare AAPL vs MSFT"
- **General Queries**: "How can you help me?"

### Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation with Swagger UI.

### Connecting from Frontend

Example using **React** with `fetch`:

```javascript
// api/chat.js
export async function sendMessage(message, sessionId = null) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      user_id: 'user-123'
    }),
  });

  return response.json();
}

// Usage in component
const handleSend = async () => {
  const result = await sendMessage('What is the bull case for AAPL?');
  console.log(result.message, result.citations);
};
```

Example using **axios**:

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: (message, sessionId, userId) =>
    api.post('/chat', {
      message,
      session_id: sessionId,
      user_id: userId,
    }),
};
```

Example using **TypeScript** with type safety:

```typescript
interface ChatRequest {
  message: string;
  session_id?: string;
  user_id?: string;
}

interface ChatResponse {
  message: string;
  session_id: string;
  timestamp: string;
  analysis_type: string;
  confidence: string;
  citations: string[];
  disclaimer: string;
}

async function chat(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  return response.json();
}
```

## Testing

The project includes a comprehensive test suite with **68 tests** covering all core functionality.

### Test Coverage

- **Agent Logic** (`tests/test_agent.py`)
  - Analysis type detection (bull/bear, earnings, comparison, risk)
  - Ticker symbol extraction
  - Message processing and response generation
  - Session management
  - Citation generation

- **API Endpoints** (`tests/test_chat_endpoint.py`)
  - Chat endpoint functionality
  - Request/response validation
  - Session persistence
  - Error handling
  - OpenAPI schema validation

- **Data Models** (`tests/test_schemas.py`)
  - Pydantic schema validation
  - ChatRequest/ChatResponse models
  - Portfolio and Holding models
  - JSON serialization/deserialization

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agent.py -v

# Run specific test class
pytest tests/test_agent.py::TestAnalysisTypeDetection -v

# Run with coverage report
pytest --cov=app --cov=agents --cov-report=html
```

All 68 tests pass successfully with comprehensive coverage of agent logic, API endpoints, and data models.

### Continuous Integration

For GitHub Actions, add `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: make test
```

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
