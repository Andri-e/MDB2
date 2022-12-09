import tkinter as tk
from tkinter import ttk, Canvas, BOTH, Label, Frame
from PIL import ImageTk, Image



class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('600x400')
        self.title('Toplevel Window')

        canvas = Canvas(self)
        canvas.create_line(20, 20, 50, 20, width=3)
        canvas.pack(fill=BOTH, expand=1)

        image = Image.open("Images/splitter.png")
        test = ImageTk.PhotoImage(image)
        label = tk.Label(image=test)
        label.image = test
        label.place(x=200, y=200)

        #frame = Frame(self, width=100, height=100)
        #frame.pack()
        #frame.place(anchor='center', relx=0.5, rely=0.5)

        #splitter_img = ImageTk.PhotoImage(Image.open("Images/splitter.png"))
        #splitter_label = Label(frame, image=splitter_img)
        #splitter_label.pack()



def update_text(window, text):
    ttk.Label(window,
              text=f"Z1 = {text}").place(x=0, y=0)



def slider_update_event(window, z1, z2_updated):
    update_text(window, z1)
    pass


def init(master):
    window = Window(master)
    window.grab_set()
