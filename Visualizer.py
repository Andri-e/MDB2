import tkinter as tk
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                   text='Close',
                   command=self.destroy).pack(expand=True)


def slider_update_event(d):
    pass


def init(master):
    window = Window(master)
    window.grab_set()
