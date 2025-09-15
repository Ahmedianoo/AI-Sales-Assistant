from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from db import SessionLocal
from models import UserCompetitor, Competitor, User, RawDocument # Add RawDocument
from services.crawler_job import perform_scheduled_crawl
import os
import asyncio
from sqlalchemy.orm import joinedload
from sqlalchemy import func 
import datetime # Add datetime

# Configuration for the scheduler
executors = {
    'default': AsyncIOExecutor()
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler(executors=executors, job_defaults=job_defaults, timezone='Asia/Dubai')

# Placeholder for your LLM agent logic
async def run_llm_agent(user_id, job_type):
    """
    This function will trigger the LLM agent to create the
    report or battlecard after the crawl is complete.
    """
    if job_type == 'battlecard':
        print(f"Triggering LLM agent for battlecard creation for user {user_id}.")
    elif job_type == 'report':
        print(f"Triggering LLM agent for report creation for user {user_id}.")
        
    # Simulate an async operation
    await asyncio.sleep(1) 

def get_cron_kwargs(schedule_type: str):
    """Maps a schedule type string to APScheduler cron arguments."""
    if schedule_type == 'daily':
        return {'day_of_week': 'mon-sun', 'hour': 3, 'minute': 34}
    elif schedule_type == 'weekly':
        return {'day_of_week': 'mon', 'hour': 2}
    elif schedule_type == 'monthly':
        return {'day': 1, 'hour': 2}
    else:
        return None

def load_user_schedules():
    db = SessionLocal()
    try:
        user_competitors = db.query(UserCompetitor).options(joinedload(UserCompetitor.competitor)).all()

        # Step 1: Combine all unique crawl schedules into a single dictionary
        crawl_schedules = {}
        for uc in user_competitors:
            # Check report frequency
            report_freq = uc.report_frequency
            if report_freq:
                key = (uc.user_id, report_freq)
                if key not in crawl_schedules:
                    crawl_schedules[key] = []
                crawl_schedules[key].append(uc.competitor.website_url)

            # Check battlecard frequency
            battlecard_freq = uc.battlecard_frequency
            if battlecard_freq:
                key = (uc.user_id, battlecard_freq)
                if key not in crawl_schedules:
                    crawl_schedules[key] = []
                crawl_schedules[key].append(uc.competitor.website_url)
        
        # Step 2: Add unique crawl jobs
        crawled_today_urls = set()
        today = datetime.date.today()
        recent_documents = db.query(RawDocument).filter(
            func.date(RawDocument.scraped_at) == today
        ).all()
        for doc in recent_documents:
            competitor = db.query(Competitor).filter_by(competitor_id=doc.competitor_id).first()
            if competitor:
                crawled_today_urls.add(competitor.website_url)
        
        for (user_id, schedule_type), competitor_urls in crawl_schedules.items():
            job_kwargs = get_cron_kwargs(schedule_type)
            if not job_kwargs:
                continue
            
            # Filter URLs that haven't been crawled today
            urls_to_crawl = [url for url in competitor_urls if url not in crawled_today_urls]

            if urls_to_crawl:
                crawl_job_id = f'crawl_user_{user_id}_{schedule_type}'
                scheduler.add_job(
                    perform_scheduled_crawl,
                    'cron',
                    id=crawl_job_id,
                    replace_existing=True,
                    args=[user_id, urls_to_crawl],
                    **job_kwargs
                )

        # Step 3: Add LLM jobs for reports
        for uc in user_competitors:
            user_id = uc.user_id
            schedule_type = uc.report_frequency
            if not schedule_type:
                continue
            
            job_kwargs = get_cron_kwargs(schedule_type)
            if not job_kwargs:
                continue

            llm_job_id = f'llm_report_user_{user_id}_{schedule_type}'
            scheduler.add_job(
                run_llm_agent,
                'cron',
                id=llm_job_id,
                replace_existing=True,
                args=[user_id, 'report'],
                **job_kwargs
            )

        # Step 4: Add LLM jobs for battlecards
        for uc in user_competitors:
            user_id = uc.user_id
            schedule_type = uc.battlecard_frequency
            if not schedule_type:
                continue
            
            job_kwargs = get_cron_kwargs(schedule_type)
            if not job_kwargs:
                continue
            
            llm_job_id = f'llm_battlecard_user_{user_id}_{schedule_type}'
            scheduler.add_job(
                run_llm_agent,
                'cron',
                id=llm_job_id,
                replace_existing=True,
                args=[user_id, 'battlecard'],
                **job_kwargs
            )
        
    finally:
        db.close()
    
    print(f"Loaded schedules from the database. Total jobs added: {len(scheduler.get_jobs())}")


def start_scheduler():
    """Starts the APScheduler instance and loads jobs from the database."""
    scheduler.start()
    load_user_schedules()
    print("APScheduler started.")