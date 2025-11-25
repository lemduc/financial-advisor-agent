"""Portfolio and holdings schemas."""

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Holding(BaseModel):
    """Individual stock holding."""

    ticker: str = Field(..., description="Stock ticker symbol")
    shares: Decimal = Field(..., description="Number of shares held")
    cost_basis: Decimal = Field(..., description="Average cost per share")
    purchase_date: Optional[date] = Field(None, description="Original purchase date")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "shares": "100",
                    "cost_basis": "150.50",
                    "purchase_date": "2023-01-15",
                }
            ]
        }
    }


class Portfolio(BaseModel):
    """User's complete portfolio."""

    user_id: str = Field(..., description="User identifier")
    holdings: list[Holding] = Field(
        default_factory=list, description="List of holdings"
    )
    total_value: Optional[Decimal] = Field(
        None, description="Current total portfolio value"
    )
    last_updated: Optional[date] = Field(None, description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "user-456",
                    "holdings": [
                        {
                            "ticker": "AAPL",
                            "shares": "100",
                            "cost_basis": "150.50",
                            "purchase_date": "2023-01-15",
                        },
                        {
                            "ticker": "MSFT",
                            "shares": "50",
                            "cost_basis": "280.00",
                            "purchase_date": "2023-03-20",
                        },
                    ],
                    "total_value": "30000.00",
                    "last_updated": "2025-11-24",
                }
            ]
        }
    }
