import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import os

from data_collector import DataCollector
from data_processor import DataProcessor
from graph_manager import GraphManager
from gui_components import ScrollableFrame
from farm_manager import FarmManager
from config import *
from utils import format_datetime, format_countdown
from ui.main_tab import MainTab  
from data_manager import DataManager
from farm_list_manager import SimpleFarmManager
from scheduler import ScheduleRunner
from ui.status_bar import StatusBar
from ui.menu_bar import MenuBar
from app_controller import AppController

class SunflowerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)
        
        self.setup_theme()
        
        self.DATA_DIRECTORY = DATA_DIRECTORY
        self.UPDATE_TIME = UPDATE_TIME
        
        self.format_datetime = format_datetime
        self.format_countdown = format_countdown
        
        self.collector = DataCollector()
        self.processor = DataProcessor()
        self.graph_manager = GraphManager()
        self.farm_manager = FarmManager(DATA_DIRECTORY)
        self.scrollable_frame_class = ScrollableFrame
        
        self.next_update = None
        self.last_update = None
        self.current_user_id = None
        
        self.controller = AppController(self)
        
        self.setup_gui()
        
        self.data_manager = DataManager(self)
        self.farm_list_manager = SimpleFarmManager(self)
        self.scheduler = ScheduleRunner(self)
        
        self.scheduler.start()
    
    def setup_theme(self):
        style = ttk.Style()
        
        style.theme_use('clam')
        
        primary_color = "#4CAF50"
        text_color = "black"
        bg_color = "white"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color, font=('Helvetica', 10))
        style.configure("TButton", background=primary_color, foreground="white", 
                       font=('Helvetica', 10, 'bold'), padding=6)
        style.map("TButton", 
                 background=[('active', primary_color), ('pressed', primary_color)])
        
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background=bg_color, foreground=text_color, 
                       font=('Helvetica', 10, 'bold'), padding=[10, 5])
        style.map("TNotebook.Tab",
                 background=[('selected', primary_color), ('active', primary_color)],
                 foreground=[('selected', 'white'), ('active', 'white')])
        
        style.configure("TLabelframe", background=bg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=text_color, 
                       font=('Helvetica', 10, 'bold'))
        
        style.configure("TRadiobutton", background=bg_color, foreground=text_color)
        style.configure("TCheckbutton", background=bg_color, foreground=text_color)
        
        self.root.configure(background=bg_color)
    
    def setup_gui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._main_tab_created = False
        self._farms_tab_created = False
        self._create_main_tab()
        self._create_farms_tab()
        
        self.status_bar = StatusBar(self.root)
        self.menu_bar = MenuBar(self.root, self)

    def _create_main_tab(self):
        if self._main_tab_created:
            return
            
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Graph")
        
        self.main_tab_manager = MainTab(self.main_tab, self)
        self._main_tab_created = True
        
    def _create_farms_tab(self):
        if self._farms_tab_created:
            return
            
        from ui.farms_tab import FarmsTab
        self.farms_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.farms_tab, text="Farm Management")
        
        self.farms_tab_manager = FarmsTab(self.farms_tab, self)
        self._farms_tab_created = True
    
    def show_about(self):
        self.controller.show_about()
    
    def validate_user_id(self):
        self.controller.validate_user_id()
    
    def update_data(self):
        self.controller.update_data()
    
    def scheduled_update(self, user_id=None):
        return self.controller.scheduled_update(user_id)
    
    def update_status_labels(self):
        self.controller.update_status_labels()
    
    def toggle_category(self, category):
        self.controller.toggle_category(category)
    
    def update_graph(self):
        self.controller.update_graph()
    
    def toggle_auto_update(self):
        self.controller.toggle_auto_update()
    
    def update_date_fields(self):
        self.controller.update_date_fields()

def main():
    root = tk.Tk()
    app = SunflowerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()