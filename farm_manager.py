import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FarmManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.admin_file = os.path.join(data_dir, "admin_farms.json")
        self.manual_file = os.path.join(data_dir, "manual_farms.json")
        self._ensure_files_exist()
        
    def _ensure_files_exist(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.admin_file):
            self._save_json_file(self.admin_file, [])
                
        if not os.path.exists(self.manual_file):
            self._save_json_file(self.manual_file, [])
    
    def _load_json_file(self, file_path, default_value=None):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list) and (default_value == [] or default_value is None):
                    return data
                else:
                    logger.warning(f"Incorrect file format {file_path}: {data}")
                    return default_value if default_value is not None else []
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return default_value if default_value is not None else []

    def _save_json_file(self, file_path, data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            return False

    def get_admin_farms(self):
        return self._load_json_file(self.admin_file, [])
    
    def add_admin_farm(self, farm_id):
        farm_id = str(farm_id)
        farms = self.get_admin_farms()
        if farm_id not in farms:
            farms.append(farm_id)
            success = self._save_json_file(self.admin_file, farms)
            if success:
                logger.info(f"Farm {farm_id} added to auto-update list")
            return success
        return False
    
    def remove_farm(self, farm_id, list_type):
        farm_id = str(farm_id)
        
        if list_type == "admin":
            farms = self.get_admin_farms()
            file_path = self.admin_file
        else:
            farms = self.get_manual_farms()
            file_path = self.manual_file
            
        logger.debug(f"Attempting to remove {farm_id} from list {list_type}")
        
        if farm_id in farms:
            farms.remove(farm_id)
            success = self._save_json_file(file_path, farms)
            if success:
                logger.info(f"Farm {farm_id} successfully removed from {list_type}")
            return success
        
        logger.debug(f"Farm {farm_id} not found in list {list_type}")
        return False
    
    def can_update_today(self, farm_id):
        farm_id = str(farm_id)
        farm_dir = os.path.join(self.data_dir, farm_id)
        if not os.path.exists(farm_dir):
            return True
            
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = os.path.join(farm_dir, f"{today}.json")
        
        return not os.path.exists(today_file)
    
    def is_auto_update_farm(self, farm_id):
        farm_id = str(farm_id)
        return farm_id in self.get_admin_farms()
    
    def get_manual_farms(self):
        return self._load_json_file(self.manual_file, [])

    def add_manual_farm(self, farm_id):
        farm_id = str(farm_id)
        farms = self.get_manual_farms()
        if farm_id not in farms:
            farms.append(farm_id)
            success = self._save_json_file(self.manual_file, farms)
            if success:
                logger.info(f"Farm {farm_id} added to manual list")
            return success
        return False

    def remove_manual_farm(self, farm_id):
        return self.remove_farm(farm_id, "manual")