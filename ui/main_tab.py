import tkinter as tk
from tkinter import ttk
from ui.controls import ScrollableControlPanel

class MainTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_tab()
        
    def setup_tab(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        
        # Section principale avec contrôles et graphique
        self.main_pane = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        self.main_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Panneau de contrôles à gauche
        self.controls_frame = ttk.LabelFrame(self.main_pane, text="Controls", width=180)
        self.controls_frame.pack_propagate(False)
        
        # Conteneur de graphique à droite
        self.graph_container = ttk.Frame(self.main_pane)
        
        self.main_pane.add(self.controls_frame, weight=1)
        self.main_pane.add(self.graph_container, weight=10)
        
        self.app.graph_frame = ttk.Frame(self.graph_container)
        self.app.graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ScrollableControlPanel(self.controls_frame, self.app)
        
    def update_date_fields(self):
        if hasattr(self, 'controls_frame'):
            for child in self.controls_frame.winfo_children():
                if hasattr(child, 'update_date_fields'):
                    child.update_date_fields()