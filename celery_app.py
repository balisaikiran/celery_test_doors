import logging
import os
from celery import Celery
from celery.schedules import crontab
from Zillow_scraper_final import main as zillow_main

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize Celery with Redis URL from environment
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
app = Celery('tasks', broker=redis_url)

# Configure timezone
app.conf.timezone = 'America/New_York'

# Task definition
@app.task
def run_my_script():
    try:
        logging.info("Starting Zillow scraper from Celery task")
        zillow_main()
        logging.info("Completed Zillow scraper task")
    except Exception as e:
        logging.error(f"Error running Zillow scraper: {e}")
        raise

# Configure periodic tasks
app.conf.beat_schedule = {
    'run-weekly-at-3am': {
        'task': 'celery_app.run_my_script',
        'schedule': crontab(hour=3, minute=0, day_of_week=1),
    },
}