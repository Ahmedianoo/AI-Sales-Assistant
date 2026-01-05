from fastapi import APIRouter, BackgroundTasks
from .ingest import process_and_ingest
from crawl4ai import AsyncWebCrawler
# from pydantic import BaseModel




async def crawl_competitor_url(competitor_id: int, url: str, background_tasks: BackgroundTasks = None) -> int:

    scheduled = 0
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(url)

    for doc in results:
        if doc.markdown and background_tasks:
            background_tasks.add_task(process_and_ingest, competitor_id, doc.markdown)
            scheduled += 1

    return scheduled