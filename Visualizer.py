import tkinter as tk
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        self.my_label = ttk.Label(self,
                text="Test text").place(x=20,y=20)


def update_text(window, text):
    window.my_label = ttk.Label(window,
                                text= f"Z1 = {text}").place(x=20,y=20)


def slider_update_event(window, z1, z2_updated):
    update_text(window, z1)
    pass


def init(master):
    window = Window(master)
    window.grab_set()
