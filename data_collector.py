import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.base_url = "https://api.sunflower-land.com/community/farms/"
        self.base_dir = "data"
        self.last_request_time = 0
        
    def create_user_directory(self, user_id):
        user_dir = os.path.join(self.base_dir, str(user_id))
        Path(user_dir).mkdir(parents=True, exist_ok=True)
        return user_dir

    def fetch_and_save_data(self, user_id, force=False):
        try:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            
            if not force and time_since_last_request < 30:
                wait_time = 30 - time_since_last_request
                time.sleep(wait_time)
            
            self.last_request_time = time.time()
            
            response = requests.get(f"{self.base_url}{user_id}")
            
            if response.status_code == 200:
                data = response.json()
                if 'farm' not in data:
                    logger.error(f"Incomplete API response for {user_id}: 'farm' missing")
                    return False
                    
                today = datetime.now().strftime("%Y-%m-%d")
                user_dir = self.create_user_directory(user_id)
                filename = f"{today}.json"
                file_path = os.path.join(user_dir, filename)
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                return True
            
            logger.error(f"API Error: Status code {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False