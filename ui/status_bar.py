import tkinter as tk
from tkinter import ttk
from datetime import datetime

class StatusBar:
    def __init__(self, parent):
        self.parent = parent
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        ttk.Separator(self.status_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=2)
        
        info_frame = ttk.Frame(self.status_frame)
        info_frame.pack(fill=tk.X)
        
        self.connection_status = ttk.Label(info_frame, text="● API Connection: OK", foreground="green")
        self.connection_status.pack(side=tk.LEFT, padx=5)
        
        self.status_message = ttk.Label(info_frame, text="")
        self.status_message.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(info_frame, text=f"Version: 1.0").pack(side=tk.RIGHT, padx=5)
        
        self.date_label = ttk.Label(info_frame, text=f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        self.date_label.pack(side=tk.RIGHT, padx=20)
        
        self.update_status()
    
    def update_status(self):
        self.date_label.config(text=f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        
        try:
            import requests
            response = requests.get("https://api.sunflower-land.com/ping")
            if response.status_code == 200:
                self.connection_status.config(text="● API Connection: OK", foreground="green")
            else:
                self.connection_status.config(text="● API Connection: Error", foreground="red")
        except:
            self.connection_status.config(text="● API Connection: Error", foreground="red")
        
        self.parent.after(300000, self.update_status)
    
    def update_message(self, message, duration=10000):
        self.status_message.config(text=message)
        
        if duration > 0:
            self.parent.after(duration, lambda: self.status_message.config(text=""))