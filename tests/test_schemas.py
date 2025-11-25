"""Tests for Pydantic schemas."""

from datetime import date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.portfolio import Holding, Portfolio


class TestChatRequestSchema:
    """Test ChatRequest schema validation."""

    def test_valid_chat_request_minimal(self):
        """Test creating a chat request with minimal fields."""
        request = ChatRequest(message="Hello")

        assert request.message == "Hello"
        assert request.session_id is None
        assert request.user_id is None

    def test_valid_chat_request_full(self):
        """Test creating a chat request with all fields."""
        request = ChatRequest(
            message="What's the bull case for AAPL?",
            session_id="session-123",
            user_id="user-456"
        )

        assert request.message == "What's the bull case for AAPL?"
        assert request.session_id == "session-123"
        assert request.user_id == "user-456"

    def test_chat_request_missing_message(self):
        """Test that message field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest()

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("message",) for error in errors)

    def test_chat_request_empty_message(self):
        """Test that empty message is accepted (validation at app level)."""
        request = ChatRequest(message="")
        assert request.message == ""


class TestChatResponseSchema:
    """Test ChatResponse schema validation."""

    def test_valid_chat_response_minimal(self):
        """Test creating a chat response with minimal fields."""
        response = ChatResponse(
            message="Here's the analysis",
            session_id="session-123"
        )

        assert response.message == "Here's the analysis"
        assert response.session_id == "session-123"
        assert response.timestamp is not None
        assert isinstance(response.timestamp, datetime)
        assert response.disclaimer is not None
        assert response.citations == []

    def test_valid_chat_response_full(self):
        """Test creating a chat response with all fields."""
        timestamp = datetime.utcnow()
        citations = ["P/E: 25", "Revenue Growth: 15%"]

        response = ChatResponse(
            message="Bull case analysis",
            session_id="session-456",
            timestamp=timestamp,
            analysis_type="bull_bear",
            confidence="high",
            citations=citations,
            disclaimer="Custom disclaimer"
        )

        assert response.message == "Bull case analysis"
        assert response.session_id == "session-456"
        assert response.timestamp == timestamp
        assert response.analysis_type == "bull_bear"
        assert response.confidence == "high"
        assert response.citations == citations
        assert response.disclaimer == "Custom disclaimer"

    def test_chat_response_default_disclaimer(self):
        """Test that default disclaimer is set."""
        response = ChatResponse(
            message="Test",
            session_id="session-789"
        )

        assert "not financial advice" in response.disclaimer.lower()

    def test_chat_response_missing_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError) as exc_info:
            ChatResponse()

        errors = exc_info.value.errors()
        assert len(errors) > 0


class TestHoldingSchema:
    """Test Holding schema validation."""

    def test_valid_holding_minimal(self):
        """Test creating a holding with minimal fields."""
        holding = Holding(
            ticker="AAPL",
            shares="100",
            cost_basis="150.50"
        )

        assert holding.ticker == "AAPL"
        assert holding.shares == Decimal("100")
        assert holding.cost_basis == Decimal("150.50")
        assert holding.purchase_date is None

    def test_valid_holding_full(self):
        """Test creating a holding with all fields."""
        purchase_date = date(2023, 1, 15)

        holding = Holding(
            ticker="MSFT",
            shares="50",
            cost_basis="280.00",
            purchase_date=purchase_date
        )

        assert holding.ticker == "MSFT"
        assert holding.shares == Decimal("50")
        assert holding.cost_basis == Decimal("280.00")
        assert holding.purchase_date == purchase_date

    def test_holding_decimal_conversion(self):
        """Test that strings are converted to Decimal."""
        holding = Holding(
            ticker="GOOGL",
            shares="25.5",
            cost_basis="120.75"
        )

        assert isinstance(holding.shares, Decimal)
        assert isinstance(holding.cost_basis, Decimal)
        assert holding.shares == Decimal("25.5")
        assert holding.cost_basis == Decimal("120.75")

    def test_holding_missing_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError) as exc_info:
            Holding(ticker="AAPL")

        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Missing shares and cost_basis

    def test_holding_invalid_decimal(self):
        """Test that invalid decimal values are rejected."""
        with pytest.raises(ValidationError):
            Holding(
                ticker="TSLA",
                shares="not_a_number",
                cost_basis="100"
            )


class TestPortfolioSchema:
    """Test Portfolio schema validation."""

    def test_valid_portfolio_empty(self):
        """Test creating an empty portfolio."""
        portfolio = Portfolio(user_id="user-123")

        assert portfolio.user_id == "user-123"
        assert portfolio.holdings == []
        assert portfolio.total_value is None
        assert portfolio.last_updated is None

    def test_valid_portfolio_with_holdings(self):
        """Test creating a portfolio with holdings."""
        holdings = [
            Holding(ticker="AAPL", shares="100", cost_basis="150.00"),
            Holding(ticker="MSFT", shares="50", cost_basis="280.00"),
        ]

        portfolio = Portfolio(
            user_id="user-456",
            holdings=holdings,
            total_value="29000.00",
            last_updated=date(2025, 11, 24)
        )

        assert portfolio.user_id == "user-456"
        assert len(portfolio.holdings) == 2
        assert portfolio.holdings[0].ticker == "AAPL"
        assert portfolio.holdings[1].ticker == "MSFT"
        assert portfolio.total_value == Decimal("29000.00")
        assert portfolio.last_updated == date(2025, 11, 24)

    def test_portfolio_missing_user_id(self):
        """Test that user_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            Portfolio()

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("user_id",) for error in errors)

    def test_portfolio_validates_holdings(self):
        """Test that holdings are validated."""
        with pytest.raises(ValidationError):
            Portfolio(
                user_id="user-789",
                holdings=[
                    {"ticker": "AAPL"}  # Missing required fields
                ]
            )


class TestSchemaJsonSerialization:
    """Test JSON serialization of schemas."""

    def test_chat_request_json_serialization(self):
        """Test that ChatRequest can be serialized to JSON."""
        request = ChatRequest(
            message="Test message",
            user_id="user-1"
        )

        json_data = request.model_dump()

        assert json_data["message"] == "Test message"
        assert json_data["user_id"] == "user-1"
        assert json_data["session_id"] is None

    def test_chat_response_json_serialization(self):
        """Test that ChatResponse can be serialized to JSON."""
        response = ChatResponse(
            message="Response",
            session_id="session-1",
            citations=["Citation 1", "Citation 2"]
        )

        json_data = response.model_dump()

        assert json_data["message"] == "Response"
        assert json_data["session_id"] == "session-1"
        assert len(json_data["citations"]) == 2

    def test_portfolio_json_serialization(self):
        """Test that Portfolio can be serialized to JSON."""
        portfolio = Portfolio(
            user_id="user-1",
            holdings=[
                Holding(ticker="AAPL", shares="100", cost_basis="150.00")
            ]
        )

        json_data = portfolio.model_dump()

        assert json_data["user_id"] == "user-1"
        assert len(json_data["holdings"]) == 1
        assert json_data["holdings"][0]["ticker"] == "AAPL"

    def test_schema_json_deserialization(self):
        """Test that schemas can be deserialized from JSON."""
        json_data = {
            "message": "Test",
            "session_id": "session-1",
            "user_id": "user-1"
        }

        request = ChatRequest(**json_data)

        assert request.message == "Test"
        assert request.session_id == "session-1"
        assert request.user_id == "user-1"
