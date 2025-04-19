import os
from datetime import datetime, timedelta
from tkinter import messagebox
from user_data_manager import UserDataManager
from update_manager import UpdateManager
from data_filter import DataFilter

class DataManager:
    def __init__(self, app):
        self.app = app
        self.user_manager = UserDataManager(app)
        self.update_manager = UpdateManager(app)
        self.data_filter = DataFilter(app)
    
    def validate_user_id(self):
        return self.user_manager.validate_user_id()
    
    def update_data(self):
        return self.update_manager.update_data()
    
    def scheduled_update(self, user_id=None):
        return self.update_manager.scheduled_update(user_id)
    
    def filter_dates(self, dates, data_series):
        return self.data_filter.filter_dates(dates, data_series)
    
    def update_graph(self):
        user_id = self.app.user_id_var.get()
        if not user_id:
            return
        
        import threading
        
        def _update_graph_thread():
            selected_items = {}
            for cat_key in self.app.processor.CATEGORIES:
                selected_items[cat_key] = [
                    item for item, var in self.app.item_vars[cat_key]['items'].items() 
                    if var.get()
                ]
            
            if not any(items for items in selected_items.values()):
                return
                
            dates, data_series = self.app.processor.get_user_data(user_id)
            
            if not dates:
                return
                
            filtered_dates, filtered_data = self.filter_dates(dates, data_series)
            
            self.app.root.after(0, lambda: self._update_graph_ui(
                filtered_dates, filtered_data, selected_items))
        
        threading.Thread(target=_update_graph_thread, daemon=True).start()
    
    def _update_graph_ui(self, filtered_dates, filtered_data, selected_items):
        self.app.graph_manager.create_graph(
            self.app.graph_frame,
            filtered_dates,
            filtered_data,
            selected_items,
            self.app.processor.COLORS
        )