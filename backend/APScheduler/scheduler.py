from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from db import SessionLocal
from models import UserCompetitor, Competitor, User, RawDocument
from services.crawler_job import perform_scheduled_crawl
import os
import asyncio
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import datetime

# Configuration for the scheduler
executors = {
    'default': AsyncIOExecutor()
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler(executors=executors, job_defaults=job_defaults)

# Placeholder for your LLM agent logic
async def run_llm_agent(user_id, job_type):
    if job_type == 'battlecard':
        print(f"Triggering LLM agent for battlecard creation for user {user_id}.")
    elif job_type == 'report':
        print(f"Triggering LLM agent for report creation for user {user_id}.")
    await asyncio.sleep(1)

def get_cron_kwargs(schedule_type: str):
    if schedule_type == 'daily':
        return {'day_of_week': 'mon-sun', 'hour': 10, 'minute': 10}
    elif schedule_type == 'weekly':
        return {'day_of_week': 'mon', 'hour': 10}
    elif schedule_type == 'monthly':
        return {'day': 1, 'hour': 10}
    else:
        return None

def load_user_schedules():
    db = SessionLocal()
    try:
        user_competitors = db.query(UserCompetitor).options(joinedload(UserCompetitor.competitor)).all()
        
        # Step 1: Create a single set of unique crawl schedules based on competitor URLs
        competitor_schedules = {}
        # Define the priority of schedules
        schedule_priority = {'monthly': 1, 'weekly': 2, 'daily': 3}

        for uc in user_competitors:
            url = uc.competitor.website_url
            
            # Find the highest priority schedule for this competitor
            frequencies = {uc.report_frequency, uc.battlecard_frequency}
            
            most_frequent = None
            current_priority = 0
            
            for freq in frequencies:
                if freq and schedule_priority.get(freq, 0) > current_priority:
                    current_priority = schedule_priority[freq]
                    most_frequent = freq
            
            # Update the competitor's schedule if it's the highest priority found so far
            if url not in competitor_schedules or schedule_priority.get(most_frequent, 0) > schedule_priority.get(competitor_schedules[url]['frequency'], 0):
                competitor_schedules[url] = {
                    'frequency': most_frequent,
                    'users': set()
                }
            competitor_schedules[url]['users'].add(uc.user_id)

        # Step 2: Add unique crawl jobs based on the competitor schedules
        crawled_today_urls = set()
        today = datetime.date.today()
        recent_documents = db.query(RawDocument).filter(
            func.date(RawDocument.scraped_at) == today
        ).all()
        for doc in recent_documents:
            competitor = db.query(Competitor).filter_by(competitor_id=doc.competitor_id).first()
            if competitor:
                crawled_today_urls.add(competitor.website_url)

        for url, schedule_data in competitor_schedules.items():
            if url not in crawled_today_urls and schedule_data['frequency']:
                job_kwargs = get_cron_kwargs(schedule_data['frequency'])
                if job_kwargs:
                    crawl_job_id = f'crawl_competitor_{url}'
                    scheduler.add_job(
                        perform_scheduled_crawl,
                        'cron',
                        id=crawl_job_id,
                        replace_existing=True,
                        args=[list(schedule_data['users']), [url]],
                        **job_kwargs
                    )

        # Step 3: Add LLM jobs for reports and battlecards (unchanged)
        for uc in user_competitors:
            user_id = uc.user_id
            
            if uc.report_frequency:
                job_kwargs = get_cron_kwargs(uc.report_frequency)
                if job_kwargs:
                    llm_job_id = f'llm_report_user_{user_id}_{uc.report_frequency}'
                    scheduler.add_job(
                        run_llm_agent,
                        'cron',
                        id=llm_job_id,
                        replace_existing=True,
                        args=[user_id, 'report'],
                        **job_kwargs
                    )

            if uc.battlecard_frequency:
                job_kwargs = get_cron_kwargs(uc.battlecard_frequency)
                if job_kwargs:
                    llm_job_id = f'llm_battlecard_user_{user_id}_{uc.battlecard_frequency}'
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

def display_all_jobs():
    """Prints a detailed list of all scheduled jobs."""
    jobs = scheduler.get_jobs()
    if not jobs:
        print("No jobs are currently scheduled.")
        return

    print("Currently Scheduled Jobs:")
    for job in jobs:
        print("--------------------")
        print(f"Job ID: {job.id}")
        print(f"Function: {job.func.__name__}")
        print(f"Trigger: {job.trigger}")
        print(f"Next Run Time: {job.next_run_time}")
        print(f"Args: {job.args}")
        print(f"Kwargs: {job.kwargs}")
        print("--------------------")


def add_update_job():
    """Adds a job to the scheduler to periodically reload user schedules from the DB."""
    scheduler.add_job(
        load_user_schedules,
        'cron',
        id='reload_schedules_from_db',
        replace_existing=True,
        # Runs every hour at 30 minutes past the hour.
        hour='*',
        minute='30' 
    )

def start_scheduler():
    scheduler.start()
    load_user_schedules()
    add_update_job()
    #print(f"Loaded schedules from the database. ", display_all_jobs(), flush=True)
    print("APScheduler started.", flush=True)