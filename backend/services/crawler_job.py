import asyncio
from crawl4ai import AsyncWebCrawler
from services.ingest import process_and_ingest
from db import SessionLocal
from models import UserCompetitor, Competitor, RawDocument
import datetime

async def perform_scheduled_crawl(user_id, competitor_urls):
    """
    Performs the web crawl and data ingestion for a list of URLs.
    This function saves the data to both the relational and vector databases.
    """
    print(f"Starting scheduled crawl for user {user_id}...")

    # Fetch competitor IDs from URLs. The URLs are the source of truth here.
    db = SessionLocal()
    try:
        competitors = db.query(Competitor).filter(Competitor.website_url.in_(competitor_urls)).all()
        competitor_map = {comp.website_url: comp.competitor_id for comp in competitors}
    finally:
        db.close()

    # Start the async web crawling session
    async with AsyncWebCrawler() as crawler:
        tasks = []
        for url in competitor_urls:
            if url in competitor_map:
                competitor_id = competitor_map[url]
                tasks.append(asyncio.create_task(
                    crawl_and_ingest_single_url(crawler, competitor_id, url)
                ))
            else:
                print(f"Skipping crawl for {url}: competitor not found in DB.")

        await asyncio.gather(*tasks)

    print("Scheduled crawl complete.")

async def crawl_and_ingest_single_url(crawler, competitor_id, url):
    """Helper function to crawl and ingest a single URL."""
    db = SessionLocal()
    try:
        results = await crawler.arun(url)
        for doc in results:
            if doc.markdown:
                doc_id, num_chunks = process_and_ingest(competitor_id, doc.markdown)
                print(f"Ingested {num_chunks} chunks for doc {doc_id} from {url}.")
                
                # Retrieve the newly created document and update the timestamp
                raw_doc = db.query(RawDocument).filter(RawDocument.id == doc_id).first()
                if raw_doc:
                    raw_doc.scraped_at = datetime.datetime.now()
                    db.commit()

    except Exception as e:
        db.rollback() # Rollback changes if an error occurs
        print(f"Failed to crawl {url}. Error: {e}")
    finally:
        db.close()