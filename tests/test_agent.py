"""Tests for the FinancialAdvisorAgent."""

import pytest

from agents.advisor_agent import FinancialAdvisorAgent
from app.schemas.portfolio import Holding, Portfolio


@pytest.fixture
def agent():
    """Create a fresh agent instance for each test."""
    return FinancialAdvisorAgent()


@pytest.fixture
def sample_portfolio():
    """Create a sample portfolio for testing."""
    return Portfolio(
        user_id="test-user-123",
        holdings=[
            Holding(ticker="AAPL", shares="100", cost_basis="150.50"),
            Holding(ticker="MSFT", shares="50", cost_basis="280.00"),
            Holding(ticker="GOOGL", shares="25", cost_basis="120.00"),
        ],
    )


class TestAnalysisTypeDetection:
    """Test analysis type detection logic."""

    def test_detect_bull_bear_analysis(self, agent):
        """Test detection of bull/bear case requests."""
        assert agent._detect_analysis_type("What's the bull case for AAPL?") == "bull_bear"
        assert agent._detect_analysis_type("Tell me the bear case") == "bull_bear"
        assert agent._detect_analysis_type("Make a case for buying") == "bull_bear"

    def test_detect_earnings_analysis(self, agent):
        """Test detection of earnings analysis requests."""
        assert agent._detect_analysis_type("Show me the earnings report") == "earnings"
        assert agent._detect_analysis_type("What were the latest earnings?") == "earnings"

    def test_detect_comparison_analysis(self, agent):
        """Test detection of stock comparison requests."""
        assert agent._detect_analysis_type("Compare AAPL vs MSFT") == "comparison"
        assert agent._detect_analysis_type("How does it compare to GOOGL?") == "comparison"
        assert agent._detect_analysis_type("AAPL versus TSLA") == "comparison"

    def test_detect_risk_analysis(self, agent):
        """Test detection of risk analysis requests."""
        assert agent._detect_analysis_type("What are the risks?") == "risk"
        assert agent._detect_analysis_type("Tell me about volatility") == "risk"
        assert agent._detect_analysis_type("What's the downside?") == "risk"

    def test_detect_general_query(self, agent):
        """Test detection of general queries."""
        assert agent._detect_analysis_type("Hello") == "general"
        assert agent._detect_analysis_type("Help me understand stocks") == "general"


class TestTickerExtraction:
    """Test ticker symbol extraction logic."""

    def test_extract_single_ticker(self, agent):
        """Test extracting a single ticker symbol."""
        assert agent._extract_ticker("What's the price of AAPL?") == "AAPL"
        assert agent._extract_ticker("Tell me about MSFT") == "MSFT"

    def test_extract_multiple_tickers(self, agent):
        """Test extracting first ticker when multiple are present."""
        # Should return the first ticker found
        ticker = agent._extract_ticker("Compare AAPL vs MSFT")
        assert ticker in ["AAPL", "MSFT"]

    def test_extract_no_ticker(self, agent):
        """Test when no ticker is present."""
        assert agent._extract_ticker("What's the market doing?") is None
        assert agent._extract_ticker("Tell me about tech stocks") is None

    def test_filter_common_words(self, agent):
        """Test that common words are filtered out."""
        assert agent._extract_ticker("I want to buy a stock") is None
        assert agent._extract_ticker("For the portfolio") is None


class TestMessageProcessing:
    """Test message processing and response generation."""

    def test_process_bull_case_message(self, agent):
        """Test processing a bull case request."""
        response = agent.process_message("What's the bull case for AAPL?")

        assert response.message is not None
        assert "bull" in response.message.lower()
        assert "AAPL" in response.message
        assert response.analysis_type == "bull_bear"
        assert response.session_id is not None
        assert len(response.citations) > 0
        assert "not financial advice" in response.disclaimer.lower()

    def test_process_bear_case_message(self, agent):
        """Test processing a bear case request."""
        response = agent.process_message("What's the bear case for MSFT?")

        assert response.message is not None
        assert "bear" in response.message.lower()
        assert "MSFT" in response.message
        assert response.analysis_type == "bull_bear"
        assert len(response.citations) > 0

    def test_process_general_message(self, agent):
        """Test processing a general query."""
        response = agent.process_message("Hello, how can you help me?")

        assert response.message is not None
        assert response.analysis_type == "general"
        assert response.session_id is not None

    def test_process_with_portfolio_context(self, agent, sample_portfolio):
        """Test processing message with portfolio context."""
        response = agent.process_message(
            "What should I know?",
            portfolio=sample_portfolio
        )

        assert response.message is not None
        # Should mention some of the holdings
        assert any(holding.ticker in response.message for holding in sample_portfolio.holdings)


