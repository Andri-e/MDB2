#! /usr/bin/env python
from LightPipes import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import tkinter as tk                # https://realpython.com/python-gui-tkinter/ 


wavelength=632.8*nm                     # wavelength of HeNe laser          nm is *e-7
gridsize=10*mm                              # gridsize of the grid
N=300                                   # number (NxN) of grid pixels
R=3*mm                                  # laser beam radius                                     for mm *0.001
z1=8*cm                                 # length of arm 1                   this is in cm        for cm *0.01
z2=8*cm                                 # length of arm 2                   this is in cm
z3=2*cm                                 # distance laser to beamsplitter
z4=1*cm                                 # distance beamsplitter to screen
Rbs=0.5                                 # reflection beam splitter
tx=0.0*mrad; ty=0.0*mrad                # tilt of mirror 1                  mrad ) 0.0
f=100*cm                                # focal length of positive lens


def get_current_value():
    return '{: .2f}'.format(current_value.get())

def calc_pattern():
    wavelength=632.8*nm                     # wavelength of HeNe laser          nm is *e-7
    gridsize=10*mm                              # gridsize of the grid
    N=300                                   # number (NxN) of grid pixels
    R=3*mm                                  # laser beam radius                                     for mm *0.001
    z1=8*cm                                 # length of arm 1                   this is in cm        for cm *0.01
    z2=8*cm                                 # length of arm 2                   this is in cm
    z3=2*cm                                 # distance laser to beamsplitter
    z4=1*cm                                 # distance beamsplitter to screen
    Rbs=0.5                                 # reflection beam splitter
    tx=0.0*mrad; ty=0.0*mrad                # tilt of mirror 1                  mrad ) 0.0
    f=100*cm                                # focal length of positive lens


    #Generate a weak converging laser beam using a weak positive lens:
    F=Begin(gridsize,wavelength,N)
    F=GaussBeam(F, R)
    #F=GaussHermite(F,R,0,0,1) #new style
    #F=GaussHermite(F,R) #new style
    #F=GaussHermite(0,0,1,R,F) #old style
    F=Lens(f,0,0,F)

    #Propagate to the beamsplitter:
    F=Forvard(z3,F)

    #Split the beam and propagate to mirror #2:
    F2=IntAttenuator(1-Rbs,F)
    F2=Forvard(z2,F2)

    #Introduce tilt and propagate back to the beamsplitter:
    F2=Tilt(tx,ty,F2)
    F2=Lens(f,0,0,F2)
    F2=Forvard(z2,F2)
    F2=IntAttenuator(Rbs,F2)

    #Split off the second beam and propagate to- and back from the mirror #1:
    F10=IntAttenuator(Rbs,F)
    F1=Forvard(z1*2,F10)
    F1=IntAttenuator(1-Rbs,F1)

    #Recombine the two beams and propagate to the screen:
    F=BeamMix(F1,F2)
    F=Forvard(z4,F)
    I=Intensity(1,F)
    #print(np.shape(I))
    #plt.imshow(I, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
    #plt.show()

    return I

# def slider_changed(event):    
#     z1 = current_value.get()   
#     print(z1)      
#     value_label.configure(text=get_current_value())
#     # updateing with new values 
#     #Generate a weak converging laser beam using a weak positive lens:
#     F=Begin(gridsize,wavelength,N)
#     F=GaussBeam(F, R)
#     #F=GaussHermite(F,R,0,0,1) #new style
#     #F=GaussHermite(F,R) #new style
#     #F=GaussHermite(0,0,1,R,F) #old style
#     F=Lens(f,0,0,F)

#     #Propagate to the beamsplitter:
#     F=Forvard(z3,F)

#     #Split the beam and propagate to mirror #2:
#     F2=IntAttenuator(1-Rbs,F)
#     F2=Forvard(z2,F2)

#     #Introduce tilt and propagate back to the beamsplitter:
#     F2=Tilt(tx,ty,F2)
#     F2=Lens(f,0,0,F2)
#     F2=Forvard(z2,F2)
#     F2=IntAttenuator(Rbs,F2)

#     #Split off the second beam and propagate to- and back from the mirror #1:
#     F10=IntAttenuator(Rbs,F)
#     F1=Forvard(z1*2,F10)
#     F1=IntAttenuator(1-Rbs,F1)

#     #Recombine the two beams and propagate to the screen:
#     F=BeamMix(F1,F2)
#     F=Forvard(z4,F)
#     I=Intensity(1,F)
#     #plt.imshow(I, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
#     #plt.show()

#     subp.clear()
#     subp.imshow(I, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
#     canvas.draw()
    
#     """ img = tk.PhotoImage(file=I)      
#     canvas.create_image(20,20, anchor=tk.NW, image=img)  """


