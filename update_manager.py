from datetime import datetime, timedelta
from tkinter import messagebox
import schedule
import logging

logger = logging.getLogger(__name__)

class UpdateManager:
    def __init__(self, app):
        self.app = app
        self.scheduled_job = None
        schedule.clear()
        self._schedule_daily_update()
        
    def _schedule_daily_update(self):
        schedule.clear()
        self.scheduled_job = schedule.every().day.at(self.app.UPDATE_TIME).do(self.scheduled_update)
        logger.info(f"Automatic update scheduled every day at {self.app.UPDATE_TIME}")
        
    def update_data(self):
        user_id = self.app.user_id_var.get().strip()
        if not user_id:
            messagebox.showerror("Error", "Please enter a farm ID")
            return False
        
        today_file_exists = not self.app.farm_manager.can_update_today(user_id)
        
        if today_file_exists:
            if not messagebox.askyesno("Update", 
                                    "You have already saved data today. "
                                    "Do you want to overwrite the existing file?"):
                return False
        
        if self._perform_update(user_id):
            return True
        return False
        
    def _perform_update(self, user_id):
        if not self.app.collector.fetch_and_save_data(user_id):
            messagebox.showerror("Error", "Error updating data")
            return False
            
        self.app.last_update = datetime.now()
        self.app.last_update_label.config(
            text=f"Last update: {self.app.format_datetime(self.app.last_update)}")
        
        is_auto = self.app.farm_manager.is_auto_update_farm(user_id)
        
        if is_auto:
            self.app.next_update = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
            self.app.next_update_label.config(
                text=f"Next update: {self.app.format_datetime(self.app.next_update)}")
        else:
            self.app.next_update = None
            self.app.next_update_label.config(text="Auto-update: Disabled")
        
        self.app.current_user_id = user_id
        self.app.update_button.config(state='normal')
        self.app.auto_update_button.config(state='normal')
        
        messagebox.showinfo("Success", "Data updated successfully")
        self.app.update_graph()
        return True
        
    def scheduled_update(self, user_id=None):
        updated = False
        farms_updated = 0
        
        if user_id:
            return self._update_single_farm(user_id)
        
        farms_to_update = self._get_farms_to_update()
        
        logger.info(f"Scheduled automatic update: {len(farms_to_update)} farms to process")
        print(f"Scheduled automatic update: {len(farms_to_update)} farms to process")
        
        for farm_id in farms_to_update:
            try:
                if self.app.collector.fetch_and_save_data(farm_id):
                    farms_updated += 1
                    updated = True
                    logger.info(f"Successful update for farm {farm_id}")
                    
                    if farm_id == self.app.current_user_id:
                        self.app.last_update = datetime.now()
                        self.app.update_status_labels()
                        self.app.update_graph()
                else:
                    logger.warning(f"Update failed for farm {farm_id}")
            except Exception as e:
                logger.error(f"Error updating farm {farm_id}: {str(e)}")
        
        logger.info(f"Automatic update completed: {farms_updated}/{len(farms_to_update)} farms updated successfully")
        print(f"Automatic update completed: {farms_updated}/{len(farms_to_update)} farms updated successfully")
        
        return updated
        
    def _update_single_farm(self, user_id):
        if self.app.farm_manager.can_update_today(user_id) and self.app.collector.fetch_and_save_data(user_id):
            if user_id == self.app.current_user_id:
                self.app.last_update = datetime.now()
                self.app.update_status_labels()
                self.app.update_graph()
            logger.info(f"Manual update successful for farm {user_id}")
            return True
        logger.warning(f"Manual update failed for farm {user_id}")
        return False
        
    def _get_farms_to_update(self):
        farms_to_update = []
        
        for farm_id in self.app.farm_manager.get_admin_farms():
            if self.app.farm_manager.can_update_today(farm_id):
                farms_to_update.append(farm_id)
                
        return farms_to_update