from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from services.crawler import crawl_competitor_url


router = APIRouter(tags=["crawler"])


class CrawlRequest(BaseModel):
    competitor_id: int
    url: str

class CrawlResponse(BaseModel):
    competitor_id: int
    url:str
    scheduled_docs: int    


@router.post("/crawl_competitor", response_model=CrawlResponse)
async def crawl_competitor(req: CrawlRequest, background_tasks: BackgroundTasks):
    scheduled = await crawl_competitor_url(req.competitor_id, req.url, background_tasks)
    return CrawlResponse(competitor_id=req.competitor_id, url=req.url, scheduled_docs=scheduled)