class TestSessionManagement:
    """Test conversation session management."""

    def test_new_session_creation(self, agent):
        """Test that new sessions are created with unique IDs."""
        response1 = agent.process_message("Hello")
        response2 = agent.process_message("Hi there")

        assert response1.session_id != response2.session_id
        assert response1.session_id in agent.sessions
        assert response2.session_id in agent.sessions

    def test_session_continuity(self, agent):
        """Test that messages in the same session are linked."""
        session_id = "test-session-123"

        response1 = agent.process_message("What's the bull case for AAPL?", session_id=session_id)
        response2 = agent.process_message("What about the bear case?", session_id=session_id)

        assert response1.session_id == session_id
        assert response2.session_id == session_id
        assert len(agent.sessions[session_id]) == 4  # 2 user messages + 2 assistant responses

    def test_session_history_content(self, agent):
        """Test that session history contains correct content."""
        session_id = "test-session-456"

        agent.process_message("First message", session_id=session_id)
        agent.process_message("Second message", session_id=session_id)

        history = agent.sessions[session_id]
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "First message"
        assert history[1]["role"] == "assistant"
        assert history[2]["role"] == "user"
        assert history[2]["content"] == "Second message"


class TestMockResponseGeneration:
    """Test mock response generation logic."""

    def test_bull_case_contains_key_sections(self, agent):
        """Test that bull case response contains expected sections."""
        message = agent._mock_bull_case("AAPL")

        assert "Bull Case" in message
        assert "Strengths" in message or "strengths" in message.lower()
        assert "Catalysts" in message or "catalysts" in message.lower()
        assert "Valuation" in message or "valuation" in message.lower()
        assert "mock" in message.lower()  # Should indicate it's mock data

    def test_bear_case_contains_key_sections(self, agent):
        """Test that bear case response contains expected sections."""
        message = agent._mock_bear_case("MSFT")

        assert "Bear Case" in message
        assert "Risks" in message or "risks" in message.lower()
        assert "Concerns" in message or "concerns" in message.lower()
        assert "mock" in message.lower()  # Should indicate it's mock data

    def test_balanced_view_contains_both_sides(self, agent):
        """Test that balanced view contains both bull and bear factors."""
        message = agent._mock_balanced_view("GOOGL")

        assert "Bull" in message
        assert "Bear" in message
        assert "GOOGL" in message


class TestCitationGeneration:
    """Test citation generation for different analysis types."""

    def test_bull_bear_citations(self, agent):
        """Test citations for bull/bear analysis."""
        citations = agent._generate_mock_citations("bull_bear")

        assert len(citations) > 0
        assert any("P/E" in citation for citation in citations)
        assert any("Revenue" in citation or "Growth" in citation for citation in citations)
        assert all("mock" in citation.lower() for citation in citations)

    def test_earnings_citations(self, agent):
        """Test citations for earnings analysis."""
        citations = agent._generate_mock_citations("earnings")

        assert len(citations) > 0
        assert any("EPS" in citation for citation in citations)
        assert any("Revenue" in citation for citation in citations)

    def test_risk_citations(self, agent):
        """Test citations for risk analysis."""
        citations = agent._generate_mock_citations("risk")

        assert len(citations) > 0
        assert any("volatility" in citation.lower() for citation in citations)
        assert any("Beta" in citation for citation in citations)

    def test_general_citations(self, agent):
        """Test that general queries have no citations."""
        citations = agent._generate_mock_citations("general")

        assert len(citations) == 0
