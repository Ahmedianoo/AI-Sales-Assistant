from fastapi import APIRouter, BackgroundTasks
from services.ingest import process_and_ingest
from crawl4ai import AsyncWebCrawler
from pydantic import BaseModel


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
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(req.url)

    scheduled = 0
    for doc in results:
        if doc.markdown:
            background_tasks.add_task(process_and_ingest, req.competitor_id, doc.markdown)
            scheduled += 1

    return CrawlResponse(
        competitor_id=req.competitor_id,
        url=req.url,
        scheduled_docs=scheduled
    )





