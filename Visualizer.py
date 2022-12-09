import tkinter as tk
from tkinter import ttk, Canvas, BOTH, Label, Frame, NW
from PIL import ImageTk, Image



class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('600x400')
        self.title('Toplevel Window')

        self.canvas = Canvas(self, background="white")
        self.canvas.pack(fill=BOTH, expand=1)

        self.splitter_img = Image.open("Images/splitter.png")
        self.splitter_img = self.splitter_img.resize((90, 15), Image.ANTIALIAS)
        self.splitter_img = ImageTk.PhotoImage(self.splitter_img)

        self.mirror_image = Image.open("Images/mirror.png")
        self.mirror_image = self.mirror_image.resize((90, 15), Image.ANTIALIAS)
        self.mirror_image1 = ImageTk.PhotoImage(self.mirror_image)
        self.mirror_image2 = ImageTk.PhotoImage(self.mirror_image.rotate(90))

        self.splitter_canvas = self.canvas.create_image(200, 20, anchor=NW, image=self.splitter_img)
        self.mirror_canvas1 = self.canvas.create_image(200, 40, anchor=NW, image=self.mirror_image1)
        self.mirror_canvas2 = self.canvas.create_image(250, 40, anchor=NW, image=self.mirror_image2)
        self.canvas.create_line(20, 20, 50, 20, width=3)


    #frame = Frame(self, width=100, height=100)
        #frame.pack()
        #frame.place(anchor='center', relx=0.5, rely=0.5)

        #splitter_img = ImageTk.PhotoImage(Image.open("Images/splitter.png"))
        #splitter_label = Label(frame, image=splitter_img)
        #splitter_label.pack()


Z1_temp=0.2

def update_text(window,z1, z2):
    ttk.Label(window,
              text=f"Z1 = {z1}").place(x=0, y=0)
    window.canvas.moveto(window.mirror_canvas1, z1*1000, 40)



def slider_update_event(window, z1, z2_updated):
    update_text(window,z1, z2_updated)
    pass


def init(master):
    window = Window(master)
    window.grab_set()
