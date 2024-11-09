import logging
import boto3
from datetime import datetime
import os

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

# Function to create a text file and write "Hi" inside it
def create_text_file(file_path='output.txt'):
    try:
        # Create the full path in the project_files directory
        full_path = os.path.join('project_files', file_path)
        with open(full_path, 'w') as file:
            file.write("Hi")
        absolute_path = os.path.abspath(full_path)
        logging.info(f"File created at: {absolute_path}")
        logging.info(f"Successfully created file '{file_path}' with content 'Hi'")
    except Exception as e:
        logging.error(f"Failed to create text file: {e}")

def main():
    setup_cloudwatch_logging()
    logging.info("Starting Zillow scraper")
    
    # Create the text file with "Hi"
    create_text_file()
    
    logging.info("Zillow scraper completed")

if __name__ == "__main__":
    main()
