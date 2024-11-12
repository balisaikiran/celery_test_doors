import json
import pymongo
from datetime import datetime
import yagmail
import logging
from typing import List, Dict, Set
from pathlib import Path

class PropertyDataSyncer:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        """Initialize the syncer with MongoDB connection details."""
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        # Setup logging
        logging.basicConfig(
            filename=f'property_sync_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def read_json_file(self, file_path: str) -> List[Dict]:
        """Read and parse the JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.logger.info(f"Successfully read JSON file: {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Error reading JSON file: {e}")
            raise

    def get_existing_zpids(self) -> Set[int]:
        """Get all existing zpids from MongoDB."""
        try:
            existing_zpids = {doc['zpid'] for doc in self.collection.find({}, {'zpid': 1})}
            self.logger.info(f"Found {len(existing_zpids)} existing properties in MongoDB")
            return existing_zpids
        except Exception as e:
            self.logger.error(f"Error retrieving existing zpids: {e}")
            raise

    def find_new_properties(self, new_data: List[Dict], existing_zpids: Set[int]) -> List[Dict]:
        """Find properties in new data that don't exist in MongoDB."""
        new_properties = [
            prop for prop in new_data 
            if prop.get('zpid') and prop['zpid'] not in existing_zpids
        ]
        self.logger.info(f"Found {len(new_properties)} new properties to add")
        return new_properties

    def find_missing_properties(self, new_data: List[Dict], existing_zpids: Set[int]) -> List[int]:
        """Find properties that exist in MongoDB but are missing from new data."""
        new_zpids = {prop['zpid'] for prop in new_data if prop.get('zpid')}
        missing_zpids = list(existing_zpids - new_zpids)
        self.logger.info(f"Found {len(missing_zpids)} missing properties")
        return missing_zpids

    def insert_new_properties(self, new_properties: List[Dict]) -> None:
        """Insert new properties into MongoDB."""
        if new_properties:
            try:
                self.collection.insert_many(new_properties)
                self.logger.info(f"Successfully inserted {len(new_properties)} new properties")
            except Exception as e:
                self.logger.error(f"Error inserting new properties: {e}")
                raise

    def send_email_notification(
        self, 
        recipient_email: str,
        missing_zpids: List[int],
        new_property_count: int,
        smtp_user: str,
        smtp_password: str
    ) -> None:
        """Send email notification about missing properties."""
        try:
            yag = yagmail.SMTP(smtp_user, smtp_password)
            
            subject = f"Property Data Sync Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            body = [
                "Property Data Synchronization Report",
                f"\nNew properties added: {new_property_count}",
                f"\nMissing properties found: {len(missing_zpids)}",
                "\nMissing Property ZPIDs:",
                *[str(zpid) for zpid in missing_zpids[:100]],  # First 100 missing zpids
                "\nFull list attached in CSV file." if len(missing_zpids) > 100 else ""
            ]

            attachments = []
            if len(missing_zpids) > 100:
                # Create CSV file for all missing zpids
                csv_path = f"new_zpids_{datetime.now().strftime('%Y%m%d')}.csv"
                with open(csv_path, 'w') as f:
                    f.write("zpid\n")
                    for zpid in missing_zpids:
                        f.write(f"{zpid}\n")
                attachments.append(csv_path)

            yag.send(recipient_email, subject, body, attachments=attachments)
            self.logger.info("Email notification sent successfully")
            
            # Clean up attachment file if it exists
            if attachments:
                Path(attachments[0]).unlink()
                
        except Exception as e:
            self.logger.error(f"Error sending email notification: {e}")
            raise

    def sync_data(
        self, 
        json_file_path: str, 
        recipient_email: str,
        smtp_user: str,
        smtp_password: str
    ) -> None:
        """Main method to orchestrate the entire sync process."""
        try:
            # Read new data
            new_data = self.read_json_file(json_file_path)
            
            # Get existing zpids
            existing_zpids = self.get_existing_zpids()
            
            # Find new properties
            new_properties = self.find_new_properties(new_data, existing_zpids)
            
            # Find missing properties
            missing_zpids = self.find_missing_properties(new_data, existing_zpids)
            
            # Insert new properties
            self.insert_new_properties(new_properties)
            
            # Send email notification
            self.send_email_notification(
                recipient_email,
                missing_zpids,
                len(new_properties),
                smtp_user,
                smtp_password
            )
            
            self.logger.info("Data sync completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during data sync: {e}")
            raise
        finally:
            self.client.close()

# Example usage
if __name__ == "__main__":
    # Configuration
    MONGO_URI = "mongodb+srv://alex:fl3ieb9QF1feP228@doorsbackend.jbb6crs.mongodb.net/Doors_BE"
    DB_NAME = "Doors_BE"
    COLLECTION_NAME = "Doors_BE_Test_old"
    JSON_FILE_PATH = "/Users/saikiran/Desktop/zillow_results_all_states_v3_all_states.json"
    RECIPIENT_EMAIL = "saiashok49@gmail.com"
    SMTP_USER = 'support@meetdoors.com'
    SMTP_PASSWORD = 'ujao lyoq ance elnl'

    # Initialize and run the syncer
    syncer = PropertyDataSyncer(MONGO_URI, DB_NAME, COLLECTION_NAME)
    syncer.sync_data(JSON_FILE_PATH, RECIPIENT_EMAIL, SMTP_USER, SMTP_PASSWORD)

