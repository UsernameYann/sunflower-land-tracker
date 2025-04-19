import tkinter as tk
from tkinter import ttk

class FarmIDSection:
    def __init__(self, parent, app, column=0):
        self.parent = parent
        self.app = app
        self.setup_section(column)
    
    def setup_section(self, column):
        frame = ttk.Frame(self.parent)
        frame.grid(row=0, column=column, sticky="nsew", padx=5, pady=2)
        
        # Section ID de ferme
        id_frame = ttk.LabelFrame(frame, text="Farm Management")
        id_frame.pack(fill=tk.X, padx=5, pady=5)
        
        input_frame = ttk.Frame(id_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Farm ID:").grid(row=0, column=0, sticky=tk.W, padx=(0,5), pady=5)
        self.app.user_id_var = tk.StringVar()
        self.app.user_id_entry = ttk.Entry(input_frame, textvariable=self.app.user_id_var)
        self.app.user_id_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        ttk.Button(button_frame, text="Validate", 
                  command=self.app.validate_user_id).grid(row=0, column=0, sticky="ew", padx=2)
        
        self.app.update_button = ttk.Button(button_frame, text="Manual Update", 
                                          command=self.app.update_data, state='disabled')
        self.app.update_button.grid(row=0, column=1, sticky="ew", padx=2)
        
        self.app.auto_update_button = ttk.Button(button_frame, text="Toggle Auto-update", 
                                              command=self.app.toggle_auto_update, state='disabled')
        self.app.auto_update_button.grid(row=0, column=2, sticky="ew", padx=2)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Ajouter la liste des fermes
        farms_frame = ttk.Frame(id_frame)
        farms_frame.pack(fill=tk.X, padx=5, pady=5)
        farms_frame.columnconfigure(0, weight=1)
        farms_frame.columnconfigure(1, weight=1)
        
        # Fermes automatiques
        auto_farms_frame = ttk.LabelFrame(farms_frame, text="Auto-update Farms")
        auto_farms_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        auto_header = ttk.Frame(auto_farms_frame)
        auto_header.pack(fill=tk.X, padx=2, pady=2)
        
        self.app.auto_status_label = ttk.Label(auto_header, text="Auto-update: Disabled", foreground="red")
        self.app.auto_status_label.pack(side=tk.LEFT)
        
        self.app.auto_count_label = ttk.Label(auto_header, text="0 farm(s)", font=('TkDefaultFont', 9, 'bold'))
        self.app.auto_count_label.pack(side=tk.RIGHT)
        
        auto_list_frame = ttk.Frame(auto_farms_frame)
        auto_list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        auto_scroll = ttk.Scrollbar(auto_list_frame)
        auto_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app.auto_farms_list = tk.Listbox(auto_list_frame, height=3, bd=1, relief=tk.SOLID, 
                                            selectbackground="#4CAF50", selectforeground="white")
        self.app.auto_farms_list.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.app.auto_farms_list.config(yscrollcommand=auto_scroll.set)
        auto_scroll.config(command=self.app.auto_farms_list.yview)
        
        self.app.auto_farms_list.bind("<Double-1>", lambda e: self._on_farm_selected(e, self.app.auto_farms_list))
        
        # Fermes manuelles
        manual_farms_frame = ttk.LabelFrame(farms_frame, text="Manual-update Farms")
        manual_farms_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        manual_header = ttk.Frame(manual_farms_frame)
        manual_header.pack(fill=tk.X, padx=2, pady=2)
        
        manual_status_label = ttk.Label(manual_header, text="Manual-only")
        manual_status_label.pack(side=tk.LEFT)
        
        self.app.manual_count_label = ttk.Label(manual_header, text="0 farm(s)", font=('TkDefaultFont', 9, 'bold'))
        self.app.manual_count_label.pack(side=tk.RIGHT)
        
        manual_list_frame = ttk.Frame(manual_farms_frame)
        manual_list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        manual_scroll = ttk.Scrollbar(manual_list_frame)
        manual_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app.manual_farms_list = tk.Listbox(manual_list_frame, height=3, bd=1, relief=tk.SOLID,
                                             selectbackground="#4CAF50", selectforeground="white")
        self.app.manual_farms_list.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.app.manual_farms_list.config(yscrollcommand=manual_scroll.set)
        manual_scroll.config(command=self.app.manual_farms_list.yview)
        
        self.app.manual_farms_list.bind("<Double-1>", lambda e: self._on_farm_selected(e, self.app.manual_farms_list))
        
        # Remplir les listes initialement
        if hasattr(self.app, 'controller') and hasattr(self.app.controller, 'update_farm_lists'):
            self.app.controller.update_farm_lists()
    
    def _on_farm_selected(self, event, listbox):
        if not listbox.curselection():
            return
            
        farm_id = listbox.get(listbox.curselection()[0])
        if farm_id and hasattr(self.app, 'controller') and hasattr(self.app.controller, 'select_farm_from_list'):
            self.app.controller.select_farm_from_list(farm_id)


class InfoSection:
    def __init__(self, parent, app, column=1):
        self.parent = parent
        self.app = app
        self.setup_section(column)
    
    def setup_section(self, column):
        info_frame = ttk.LabelFrame(self.parent, text="Farm Information")
        info_frame.grid(row=0, column=column, sticky="nsew", padx=5, pady=2)
        info_frame.columnconfigure(0, weight=1)
        
        inner_frame = ttk.Frame(info_frame)
        inner_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        inner_frame.columnconfigure(0, weight=1)
        
        self.app.last_update_label = ttk.Label(inner_frame, text="Last update: -")
        self.app.last_update_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.app.next_update_label = ttk.Label(inner_frame, text="Auto-update: Disabled")
        self.app.next_update_label.grid(row=1, column=0, sticky=tk.W, pady=5)