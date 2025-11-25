from fastapi import FastAPI

app = FastAPI(title="Financial Advisor Agent")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health endpoint to confirm the service is up."""
    return {"status": "ok", "message": "financial-advisor-agent online"}
