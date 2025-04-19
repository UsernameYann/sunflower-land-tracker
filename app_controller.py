from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from config import APP_TITLE

class AppController:
    def __init__(self, app):
        self.app = app
        
    def validate_user_id(self):
        self.app.data_manager.validate_user_id()
    
    def update_data(self):
        self.app.data_manager.update_data()
    
    def scheduled_update(self, user_id=None):
        return self.app.data_manager.scheduled_update(user_id)
    
    def update_status_labels(self):
        if self.app.last_update:
            self.app.last_update_label.config(
                text=f"Last update: {self.app.format_datetime(self.app.last_update)}")
        
        if self.app.next_update:
            remaining = self.app.next_update - datetime.now()
            if remaining.total_seconds() > 0:
                self.app.next_update_label.config(
                    text=f"Next update: {self.app.format_datetime(self.app.next_update)} "
                         f"(in {self.app.format_countdown(remaining.total_seconds())})")
            else:
                self.app.next_update_label.config(text="Next update: Soon")
                
            # Mettre à jour l'indicateur de statut automatique
            if hasattr(self.app, 'auto_status_label'):
                self.app.auto_status_label.config(text="Auto-update: Enabled", foreground="green")
        else:
            self.app.next_update_label.config(text="Auto-update: Disabled")
            
            # Mettre à jour l'indicateur de statut automatique
            if hasattr(self.app, 'auto_status_label'):
                self.app.auto_status_label.config(text="Auto-update: Disabled", foreground="red")
    
    def toggle_category(self, category):
        state = self.app.item_vars[category]['all'].get()
        for item_var in self.app.item_vars[category]['items'].values():
            item_var.set(state)
        self.update_graph()
    
    def update_graph(self):
        self.app.data_manager.update_graph()
    
    def show_about(self):
        messagebox.showinfo("About", 
                      f"{APP_TITLE}\n\nVersion 1.0\n\n"
                      "Resource tracking application\nfor Sunflower Land")
    
    def toggle_auto_update(self):
        if not self.app.current_user_id:
            return
            
        if self.app.farm_list_manager.toggle_auto_update():
            self.app.next_update = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
            self.update_status_labels()
            messagebox.showinfo("Auto-update enabled", 
                          "This farm will now be updated automatically every day at midnight.")
        else:
            self.app.next_update = None
            self.update_status_labels()
            messagebox.showinfo("Auto-update disabled", 
                          "This farm will now only be updated manually.")
    
    def update_date_fields(self):
        if hasattr(self.app, 'main_tab_manager') and hasattr(self.app.main_tab_manager, 'update_date_fields'):
            self.app.main_tab_manager.update_date_fields()
    
    def update_farm_lists(self):
        """Mettre à jour les listes de fermes dans l'interface"""
        if not hasattr(self.app, 'auto_farms_list') or not hasattr(self.app, 'manual_farms_list'):
            return
            
        # Effacer les listes actuelles
        self.app.auto_farms_list.delete(0, tk.END)
        self.app.manual_farms_list.delete(0, tk.END)
        
        # Ajouter les fermes automatiques
        auto_farms = self.app.farm_manager.get_admin_farms()
        for farm_id in auto_farms:
            self.app.auto_farms_list.insert(tk.END, farm_id)
            
        # Ajouter les fermes manuelles
        manual_farms = self.app.farm_manager.get_manual_farms()
        for farm_id in manual_farms:
            self.app.manual_farms_list.insert(tk.END, farm_id)
            
        # Mettre à jour les compteurs
        if hasattr(self.app, 'auto_count_label'):
            self.app.auto_count_label.config(text=f"{len(auto_farms)} farm(s)")
            
        if hasattr(self.app, 'manual_count_label'):
            self.app.manual_count_label.config(text=f"{len(manual_farms)} farm(s)")
    
    def select_farm_from_list(self, farm_id):
        """Sélectionner une ferme depuis la liste"""
        if not farm_id:
            return
            
        self.app.user_id_var.set(farm_id)
        self.validate_user_id()
    
    def remove_farm(self, farm_id, list_type):
        """Supprimer une ferme de la liste spécifiée"""
        if list_type == "admin":
            success = self.app.farm_manager.remove_farm(farm_id, "admin")
            if success:
                messagebox.showinfo("Success", f"Farm {farm_id} removed from auto-update list")
            else:
                messagebox.showerror("Error", f"Failed to remove farm {farm_id}")
        else:
            success = self.app.farm_manager.remove_manual_farm(farm_id)
            if success:
                messagebox.showinfo("Success", f"Farm {farm_id} removed from manual list")
            else:
                messagebox.showerror("Error", f"Failed to remove farm {farm_id}")
        
        if success:
            self.update_farm_lists()