import tkinter as tk
from tkinter import ttk, messagebox

class FarmsTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_tab()
        
    def setup_tab(self):
        # Configuration de la grille
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)
        
        # Frame principale
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        
        # Section ID de ferme
        id_frame = ttk.LabelFrame(main_frame, text="Farm Selection")
        id_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        input_frame = ttk.Frame(id_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Farm ID:").grid(row=0, column=0, sticky=tk.W, padx=(0,5), pady=5)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        entry_frame.columnconfigure(0, weight=1)
        
        self.app.user_id_var = tk.StringVar()
        self.app.user_id_entry = ttk.Entry(entry_frame, textvariable=self.app.user_id_var)
        self.app.user_id_entry.grid(row=0, column=0, sticky="ew")
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, sticky="e", padx=5)
        
        validate_btn = ttk.Button(button_frame, text="Validate", 
                                command=self.app.validate_user_id)
        validate_btn.pack(side=tk.LEFT, padx=2)
        
        self.app.update_button = ttk.Button(button_frame, text="Manual Update", 
                                         command=self.app.update_data, state='disabled')
        self.app.update_button.pack(side=tk.LEFT, padx=2)
        
        self.app.auto_update_button = ttk.Button(button_frame, text="Toggle Auto-update", 
                                             command=self.app.toggle_auto_update, state='disabled')
        self.app.auto_update_button.pack(side=tk.LEFT, padx=2)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Section Information
        info_frame = ttk.LabelFrame(main_frame, text="Farm Information")
        info_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        inner_info_frame = ttk.Frame(info_frame)
        inner_info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.app.last_update_label = ttk.Label(inner_info_frame, text="Last update: -")
        self.app.last_update_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.app.next_update_label = ttk.Label(inner_info_frame, text="Auto-update: Disabled")
        self.app.next_update_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.app.auto_status_label = ttk.Label(inner_info_frame, text="Auto-update: Disabled", foreground="red")
        self.app.auto_status_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Section listes des fermes
        farms_frame = ttk.Frame(self.parent)
        farms_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        farms_frame.columnconfigure(0, weight=1)
        farms_frame.columnconfigure(1, weight=1)
        farms_frame.rowconfigure(0, weight=1)
        
        # Liste des fermes automatiques
        auto_frame = ttk.LabelFrame(farms_frame, text="Auto-update Farms")
        auto_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        auto_toolbar = ttk.Frame(auto_frame)
        auto_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        self.app.auto_count_label = ttk.Label(auto_toolbar, text="0 farm(s)")
        self.app.auto_count_label.pack(side=tk.LEFT, padx=5)
        
        remove_auto_btn = ttk.Button(auto_toolbar, text="Remove Selected", 
                                   command=lambda: self.remove_farm("auto"))
        remove_auto_btn.pack(side=tk.RIGHT, padx=5)
        
        auto_list_frame = ttk.Frame(auto_frame)
        auto_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        auto_scroll = ttk.Scrollbar(auto_list_frame)
        auto_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app.auto_farms_list = tk.Listbox(auto_list_frame, bd=1, relief=tk.SOLID, 
                                           selectbackground="#4CAF50", selectforeground="white")
        self.app.auto_farms_list.pack(fill=tk.BOTH, expand=True)
        self.app.auto_farms_list.config(yscrollcommand=auto_scroll.set)
        auto_scroll.config(command=self.app.auto_farms_list.yview)
        
        self.app.auto_farms_list.bind("<Double-1>", lambda e: self.select_farm(e, self.app.auto_farms_list))
        
        # Liste des fermes manuelles
        manual_frame = ttk.LabelFrame(farms_frame, text="Manual-update Farms")
        manual_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        manual_toolbar = ttk.Frame(manual_frame)
        manual_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        self.app.manual_count_label = ttk.Label(manual_toolbar, text="0 farm(s)")
        self.app.manual_count_label.pack(side=tk.LEFT, padx=5)
        
        remove_manual_btn = ttk.Button(manual_toolbar, text="Remove Selected", 
                                     command=lambda: self.remove_farm("manual"))
        remove_manual_btn.pack(side=tk.RIGHT, padx=5)
        
        manual_list_frame = ttk.Frame(manual_frame)
        manual_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        manual_scroll = ttk.Scrollbar(manual_list_frame)
        manual_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app.manual_farms_list = tk.Listbox(manual_list_frame, bd=1, relief=tk.SOLID, 
                                             selectbackground="#4CAF50", selectforeground="white")
        self.app.manual_farms_list.pack(fill=tk.BOTH, expand=True)
        self.app.manual_farms_list.config(yscrollcommand=manual_scroll.set)
        manual_scroll.config(command=self.app.manual_farms_list.yview)
        
        self.app.manual_farms_list.bind("<Double-1>", lambda e: self.select_farm(e, self.app.manual_farms_list))
        
        # Actualiser les listes de fermes
        if hasattr(self.app, 'controller') and hasattr(self.app.controller, 'update_farm_lists'):
            self.app.controller.update_farm_lists()
    
    def select_farm(self, event, listbox):
        if not listbox.curselection():
            return
            
        farm_id = listbox.get(listbox.curselection()[0])
        if farm_id and hasattr(self.app, 'controller'):
            self.app.controller.select_farm_from_list(farm_id)
    
    def remove_farm(self, list_type):
        if list_type == "auto":
            if not self.app.auto_farms_list.curselection():
                messagebox.showinfo("Info", "Please select a farm to remove")
                return
                
            farm_id = self.app.auto_farms_list.get(self.app.auto_farms_list.curselection()[0])
            if farm_id and messagebox.askyesno("Confirm", f"Are you sure you want to remove farm {farm_id} from auto-update?"):
                self.app.farm_manager.remove_farm(farm_id, "admin")
                
                # Si c'est la ferme actuelle, mettre à jour les labels
                if farm_id == self.app.current_user_id:
                    self.app.next_update = None
                    self.app.controller.update_status_labels()
                
                messagebox.showinfo("Success", f"Farm {farm_id} removed from auto-update")
                self.app.controller.update_farm_lists()
        
        elif list_type == "manual":
            if not self.app.manual_farms_list.curselection():
                messagebox.showinfo("Info", "Please select a farm to remove")
                return
                
            farm_id = self.app.manual_farms_list.get(self.app.manual_farms_list.curselection()[0])
            if farm_id and messagebox.askyesno("Confirm", f"Are you sure you want to remove farm {farm_id}?"):
                self.app.farm_manager.remove_manual_farm(farm_id)
                messagebox.showinfo("Success", f"Farm {farm_id} removed")
                self.app.controller.update_farm_lists()
