import tkinter as tk

class MenuBar:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        menubar = tk.Menu(parent)
        parent.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=parent.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=app.show_about)