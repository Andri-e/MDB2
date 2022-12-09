import tkinter as tk
from tkinter import ttk, Canvas, BOTH, Label, Frame, NW
from PIL import ImageTk, Image

class grid_pos:
    x0 = 50

    x1 = 280
    y1 = 50

    x2 = 450
    y2 = 150

pos_scale = 500

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('600x400')
        self.title('Toplevel Window')

        self.canvas = Canvas(self, background="white")
        self.canvas.pack(fill=BOTH, expand=1)

        self.laser_img = Image.open("Images/laser.png")
        self.laser_img = self.laser_img.resize((90, 15), Image.ANTIALIAS)
        self.laser_img = ImageTk.PhotoImage(self.laser_img)

        self.splitter_img = Image.open("Images/splitter.png")
        self.splitter_img = self.splitter_img.resize((90, 15), Image.ANTIALIAS)
        self.splitter_img = ImageTk.PhotoImage(self.splitter_img.rotate(45, expand=True))

        self.mirror_image = Image.open("Images/mirror.png")
        self.mirror_image = self.mirror_image.resize((90, 15), Image.ANTIALIAS)
        self.mirror_image1 = ImageTk.PhotoImage(self.mirror_image)
        self.mirror_image2 = ImageTk.PhotoImage(self.mirror_image.rotate(90, expand=True))

        self.laser_canvas = self.canvas.create_image(grid_pos.x0,
                                                     grid_pos.y2+33,
                                                     anchor=NW,
                                                     image=self.laser_img)

        self.splitter_canvas = self.canvas.create_image(grid_pos.x1 + 6,
                                                        grid_pos.y2+3,
                                                        anchor=NW,
                                                        image=self.splitter_img)
        self.mirror_canvas1 = self.canvas.create_image(grid_pos.x1,
                                                       grid_pos.y1,
                                                       anchor=NW,
                                                       image=self.mirror_image1)
        self.mirror_canvas2 = self.canvas.create_image(grid_pos.x2,
                                                       grid_pos.y2,
                                                       anchor=NW,
                                                       image=self.mirror_image2)

        self.canvas.create_line(grid_pos.x1+45,
                                grid_pos.y2+40,
                                grid_pos.x1+45,
                                grid_pos.y1+15,
                                width=3,
                                fill='red')

        self.laser1 = self.canvas.create_line(grid_pos.x1+45,
                                              grid_pos.y2+40,
                                              grid_pos.x2,
                                              grid_pos.y2+40,
                                              width=3,
                                              fill='red')
        self.canvas.create_line(grid_pos.x0+90,
                                grid_pos.y2+40,
                                grid_pos.x1+45,
                                grid_pos.y2+40,
                                width=3,
                                fill='red')

        self.z1_label = ttk.Label(self,text="Z1 = 0.2")
        self.z1_label.place(x=0, y=0)

        self.scale_label = ttk.Label(self,text="Model not to scale")
        self.scale_label.place(x=0, y=20)


Z1_temp=0.2

def update_text(window,z1, z2):
    ttk.Label(window,
              text=f"Z1 = {z1}").place(x=0, y=0)
    window.canvas.moveto(window.mirror_canvas2,
                         grid_pos.x2-(pos_scale/5)+z1*pos_scale,
                         grid_pos.y2
                         )

    window.canvas.coords(window.laser1,
                         grid_pos.x1+45,
                         grid_pos.y2+40,
                         grid_pos.x2-(pos_scale/5)+z1*pos_scale,
                         grid_pos.y2+40)



def slider_update_event(window, z1, z2_updated):
    update_text(window,z1, z2_updated)
    pass


def init(master):
    window = Window(master)
    window.grab_set()
