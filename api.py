from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import run_verification_pipeline

app = FastAPI(title="Disaster Verification API")

# Request schema
class VerifyRequest(BaseModel):
    disaster_type: str
    location: str
    event_date: str   # keep string for now (ISO yyyy-mm-dd)
    description: str

# Response schema (optional but clean)
class VerifyResponse(BaseModel):
    result: dict


@app.post("/verify")
def verify(req: VerifyRequest):
    """
    Structured disaster verification endpoint
    """

    # Combine structured data into a clean claim string
    combined_text = (
        f"{req.disaster_type} reported in {req.location} "
        f"on {req.event_date}. {req.description}"
    )

    # Pass to your existing pipeline
    result = run_verification_pipeline(combined_text)

    return result
