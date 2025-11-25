"""Financial advisor agent implementation."""

import uuid
from datetime import datetime
from typing import Optional

from app.schemas.chat import ChatResponse
from app.schemas.portfolio import Portfolio


class FinancialAdvisorAgent:
    """
    Agent that provides financial analysis and insights.

    Currently uses mock responses. Will be replaced with LangChain integration.
    """

    SYSTEM_PROMPT = """You are a knowledgeable financial advisor assistant helping individual investors.

Your role:
- Provide evidence-backed market insights
- Analyze portfolio holdings with bull/bear perspectives
- Surface relevant metrics and data
- Flag uncertainty and missing data clearly
- Always include appropriate disclaimers

Principles:
- Evidence over hype: cite underlying data and metrics
- Transparency: acknowledge limitations and data gaps
- Risk awareness: highlight potential downsides
- No direct investment advice: provide information for informed decision-making
"""

    def __init__(self):
        """Initialize the financial advisor agent."""
        self.sessions: dict[str, list[dict]] = {}

    def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        portfolio: Optional[Portfolio] = None,
    ) -> ChatResponse:
        """
        Process a user message and generate a response.

        Args:
            message: User's input message
            session_id: Optional session ID for conversation continuity
            user_id: Optional user ID for portfolio context
            portfolio: Optional portfolio data for context

        Returns:
            ChatResponse with agent's analysis
        """
        # Generate or use existing session ID
        if not session_id:
            session_id = f"session-{uuid.uuid4().hex[:8]}"

        # Store message in session history
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {"role": "user", "content": message, "timestamp": datetime.utcnow()}
        )

        # Detect analysis type from message
        analysis_type = self._detect_analysis_type(message)

        # Generate mock response based on analysis type
        response_message = self._generate_mock_response(
            message, analysis_type, portfolio
        )

        # Mock citations
        citations = self._generate_mock_citations(analysis_type, portfolio)

        # Store agent response in session
        self.sessions[session_id].append(
            {
                "role": "assistant",
                "content": response_message,
                "timestamp": datetime.utcnow(),
            }
        )

        return ChatResponse(
            message=response_message,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            analysis_type=analysis_type,
            confidence="medium",
            citations=citations,
        )

    def _detect_analysis_type(self, message: str) -> str:
        """Detect the type of analysis requested from the message."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["bull", "bear", "case"]):
            return "bull_bear"
        elif any(word in message_lower for word in ["earnings", "report"]):
            return "earnings"
        elif any(
            word in message_lower for word in ["compare", "comparison", "versus", "vs"]
        ):
            return "comparison"
        elif any(word in message_lower for word in ["risk", "volatility", "downside"]):
            return "risk"
        else:
            return "general"

    def _generate_mock_response(
        self, message: str, analysis_type: str, portfolio: Optional[Portfolio] = None
    ) -> str:
        """Generate a mock response based on analysis type."""
        # Extract ticker if mentioned
        ticker = self._extract_ticker(message)

        if analysis_type == "bull_bear":
            if "bull" in message.lower():
                return self._mock_bull_case(ticker)
            elif "bear" in message.lower():
                return self._mock_bear_case(ticker)
            else:
                return self._mock_balanced_view(ticker)

        elif analysis_type == "earnings":
            return f"Here's an earnings analysis for {ticker or 'your holdings'}:\n\nMock earnings data will be displayed here with YoY comparisons and surprises."

        elif analysis_type == "risk":
            return f"Risk analysis for {ticker or 'your portfolio'}:\n\nMock risk metrics including volatility, concentration, and diversification scores."

        else:
            portfolio_context = ""
            if portfolio and portfolio.holdings:
                tickers = [h.ticker for h in portfolio.holdings[:3]]
                portfolio_context = f" I can see you hold {', '.join(tickers)}."

            return f"I'm here to help with your investment research.{portfolio_context} You can ask me about bull/bear cases, earnings analysis, stock comparisons, or risk assessments."

    def _mock_bull_case(self, ticker: Optional[str]) -> str:
        """Generate mock bull case analysis."""
        ticker_display = ticker or "this stock"
        return f"""**Bull Case for {ticker_display.upper()}**

**Strengths:**
- Strong revenue growth trajectory (mock: +15% YoY)
- Expanding profit margins (mock: 25% → 28%)
- Market leadership in key segments
- Robust balance sheet with low debt

**Catalysts:**
- New product launches expected in Q2
- Expanding into high-growth markets
- Operational efficiency improvements

**Valuation:**
- Trading at reasonable P/E relative to growth (mock: 22x vs sector 25x)
- Free cash flow generation supports current valuation

Note: This is a mock analysis. Real data integration pending."""

    def _mock_bear_case(self, ticker: Optional[str]) -> str:
        """Generate mock bear case analysis."""
        ticker_display = ticker or "this stock"
        return f"""**Bear Case for {ticker_display.upper()}**

**Risks:**
- Increasing competition in core markets
- Potential margin compression (mock: concerns about input costs)
- High valuation relative to historical averages
- Regulatory headwinds in key jurisdictions

**Concerns:**
- Customer concentration risk (top 3 customers = 40% revenue)
- Execution risk on new initiatives
- Macroeconomic sensitivity

**Valuation:**
- Premium valuation leaves little room for disappointment
- Multiple expansion may reverse in downturn

Note: This is a mock analysis. Real data integration pending."""

    def _mock_balanced_view(self, ticker: Optional[str]) -> str:
        """Generate mock balanced analysis."""
        ticker_display = ticker or "this stock"
        return f"""**Analysis for {ticker_display.upper()}**

**Bull Factors:**
- Revenue growth momentum
- Strong competitive position
- Margin expansion potential

**Bear Factors:**
- Valuation concerns
- Market competition intensifying
- Execution risks on growth plans

**Recommendation:**
Monitor upcoming earnings and sector trends. Consider position sizing relative to overall portfolio risk.

Note: This is a mock analysis. Real data integration pending."""

    def _extract_ticker(self, message: str) -> Optional[str]:
        """Extract stock ticker from message (simple pattern matching)."""
        import re

        # Look for uppercase sequences of 1-5 letters (common ticker pattern)
        pattern = r"\b[A-Z]{1,5}\b"
        matches = re.findall(pattern, message)

        # Filter out common words that aren't tickers
        excluded = {"I", "A", "MY", "THE", "FOR", "AND", "OR"}
        tickers = [m for m in matches if m not in excluded]

        return tickers[0] if tickers else None

    def _generate_mock_citations(
        self, analysis_type: str, portfolio: Optional[Portfolio] = None
    ) -> list[str]:
        """Generate mock data citations."""
        if analysis_type == "bull_bear":
            return [
                "P/E Ratio: 22.5 (mock data)",
                "Revenue Growth YoY: +15% (mock data)",
                "Profit Margin: 28% (mock data)",
            ]
        elif analysis_type == "earnings":
            return [
                "Q3 EPS: $2.45 vs est. $2.30 (mock data)",
                "Revenue: $12.5B vs est. $12.1B (mock data)",
            ]
        elif analysis_type == "risk":
            return [
                "30-day volatility: 18% (mock data)",
                "Beta: 1.15 (mock data)",
                "Max drawdown (1Y): -22% (mock data)",
            ]
        else:
            return []
