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

        self.geometry('600x500')
        self.title('Toplevel Window')

        self.canvas = Canvas(self, background="white")
        self.canvas.pack(fill=BOTH, expand=1)

        self.laser_img = Image.open("Images/laser.png")
        self.laser_img = self.laser_img.resize((90, 15), Image.ANTIALIAS)
        self.laser_img = ImageTk.PhotoImage(self.laser_img)

        self.cam_img = Image.open("Images/cam.png")
        self.cam_img = self.cam_img.resize((40, 40), Image.ANTIALIAS)
        self.cam_img = ImageTk.PhotoImage(self.cam_img)

        self.splitter_img = Image.open("Images/splitter.png")
        self.splitter_img = self.splitter_img.resize((90, 15), Image.ANTIALIAS)
        self.splitter_img = ImageTk.PhotoImage(self.splitter_img.rotate(45, expand=True))

        self.mirror_image = Image.open("Images/mirror.png")
        self.mirror_image = self.mirror_image.resize((90, 15), Image.ANTIALIAS)
        self.mirror_image1 = ImageTk.PhotoImage(self.mirror_image)
        self.mirror_image2 = ImageTk.PhotoImage(self.mirror_image.rotate(90, expand=True))

        self.lens_img = Image.open("Images/concave_lens.png")
        self.lens_img = self.lens_img.resize((90, 15), Image.ANTIALIAS)
        self.lens_img = ImageTk.PhotoImage(self.lens_img)

        self.laser_canvas = self.canvas.create_image(grid_pos.x0,
                                                     grid_pos.y2+33,
                                                     anchor=NW,
                                                     image=self.laser_img)

        self.splitter_canvas = self.canvas.create_image(grid_pos.x1 + 6,
                                                        grid_pos.y2+3,
                                                        anchor=NW,
                                                        image=self.splitter_img)
        self.mirror_stationary = self.canvas.create_image(grid_pos.x1,
                                                          grid_pos.y1,
                                                          anchor=NW,
                                                          image=self.mirror_image1)
        self.mirror_moving = self.canvas.create_image(grid_pos.x2,
                                                      grid_pos.y2,
                                                      anchor=NW,
                                                      image=self.mirror_image2)

        self.lens_canvas = self.canvas.create_image(grid_pos.x1,
                                                    grid_pos.y2+200,
                                                    anchor=NW,
                                                    image=self.lens_img)

        self.cam_canvas = self.canvas.create_image(grid_pos.x1+25,
                                                    grid_pos.y2+280,
                                                    anchor=NW,
                                                    image=self.cam_img)

        self.canvas.create_line(grid_pos.x1+45,
                                grid_pos.y2+40,
                                grid_pos.x1+45,
                                grid_pos.y1+15,
                                width=3,
                                fill='red')

        self.canvas.create_line(grid_pos.x1+45,
                                grid_pos.y2+40,
                                grid_pos.x1+45,
                                grid_pos.y2+210,
                                width=3,
                                fill='red')

        points = [grid_pos.x1+45, grid_pos.y2+190,
                  grid_pos.x1+35, grid_pos.y2+280,
                  grid_pos.x1+55, grid_pos.y2+280]
        self.canvas.create_polygon(points, width=3, fill='red')

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

        self.scale_label = ttk.Label(self,text="Model not to scale")
        self.scale_label.place(x=0, y=0)

        self.pointing_line = self.canvas.create_line(grid_pos.x2+1,
                                                     grid_pos.y2+89,
                                                     grid_pos.x2+1,
                                                     grid_pos.y2+89+40,
                                                     width=2,
                                                     fill='black')
        self.canvas.create_line(grid_pos.x2-pos_scale*0.04+1,
                                grid_pos.y2+100,
                                grid_pos.x2+pos_scale*0.11+1,
                                grid_pos.y2+100,
                                width=2,
                                fill='black') #scale line horizontal

        self.canvas.create_line(grid_pos.x2-pos_scale*0.04+1,
                                grid_pos.y2+100,
                                grid_pos.x2-pos_scale*0.04+1,
                                grid_pos.y2+90,
                                width=2,
                                fill='black') #scale line delimiter 1

        self.canvas.create_text(grid_pos.x2-pos_scale*0.10, grid_pos.y2+95,  text='16 mm')

        self.canvas.create_line(grid_pos.x2+pos_scale*0.11+1,
                                grid_pos.y2+100,
                                grid_pos.x2+pos_scale*0.11+1,
                                grid_pos.y2+90,
                                width=2,
                                fill='black') #scale line delimiter 2

        self.canvas.create_text(grid_pos.x2+pos_scale*0.15, grid_pos.y2+95,  text='31 mm')

        self.pointing_label = self.canvas.create_text(grid_pos.x2+25, grid_pos.y2+90+34,  text='20.0 mm')

        # Item labels
        self.canvas.create_text(grid_pos.x1+20, grid_pos.y1-10,  text='Mirror')
        self.canvas.create_text(grid_pos.x1, grid_pos.y2+20,  text='Beam splitter')
        self.canvas.create_text(grid_pos.x1-10, grid_pos.y2+300,  text='Viewpoint')
        self.canvas.create_text(grid_pos.x0+30, grid_pos.y2+18,  text='Laser')
        self.canvas.create_text(grid_pos.x1, grid_pos.y2+190,  text='Concave lens')
        self.mirror_label = self.canvas.create_text(grid_pos.x2+4, grid_pos.y2-7,  text='Mirror')


def update_text(window,z1, z2):
    pos = int(grid_pos.x2-(pos_scale/5)+z1*pos_scale)
    window.canvas.moveto(window.mirror_moving,
                         pos,
                         grid_pos.y2
                         )

    window.canvas.coords(window.laser1,
                         grid_pos.x1+45,
                         grid_pos.y2+40,
                         grid_pos.x2-(pos_scale/5)+z1*pos_scale,
                         grid_pos.y2+40)

    window.canvas.coords(window.pointing_line,
                         pos+1,
                         grid_pos.y2+89,
                         pos+1,
                         grid_pos.y2+89+40)

    window.canvas.coords(window.pointing_label,
                         pos+25,
                         grid_pos.y2+90+34)

    window.canvas.coords(window.mirror_label,
                         pos+4, grid_pos.y2-7)

    window.canvas.itemconfigure(window.pointing_label, text=f"{z1*100:.1f} mm")




def slider_update_event(window, z1, z2_updated):
    update_text(window, z1, z2_updated)
    pass


def init(master):
    window = Window(master)
    window.grab_set()
