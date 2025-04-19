import time
import schedule
from threading import Thread
from datetime import datetime

class ScheduleRunner:
    def __init__(self, app):
        self.app = app
        self.thread = None
    
    def start(self):
        self.thread = Thread(target=self.run_schedule, daemon=True)
        self.thread.start()
    
    def run_schedule(self):
        while True:
            schedule.run_pending()
            
            if self.app.current_user_id:
                is_auto_update = self.app.farm_manager.is_auto_update_farm(self.app.current_user_id)
                
                if is_auto_update and self.app.next_update:
                    remaining = self.app.next_update - datetime.now()
                    if remaining.total_seconds() > 0:
                        self.app.next_update_label.config(
                            text=f"Next update: {self.app.format_datetime(self.app.next_update)} "
                                 f"(in {self.app.format_countdown(remaining.total_seconds())})")
            
            time.sleep(1)