import logging
import boto3
from datetime import datetime

# Setup logging to both console and CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def setup_cloudwatch_logging():
    try:
        session = boto3.Session()
        client = session.client('logs')
        log_group = '/zillow-scraper/logs'
        log_stream = f'scraper-{datetime.now().strftime("%Y-%m-%d")}'
        
        try:
            client.create_log_group(logGroupName=log_group)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
            
        try:
            client.create_log_stream(
                logGroupName=log_group,
                logStreamName=log_stream
            )
        except client.exceptions.ResourceAlreadyExistsException:
            pass
            
    except Exception as e:
        logging.error(f"Failed to setup CloudWatch logging: {e}")

def main():
    setup_cloudwatch_logging()
    logging.info("Starting Zillow scraper")
    print("Hi testing:")
    logging.info("Zillow scraper completed")

if __name__ == "__main__":
    main()