def slider_changed(event):    
    z1 = current_value.get()   
    print(z1)      
    value_label.configure(text=get_current_value())
    # updateing with new values 
    #Generate a weak converging laser beam using a weak positive lens:
    F=Begin(gridsize,wavelength,N)
    F=GaussBeam(F, R)
    #F=GaussHermite(F,R,0,0,1) #new style
    #F=GaussHermite(F,R) #new style
    #F=GaussHermite(0,0,1,R,F) #old style
    F=Lens(f,0,0,F)

    #Propagate to the beamsplitter:
    F=Forvard(z3,F)

    #Split the beam and propagate to mirror #2:
    F2=IntAttenuator(1-Rbs,F)
    F2=Forvard(z2,F2)

    #Introduce tilt and propagate back to the beamsplitter:
    F2=Tilt(tx,ty,F2)
    F2=Lens(f,0,0,F2)
    F2=Forvard(z2,F2)
    F2=IntAttenuator(Rbs,F2)

    #Split off the second beam and propagate to- and back from the mirror #1:
    F10=IntAttenuator(Rbs,F)
    F1=Forvard(z1*2,F10)
    F1=IntAttenuator(1-Rbs,F1)

    #Recombine the two beams and propagate to the screen:
    F=BeamMix(F1,F2)
    F=Forvard(z4,F)
    I=Intensity(1,F)
    #plt.imshow(I, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
    #plt.show()

    subp.clear()
    subp.imshow(I, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')
    canvas.draw()
    
    """ img = tk.PhotoImage(file=I)      
    canvas.create_image(20,20, anchor=tk.NW, image=img)  """


master = tk.Tk()


""" canvas = tk.Canvas(master, width = 300, height = 300)      
canvas.pack()   """

""" canvas = tk.Canvas(master, width = 300, height = 300)      
canvas.pack()      
img = tk.PhotoImage(file="ball.ppm")      
canvas.create_image(20,20, anchor=tk.NW, image=img)  """


""" 
# Original setup
#Generate a weak converging laser beam using a weak positive lens:
F=Begin(gridsize,wavelength,N)
F=GaussBeam(F, R)
#F=GaussHermite(F,R,0,0,1) #new style
#F=GaussHermite(F,R) #new style
#F=GaussHermite(0,0,1,R,F) #old style
F=Lens(f,0,0,F)

#Propagate to the beamsplitter:
F=Forvard(z3,F)

#Split the beam and propagate to mirror #2:
F2=IntAttenuator(1-Rbs,F)
F2=Forvard(z2,F2)

#Introduce tilt and propagate back to the beamsplitter:
F2=Tilt(tx,ty,F2)
F2=Lens(f,0,0,F2)
F2=Forvard(z2,F2)
F2=IntAttenuator(Rbs,F2)

#Split off the second beam and propagate to- and back from the mirror #1:
F10=IntAttenuator(Rbs,F)
F1=Forvard(z1*2,F10)
F1=IntAttenuator(1-Rbs,F1)

#Recombine the two beams and propagate to the screen:
F=BeamMix(F1,F2)
F=Forvard(z4,F)
I=Intensity(1,F)
#plt.imshow(I,cmap='jet'); plt.axis('off');plt.title('intensity pattern')
#plt.show()
 """



# Scales from https://python-course.eu/tkinter/sliders-in-tkinter.php#:~:text=A%20slider%20is%20a%20Tkinter,with%20the%20Scale%20method().
#w1 = tk.Scale(master, from_=0, to=42)
#w1.pack()
#w2 = tk.Scale(master, from_=0, to=200, orient=tk.HORIZONTAL)
#w2.pack()
#print(w1)
#tk.Button(master, text='Show', command=show_values).pack()

master.columnconfigure(0, weight=1)
master.rowconfigure(0, weight=1)

# slider current value
current_value = tk.DoubleVar()
current_value.set(z1)

#  slider
slider = tk.Scale(
    master,
    from_=0,
    to=0.2,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=current_value,
    resolution=0.0001
)

slider.grid(
    column=0,
    row=99,                     # high number = bottom of thing
    sticky='we'
)

fig = Figure(figsize=(10,10))
subp = fig.add_subplot(111)

I_start = calc_pattern()
#subp.plot(I_start[0], I_start[1])
subp.imshow(I_start, cmap='jet'); plt.axis('off'); plt.title('intensity pattern')

canvas = FigureCanvasTkAgg(fig, master)

# canvas = tk.Canvas(master, height=100, width=100)
# canvas.create_image(0,0,anchor="nw",image=calc_pattern())
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")


# current value label
current_value_label = tk.Label(
    master,
    text='Current Value:'
)

current_value_label.grid(
    row=3,
    columnspan=2,
    sticky='n',
    ipadx=10,
    ipady=10
)

# value label
value_label = tk.Label(
    master,
    text=get_current_value()
)
value_label.grid(
    row=4,
    columnspan=2,
    sticky='n'
)

master.mainloop()

