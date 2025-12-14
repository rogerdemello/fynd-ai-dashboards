"""FastAPI backend for Task 2 - AI Feedback System."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database import add_submission, get_all_submissions, get_analytics
from llm_service import generate_user_response, generate_admin_summary, generate_recommended_action

app = FastAPI(title="AI Feedback System API", version="1.0.0")

# Enable CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmissionRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Star rating from 1-5")
    review: str = Field(..., min_length=1, max_length=5000, description="Review text")


class SubmissionResponse(BaseModel):
    id: int
    ai_response: str


@app.get("/")
def root():
    """API health check."""
    return {"status": "ok", "message": "AI Feedback System API is running"}


@app.post("/api/submit", response_model=SubmissionResponse)
def submit_review(submission: SubmissionRequest):
    """Submit a new review and get AI-generated response."""
    try:
        # Generate AI responses
        ai_response = generate_user_response(submission.rating, submission.review)
        ai_summary = generate_admin_summary(submission.rating, submission.review)
        ai_action = generate_recommended_action(submission.rating, submission.review)
        
        # Store in database
        submission_id = add_submission(
            rating=submission.rating,
            review=submission.review,
            ai_response=ai_response,
            ai_summary=ai_summary,
            ai_recommended_action=ai_action
        )
        
        return SubmissionResponse(id=submission_id, ai_response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing submission: {str(e)}")


@app.get("/api/submissions")
def list_submissions():
    """Get all submissions (for admin dashboard)."""
    try:
        submissions = get_all_submissions()
        return {"submissions": submissions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving submissions: {str(e)}")


@app.get("/api/analytics")
def get_stats():
    """Get analytics summary (for admin dashboard)."""
    try:
        analytics = get_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing analytics: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
