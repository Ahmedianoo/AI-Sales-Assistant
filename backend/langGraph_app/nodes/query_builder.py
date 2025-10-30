# langGraph_app/nodes/query_builder.py
from langGraph_app.state.report_state import ReportState
from db import SessionLocal
from models import Competitor  # make sure this matches your actual model name

def build_query(state: ReportState) -> ReportState:
    competitor_ids = state.get("competitor_ids", [])
    db = SessionLocal()

    try:
        names = []
        for cid in competitor_ids:
            comp = db.query(Competitor).filter(Competitor.competitor_id == cid).first()
            if comp and comp.name:
                names.append(comp.name)

        if names:
            # join names into a single query string
            state["query"] = " ".join(names)
        else:
            # fallback if no names found
            state["query"] = f"competitors: {competitor_ids}"

    finally:
        db.close()

    return state
