import tkinter as tk
from tkinter import ttk

class PeriodControls:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_period_section()
    
    def setup_period_section(self):
        ttk.Label(self.parent, text="PERIOD", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(2, 3))
        
        period_frame = ttk.Frame(self.parent)
        period_frame.pack(fill=tk.X, pady=0)
        
        self.app.date_option = tk.StringVar(value="all")
        
        self.app.date_option.trace_add("write", self._on_date_option_change)
        
        for text, value in [("All history", "all"), ("Last 7 days", "week"), 
                          ("Last 30 days", "month"), ("Custom", "custom")]:
            ttk.Radiobutton(period_frame, text=text, variable=self.app.date_option, 
                          value=value, command=self.update_date_fields).pack(anchor=tk.W, pady=1)
        
        custom_frame = ttk.Frame(period_frame)
        custom_frame.pack(fill=tk.X, pady=2)
        
        start_frame = ttk.Frame(custom_frame)
        start_frame.pack(fill=tk.X, pady=2)
        ttk.Label(start_frame, text="From (YYYY-MM-DD):").pack(side=tk.LEFT, padx=2)
        self.app.start_date = ttk.Entry(start_frame, width=10, state="disabled")
        self.app.start_date.pack(side=tk.LEFT, padx=2)
        
        end_frame = ttk.Frame(custom_frame)
        end_frame.pack(fill=tk.X, pady=2)
        ttk.Label(end_frame, text="To (YYYY-MM-DD):").pack(side=tk.LEFT, padx=2)
        self.app.end_date = ttk.Entry(end_frame, width=10, state="disabled")
        self.app.end_date.pack(side=tk.LEFT, padx=2)
        
        apply_frame = ttk.Frame(custom_frame)
        apply_frame.pack(fill=tk.X, pady=2)
        self.app.apply_date_button = ttk.Button(apply_frame, text="Apply", 
                                              command=self.app.update_graph, state="disabled")
        self.app.apply_date_button.pack(side=tk.LEFT, padx=2)

    def update_date_fields(self):
        if self.app.date_option.get() == "custom":
            self.app.start_date.config(state="normal")
            self.app.end_date.config(state="normal")
            self.app.apply_date_button.config(state="normal")
        else:
            self.app.start_date.config(state="disabled")
            self.app.end_date.config(state="disabled")
            self.app.apply_date_button.config(state="disabled")
            self.app.root.after(100, self.app.update_graph)

    def _on_date_option_change(self, *args):
        if hasattr(self, '_update_timer'):
            self.parent.after_cancel(self._update_timer)
        
        self.update_date_fields()
        
        if self.app.date_option.get() != "custom":
            self._update_timer = self.app.root.after(250, self.app.update_graph)


class FilterControls:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_filters_section()
    
    def setup_filters_section(self):
        filters_frame = ttk.LabelFrame(self.parent, text="FILTERS")
        filters_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.app.item_vars = {}
        
        for cat_key, cat_info in self.app.processor.CATEGORIES.items():
            cat_frame = ttk.Frame(filters_frame, relief="groove", borderwidth=1)
            cat_frame.pack(fill=tk.X, padx=5, pady=2)
            
            cat_header = ttk.Frame(cat_frame)
            cat_header.pack(fill=tk.X, padx=2, pady=2)
            
            cat_label = ttk.Label(cat_header, text=cat_info['name'], font=('TkDefaultFont', 9, 'bold'))
            cat_label.pack(side=tk.LEFT)
            
            var = tk.BooleanVar()
            self.app.item_vars[cat_key] = {'all': var, 'items': {}}
            
            all_check = ttk.Checkbutton(cat_header, text="All", variable=var,
                                      command=lambda ck=cat_key: self.app.toggle_category(ck))
            all_check.pack(side=tk.RIGHT)
            
            items_frame = ttk.Frame(cat_frame)
            items_frame.pack(fill=tk.X, padx=2, pady=2)
            
            for item in cat_info['items']:
                item_var = tk.BooleanVar()
                self.app.item_vars[cat_key]['items'][item] = item_var
                
                cb = ttk.Checkbutton(items_frame, text=item, variable=item_var,
                                   command=self.app.update_graph, padding=0)
                cb.pack(anchor=tk.W, pady=0)


class ScrollableControlPanel:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_scrollable_panel()
    
    def setup_scrollable_panel(self):
        frame_wrapper = ttk.Frame(self.parent)
        frame_wrapper.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        control_canvas = tk.Canvas(frame_wrapper, highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(frame_wrapper, orient=tk.VERTICAL, command=control_canvas.yview)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        control_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        content_frame = ttk.Frame(control_canvas)
        
        control_canvas.configure(yscrollcommand=scrollbar.set)
        
        window_id = control_canvas.create_window((0, 0), window=content_frame, anchor="nw", width=160)
        
        self._configure_scrolling_events(content_frame, control_canvas, window_id, frame_wrapper)
        
        self._add_controls(content_frame)
        
        self.parent.update_idletasks()
        control_canvas.configure(scrollregion=control_canvas.bbox("all"))
    
    def _configure_scrolling_events(self, content_frame, control_canvas, window_id, frame_wrapper):
        content_frame.bind(
            "<Configure>", 
            lambda e: control_canvas.configure(scrollregion=control_canvas.bbox("all"))
        )
        
        control_canvas.bind(
            "<Configure>", 
            lambda e: control_canvas.itemconfig(window_id, width=e.width)
        )
        
        for widget in [frame_wrapper, content_frame, control_canvas]:
            widget.bind(
                "<Enter>", 
                lambda e, canvas=control_canvas: canvas.focus_set() if canvas.winfo_exists() else None
            )
        
        def _on_mousewheel(event):
            shift = -1 if (event.num == 4 or event.delta > 0) else 1
            control_canvas.yview_scroll(shift, "units")
            return "break"
        
        control_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        control_canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        control_canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        
        control_canvas.bind_all("<2>", lambda e: "break")
        control_canvas.bind_all(
            "<B2-Motion>", 
            lambda e: control_canvas.yview_scroll(-1*(e.y-control_canvas.winfo_rooty()), "units")
        )
    
    def _add_controls(self, parent):
        PeriodControls(parent, self.app)
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)
        FilterControls(parent, self.app)