import os
from datetime import datetime, timedelta
from tkinter import messagebox

class UserDataManager:
    def __init__(self, app):
        self.app = app
        
    def validate_user_id(self):
        user_id = self.app.user_id_var.get().strip()
        if not user_id:
            messagebox.showerror("Error", "Please enter a farm ID")
            return False

        user_dir = os.path.join(self.app.DATA_DIRECTORY, str(user_id))
        
        if os.path.exists(user_dir) and os.listdir(user_dir):
            return self._setup_existing_user(user_id, user_dir)
        else:
            return self._handle_new_user(user_id)
            
    def _setup_existing_user(self, user_id, user_dir):
        self.app.current_user_id = user_id
        self.app.update_button.config(state='normal')
        self.app.auto_update_button.config(state='normal')
        
        is_auto_update = self.app.farm_manager.is_auto_update_farm(user_id)
        
        if not is_auto_update and user_id not in self.app.farm_manager.get_manual_farms():
            self.app.farm_manager.add_manual_farm(user_id)
            
        self._setup_update_schedule(user_id, is_auto_update)
        
        files = sorted(os.listdir(user_dir))
        if files:
            latest_file = files[-1]
            self.app.last_update = datetime.strptime(latest_file.replace('.json', ''), '%Y-%m-%d')
            self.app.last_update_label.config(
                text=f"Last update: {self.app.format_datetime(self.app.last_update)}")
        
        self.app.update_graph()
        
        # Mettre à jour les listes de fermes
        if hasattr(self.app.controller, 'update_farm_lists'):
            self.app.controller.update_farm_lists()
            
        return True
        
    def _handle_new_user(self, user_id):
        if messagebox.askyesno("New Farm", 
                            "No data found for this Farm ID. "
                            "Would you like to save data now?"):
            
            if self.app.collector.fetch_and_save_data(user_id):
                self.app.current_user_id = user_id
                self.app.last_update = datetime.now()
                self.app.last_update_label.config(
                    text=f"Last update: {self.app.format_datetime(self.app.last_update)}")
                
                self.app.update_button.config(state='normal')
                self.app.auto_update_button.config(state='normal')
                
                if messagebox.askyesno("Auto-update", 
                                    "Do you want to enable automatic daily updates for this farm?"):
                    self.app.farm_manager.add_admin_farm(user_id)
                    self.app.next_update = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
                    from schedule import every
                    every().day.at(self.app.UPDATE_TIME).do(self.app.scheduled_update, user_id)
                    self.app.next_update_label.config(
                        text=f"Next update: {self.app.format_datetime(self.app.next_update)}")
                else:
                    self.app.farm_manager.add_manual_farm(user_id)
                    self.app.next_update = None
                    self.app.next_update_label.config(text="Auto-update: Disabled")
                
                # Mettre à jour les listes de fermes
                if hasattr(self.app.controller, 'update_farm_lists'):
                    self.app.controller.update_farm_lists()
                    
                messagebox.showinfo("Success", "Farm added successfully")
                self.app.update_graph()
                return True
            else:
                messagebox.showerror("Error", "Unable to retrieve data for this farm ID")
                return False
        else:
            return False
            
    def _setup_update_schedule(self, user_id, is_auto_update):
        if is_auto_update:
            self.app.next_update = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
            from schedule import every
            every().day.at(self.app.UPDATE_TIME).do(self.app.scheduled_update, user_id)
            self.app.next_update_label.config(
                text=f"Next update: {self.app.format_datetime(self.app.next_update)}")
        else:
            self.app.next_update = None
            self.app.next_update_label.config(text="Auto-update: Disabled")