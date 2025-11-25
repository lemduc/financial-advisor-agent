"""Tests for the chat API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestChatEndpoint:
    """Test the /chat endpoint functionality."""

    def test_chat_endpoint_exists(self, client):
        """Test that the chat endpoint is accessible."""
        response = client.post(
            "/chat",
            json={"message": "Hello"}
        )
        assert response.status_code == 200

    def test_chat_with_bull_case_request(self, client):
        """Test chat endpoint with a bull case request."""
        response = client.post(
            "/chat",
            json={
                "message": "What's the bull case for AAPL?",
                "user_id": "test-user-1"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "session_id" in data
        assert "timestamp" in data
        assert "analysis_type" in data
        assert "citations" in data
        assert "disclaimer" in data

        assert data["analysis_type"] == "bull_bear"
        assert "AAPL" in data["message"]
        assert len(data["citations"]) > 0

    def test_chat_with_bear_case_request(self, client):
        """Test chat endpoint with a bear case request."""
        response = client.post(
            "/chat",
            json={"message": "What's the bear case for MSFT?"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["analysis_type"] == "bull_bear"
        assert "bear" in data["message"].lower()
        assert "MSFT" in data["message"]

    def test_chat_with_earnings_request(self, client):
        """Test chat endpoint with earnings analysis request."""
        response = client.post(
            "/chat",
            json={"message": "Show me the earnings for GOOGL"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["analysis_type"] == "earnings"
        assert "earnings" in data["message"].lower()

    def test_chat_with_risk_request(self, client):
        """Test chat endpoint with risk analysis request."""
        response = client.post(
            "/chat",
            json={"message": "What are the risks of TSLA?"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["analysis_type"] == "risk"
        assert "risk" in data["message"].lower()

    def test_chat_with_general_query(self, client):
        """Test chat endpoint with a general query."""
        response = client.post(
            "/chat",
            json={"message": "Hello, how can you help me?"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["analysis_type"] == "general"
        assert data["message"] is not None

    def test_chat_session_id_persistence(self, client):
        """Test that session IDs are maintained across requests."""
        # First request without session ID
        response1 = client.post(
            "/chat",
            json={"message": "First message"}
        )
        session_id = response1.json()["session_id"]

        # Second request with the same session ID
        response2 = client.post(
            "/chat",
            json={
                "message": "Second message",
                "session_id": session_id
            }
        )

        assert response2.status_code == 200
        assert response2.json()["session_id"] == session_id

    def test_chat_generates_new_session_when_not_provided(self, client):
        """Test that new session IDs are generated when not provided."""
        response1 = client.post(
            "/chat",
            json={"message": "Message 1"}
        )
        response2 = client.post(
            "/chat",
            json={"message": "Message 2"}
        )

        session_id_1 = response1.json()["session_id"]
        session_id_2 = response2.json()["session_id"]

        assert session_id_1 != session_id_2

    def test_chat_response_has_disclaimer(self, client):
        """Test that all responses include a disclaimer."""
        response = client.post(
            "/chat",
            json={"message": "What should I invest in?"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "disclaimer" in data
        assert "not financial advice" in data["disclaimer"].lower()

    def test_chat_response_has_timestamp(self, client):
        """Test that responses include a timestamp."""
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "timestamp" in data
        # Timestamp should be in ISO format
        assert "T" in data["timestamp"]


class TestChatRequestValidation:
    """Test request validation for the chat endpoint."""

    def test_chat_requires_message(self, client):
        """Test that message field is required."""
        response = client.post(
            "/chat",
            json={}
        )

        assert response.status_code == 422  # Validation error

    def test_chat_accepts_empty_optional_fields(self, client):
        """Test that optional fields can be omitted."""
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )

        assert response.status_code == 200

    def test_chat_accepts_user_id(self, client):
        """Test that user_id is accepted when provided."""
        response = client.post(
            "/chat",
            json={
                "message": "Test message",
                "user_id": "user-123"
            }
        )

        assert response.status_code == 200

    def test_chat_accepts_session_id(self, client):
        """Test that session_id is accepted when provided."""
        response = client.post(
            "/chat",
            json={
                "message": "Test message",
                "session_id": "session-456"
            }
        )

        assert response.status_code == 200
        assert response.json()["session_id"] == "session-456"

    def test_chat_rejects_invalid_json(self, client):
        """Test that invalid JSON is rejected."""
        response = client.post(
            "/chat",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422


class TestChatResponseSchema:
    """Test the response schema structure."""

    def test_response_has_all_required_fields(self, client):
        """Test that response contains all required fields."""
        response = client.post(
            "/chat",
            json={"message": "Test"}
        )

        data = response.json()
        required_fields = [
            "message",
            "session_id",
            "timestamp",
            "disclaimer"
        ]

        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_response_citations_is_list(self, client):
        """Test that citations field is a list."""
        response = client.post(
            "/chat",
            json={"message": "What's the bull case for AAPL?"}
        )

        data = response.json()
        assert isinstance(data["citations"], list)

    def test_response_confidence_field(self, client):
        """Test that confidence field is present."""
        response = client.post(
            "/chat",
            json={"message": "Analyze MSFT"}
        )

        data = response.json()
        assert "confidence" in data

    def test_response_analysis_type_field(self, client):
        """Test that analysis_type field is present."""
        response = client.post(
            "/chat",
            json={"message": "Tell me about GOOGL"}
        )

        data = response.json()
        assert "analysis_type" in data
        assert data["analysis_type"] in [
            "bull_bear",
            "earnings",
            "comparison",
            "risk",
            "general"
        ]


class TestChatEndpointDocumentation:
    """Test that the endpoint is properly documented."""

    def test_chat_endpoint_in_openapi_schema(self, client):
        """Test that chat endpoint appears in OpenAPI schema."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        schema = response.json()

        assert "/chat" in schema["paths"]
        assert "post" in schema["paths"]["/chat"]

    def test_chat_endpoint_has_description(self, client):
        """Test that endpoint has a description."""
        response = client.get("/openapi.json")
        schema = response.json()

        chat_endpoint = schema["paths"]["/chat"]["post"]
        assert "summary" in chat_endpoint or "description" in chat_endpoint

    def test_chat_endpoint_has_request_schema(self, client):
        """Test that endpoint has request schema defined."""
        response = client.get("/openapi.json")
        schema = response.json()

        chat_endpoint = schema["paths"]["/chat"]["post"]
        assert "requestBody" in chat_endpoint

    def test_chat_endpoint_has_response_schema(self, client):
        """Test that endpoint has response schema defined."""
        response = client.get("/openapi.json")
        schema = response.json()

        chat_endpoint = schema["paths"]["/chat"]["post"]
        assert "responses" in chat_endpoint
        assert "200" in chat_endpoint["responses"]
