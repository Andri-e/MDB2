#! /usr/bin/env python
from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import tkinter as tk                # https://realpython.com/python-gui-tkinter/ 


wavelength=632.8*nm                     # wavelength of HeNe laser
size=10*mm                              # size of the grid
N=300                                   # number (NxN) of grid pixels
R=3*mm                                  # laser beam radius
z1=8*cm                                 # length of arm 1
z2=8*cm                                 # length of arm 2
z3=2*cm                                 # distance laser to beamsplitter
z4=1*cm                                 # distance beamsplitter to screen
Rbs=0.5                                 # reflection beam splitter
tx=0.0*mrad; ty=0.0*mrad                # tilt of mirror 1
f=100*cm                                # focal length of positive lens


def show_values():                      
    print (z1.get(), z2.get())

#Generate a weak converging laser beam using a weak positive lens:
F=Begin(size,wavelength,N)
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


plt.imshow(I,cmap='jet'); plt.axis('off');plt.title('intensity pattern')
plt.show()

master = tk.Tk()

# Scales from https://python-course.eu/tkinter/sliders-in-tkinter.php#:~:text=A%20slider%20is%20a%20Tkinter,with%20the%20Scale%20method().
#w1 = tk.Scale(master, from_=0, to=42)
#w1.pack()
#w2 = tk.Scale(master, from_=0, to=200, orient=tk.HORIZONTAL)
#w2.pack()
#print(w1)
#tk.Button(master, text='Show', command=show_values).pack()

z1 = tk.Scale(master, from_=0, to=42)
z1.pack()
z2 = tk.Scale(master, from_=0, to=200, orient=tk.HORIZONTAL)
z2.pack()
tk.Button(master, text='Show', command=show_values).pack()

master.mainloop()