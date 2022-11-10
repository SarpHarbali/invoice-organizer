import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, name, dimensions):
        super().__init__()
        self.name = name
        self.dimensions = dimensions
        self.title(self.name)
        self.geometry(self.dimensions)

class Others(tk.Toplevel):
    def __init__(self, parent, name, dimensions):
        super().__init__(parent)
        self.name = name
        self.dimensions = dimensions
        self.title(self.name)
        self.geometry(self.dimensions)