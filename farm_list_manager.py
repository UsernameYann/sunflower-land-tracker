import tkinter as tk
from tkinter import messagebox

class SimpleFarmManager:
    def __init__(self, app):
        self.app = app
    
    def toggle_auto_update(self):
        user_id = self.app.current_user_id
        if not user_id:
            return False
            
        is_auto = self.app.farm_manager.is_auto_update_farm(user_id)
        
        if is_auto:
            self.app.farm_manager.remove_farm(user_id, "admin")
            self.app.farm_manager.add_manual_farm(user_id)
            return False
        else:
            self.app.farm_manager.remove_manual_farm(user_id)
            self.app.farm_manager.add_admin_farm(user_id)
            return True