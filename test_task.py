from celery_app import run_my_script

if __name__ == "__main__":
    print("Triggering Zillow scraper task manually...")
    result = run_my_script.delay()
    print(f"Task ID: {result.id}")
    print("Task triggered successfully. Check the worker logs for results.")