# routes/reports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from db import get_db
from middleware.isAuthenticated import get_current_user
from langGraph_app.state.report_state import ReportState
from langGraph_app.nodes.query_builder import build_query


from models.reports import Report
from models.user_competitor import UserCompetitor
from services.report_generator import generate_report
from langGraph_app.nodes.retriever import retrieve_docs
import datetime

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

from pydantic import BaseModel

class ReportRequest(BaseModel):
    user_comp_id: int
    competitor_id: int
    

# @router.post("/", response_model=dict)
# async def generate_report(
#     request: ReportRequest,
#     user: dict = Depends(get_current_user),   # get current user
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Construct ReportState with user_id from authentication
#         state: ReportState = {
#             "user_id": user.user_id,   # inject logged-in user id
#             "competitor_ids": request.competitor_ids,
#             "query": None,
#             "retrieved_docs": None,
#             "generated_report": None,
#             "error": None,
#         }

#         # For now, just return the state (no pipeline yet)
#         return JSONResponse(
#             content={"state": state},
#             status_code=200,
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# @router.post("/test-query")
# async def test_query(state: ReportState):
#     new_state = build_query(state)
#     return {"state": new_state}


# from fastapi import Body

# @router.post("/test-retriever")
# async def test_retriever(state: dict = Body(...)):
#     from langGraph_app.nodes.retriever import retrieve_docs
    
#     try:
#         updated_state = retrieve_docs(state)
#         return {"state": updated_state}
#     except Exception as e:
#         import traceback; traceback.print_exc()
#         return {"error": str(e)}
    



# from langGraph_app.nodes.retriever import deduplicate_docs
# from langGraph_app.nodes.retriever import retrieve_docs
# from services.report_generator import generate_report

# @router.post("/test-generator")
# def test_generator(payload: dict, db: Session = Depends(get_db)):
#     state = {
#         "user_id": payload["user_id"],
#         "competitor_ids": payload["competitor_ids"],
#         "query": payload["query"],
#         "retrieved_docs": None,
#         "generated_report": None,
#         "error": None,
#     }

#     # use retriever pipeline
#     state = retrieve_docs(state)

#     # apply deduplication here too (safety net)
#     docs = deduplicate_docs(state["retrieved_docs"])

#     # generate report from deduped docs
#     report = generate_report(docs, state["query"])

#     return {
#         "query": state["query"],
#         "docs_count": len(docs),
#         "report": report
#     }


########################################################################


@router.post("/run")
async def run_full_pipeline(
    request: ReportRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Initialize state
        state = {
            "user_id": user.user_id,
            "competitor_ids": [request.competitor_id],  # used for retrieval
            "query": None,
            "retrieved_docs": None,
            "generated_report": None,
            "error": None,
        }

        # Build and retrieve
        state = build_query(state)
        state = retrieve_docs(state)

        if not state["retrieved_docs"]:
            state["generated_report"] = "⚠️ No relevant documents found"
            return JSONResponse(content={"state": state}, status_code=200)

        #  Generate report
        report_text = generate_report(state["retrieved_docs"], state["query"])
        state["generated_report"] = report_text

        # 4️Save report under correct user_comp_id
        new_report = Report(
            user_comp_id=request.user_comp_id,
            report_type="competitor_analysis",
            report_date=datetime.date.today(),
            metrics={"report_text": report_text},
            created_at=datetime.datetime.now(),
        )
        db.add(new_report)
        db.commit()

        return JSONResponse(content={"state": state}, status_code=200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")




@router.get("/")
async def get_user_reports(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = (
        db.query(Report)
        .join(UserCompetitor, Report.user_comp_id == UserCompetitor.user_comp_id)
        .filter(UserCompetitor.user_id == user.user_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    # if not reports:
    #     raise HTTPException(status_code=404, detail=f"No reports found for user_id={user.user_id}")

    return reports
