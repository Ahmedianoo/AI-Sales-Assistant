from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from db import get_db
from middleware.isAuthenticated import get_current_user

# import your LangGraph workflow
from workflows.competitor_analysis import workflow


router = APIRouter(
    prefix="/langgraph",
    tags=["langgraph"]
)

# ----- Request & Response Models -----
class AnalyzeRequest(BaseModel):
    url: str


class AnalyzeResponse(BaseModel):
    url: str
    summary: str



@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_competitor(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),   
    current_user: dict = Depends(get_current_user)   
):
    try:
        # run workflow
        result = workflow.invoke({"url": request.url})

        if not result or "summary" not in result:
            raise HTTPException(status_code=500, detail="Workflow failed to produce a summary")

        return AnalyzeResponse(url=request.url, summary=result["summary"])

    except HTTPException:
        raise
    except Exception as e:
        print("LangGraph error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
