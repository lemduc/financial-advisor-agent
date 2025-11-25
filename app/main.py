import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.advisor_agent import FinancialAdvisorAgent
from app.schemas.chat import ChatRequest, ChatResponse

app = FastAPI(
    title="Financial Advisor Agent",
    description="""
    A portfolio-aware conversational assistant that helps individual investors monitor holdings,
    receive trade reminders, and get evidence-backed market insights.

    ## Features
    * Portfolio tracking and analysis
    * AI-powered market insights
    * Trade reminder scheduling
    * Evidence-backed recommendations
    """,
    version="0.1.0",
    contact={
        "name": "Financial Advisor Agent Team",
    },
)

# Configure CORS
# Get allowed origins from environment variable, defaulting to common development URLs
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:8080"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the advisor agent
advisor_agent = FinancialAdvisorAgent()


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    """
    Welcome endpoint that provides basic API information.

    Returns API name, version, and available documentation links.
    """
    return {
        "name": "Financial Advisor Agent API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Health check endpoint to confirm the service is operational.

    Returns a simple status message indicating the service is running.
    """
    return {"status": "ok", "message": "financial-advisor-agent online"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the financial advisor agent.

    Send a message to get investment insights, portfolio analysis, or market research.

    **Analysis Types:**
    - Bull/Bear case analysis
    - Earnings reviews
    - Stock comparisons
    - Risk assessments

    **Features:**
    - Session-based conversation history
    - Portfolio-aware responses
    - Evidence-backed insights with citations
    - Automatic disclaimer inclusion
    """
    # TODO: Fetch user portfolio from database if user_id provided
    portfolio = None

    # Process message through agent
    response = advisor_agent.process_message(
        message=request.message,
        session_id=request.session_id,
        user_id=request.user_id,
        portfolio=portfolio,
    )

    return response
