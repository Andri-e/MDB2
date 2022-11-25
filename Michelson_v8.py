# Todo 
# Scale to the slider thing 
# count the rings and movements to calculate lamda  
# Check touch pad compatability 
# Drop down box so we can change wavelength             Let agni know if an issue 


#! /usr/bin/env python
from LightPipes import *                    # https://opticspy.github.io/lightpipes/ 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import tkinter as tk                        # https://realpython.com/python-gui-tkinter/ 


wavelength = 632.8*nm                     # wavelength of HeNe laser          nm is *e-7
gridsize = 10*mm                          # gridsize of the grid
N = 300                                   # number (NxN) of grid pixels
R = 3*mm                                  # laser beam radius                                     for mm *0.001
z1 = 20*cm                                # length of arm 1                   this is in cm        for cm *0.01
z2 = z1*2                                 # length of arm 2                   this is in cm
z3 = 2*cm                                 # distance laser to beamsplitter
z4 = 1*cm                                 # distance beamsplitter to screen
Rbs = 0.5                                 # reflection beam splitter
tx = 0.0*mrad; ty = 0.0*mrad              # tilt of mirror 1                  mrad ) 0.0
f = 100*cm                                # focal length of positive lens


def get_current_value():
    return '{: .2f}'.format(current_value.get())

def calc_pattern():
    z2_temp = z2 - z1
    #Generate a weak converging laser beam using a weak positive lens:
    F = Begin(gridsize,wavelength,N)
    F = GaussBeam(F, R)
    F = Lens(f, 0, 0, F)

    #Propagate to the beamsplitter:
    F = Forvard(z3, F)

    #Split the beam and propagate to mirror #2:
    F2 = IntAttenuator(1-Rbs, F)
    F2 = Forvard(z2_temp, F2)

    #Introduce tilt and propagate back to the beamsplitter:
    F2 = Tilt(tx, ty, F2)
    F2 = Lens(f, 0, 0, F2)
    F2 = Forvard(z2_temp, F2)
    F2 = IntAttenuator(Rbs, F2)

    #Split off the second beam and propagate to- and back from the mirror #1:
    F10 = IntAttenuator(Rbs, F)
    F1 = Forvard(z1*2, F10)
    F1 = IntAttenuator(1-Rbs, F1)

    #Recombine the two beams and propagate to the screen:
    F = BeamMix(F1, F2)
    F = Forvard(z4, F)
    I = Intensity(1, F)

    return I


def slider_changed( event ):    
    z1 = current_value.get()  
    z2_updated = z2 - z1 
    print( z1 )      
    value_label.configure( text = get_current_value() )
    # updateing with new values 
    #Generate a weak converging laser beam using a weak positive lens:
    F = Begin(gridsize, wavelength, N)
    F = GaussBeam(F, R)
    F = Lens(f, 0, 0, F)

    #Propagate to the beamsplitter:
    F = Forvard(z3, F)

    #Split the beam and propagate to mirror #2:
    F2 = IntAttenuator(1-Rbs, F)
    F2 = Forvard(z2_updated, F2)

    #Introduce tilt and propagate back to the beamsplitter:
    F2 = Tilt(tx, ty, F2)
    F2 = Lens(f, 0, 0, F2)
    F2 = Forvard(z2_updated, F2)
    F2 = IntAttenuator(Rbs, F2)

    #Split off the second beam and propagate to- and back from the mirror #1:
    F10 = IntAttenuator(Rbs, F)
    F1 = Forvard(z1*2, F10)
    F1 = IntAttenuator(1-Rbs, F1)

    #Recombine the two beams and propagate to the screen:
    F = BeamMix(F1, F2)
    F = Forvard(z4, F)
    I = Intensity(1, F)

    subp.clear()
    #subp.imshow(I, cmap = 'jet'); plt.axis('off'); plt.title('intensity pattern')
    subp.axis('off')
    subp.imshow(I, cmap='gist_heat'); #plt.axis('off'); plt.title('intensity pattern')
    canvas.draw()


master = tk.Tk()

master.configure(bg="black")
master.columnconfigure(0, weight=1)
master.rowconfigure(0, weight=1)

# slider current value
current_value = tk.DoubleVar()
current_value.set(z1)

#  slider
slider = tk.Scale(
    master,
    from_ = 0.16,
    to = 0.31,
    orient = 'horizontal',  # vertical
    width = 100,
    sliderlength = 150,
    command = slider_changed,
   # variable = current_value,
    resolution = 0.0001,
    bg = "black",
    fg = "white",
    activebackground = "red",
    font = ("Arial", 30)
)

slider.grid(
    column = 0,
    row = 99,                     # high number = bottom of thing
    sticky = 'we'
)

fig = Figure(figsize=(20,20))
subp = fig.add_subplot(111)
fig.patch.set_facecolor("black")

I_start = calc_pattern()
#subp.imshow(I_start, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
subp.axis('off')
subp.imshow(I_start, cmap='gist_heat'); #plt.axis('off'); plt.title('intensity pattern')

canvas = FigureCanvasTkAgg(fig, master)

canvas.get_tk_widget().configure(background='black')
canvas._tkcanvas.config(bg="black")

canvas.get_tk_widget().grid(column=0, row=0, sticky = "nsew")
canvas.draw()


# current value label
# current_value_label = tk.Label(
#     master,
#     text='Current Value:',
#     font=("Arial", 30),
#     bg="black",
#     fg="white"
# )

# current_value_label.grid(
#     row = 3,
#     columnspan = 2,
#     sticky = 'n',
#     ipadx = 10,
#     ipady = 10
# )

# value label
value_label = tk.Label(
    master,
    text = get_current_value(),
    font = ("Arial", 30),
    bg = "black",
    fg = "white"
)
# value_label.grid(
#     row = 4,
#     columnspan = 2,
#     sticky = 'n'
# )

master.mainloop()

