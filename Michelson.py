# Todo 
# Scale to the slider thing 
# count the rings and movements to calculate lamda  
# Check touch pad compatability 
# Drop down box so we can change wavelength             Let agni know if an issue 


#! /usr/bin/env python
from operator import truediv
from LightPipes import *                    # https://opticspy.github.io/lightpipes/ 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import Visualizer

import tkinter as tk                        # https://realpython.com/python-gui-tkinter/

import cProfile


wavelength = 632.8*nm                     # wavelength of HeNe laser          nm is *e-7
gridsize = 10*mm                          # gridsize of the grid
N = 300                                   # number (NxN) of grid pixels
R = 3*mm                                  # laser beam radius                                     for mm *0.001
z1 = 16*cm                                # length of arm 1                   this is in cm        for cm *0.01
z2 = z1*2                                 # length of arm 2                   this is in cm
z3 = 2*cm                                 # distance laser to beamsplitter
z4 = 1*cm                                 # distance beamsplitter to screen
Rbs = 0.5                                 # reflection beam splitter
tx = 0.0*mrad; ty = 0.0*mrad              # tilt of mirror 1                  mrad ) 0.0
f = 100*cm                                # focal length of positive lens


class MyCircularQueue():

    def __init__(self, k):
        self.k = k
        self.queue = [None] * k
        self.head = self.tail = -1
        self.ring_counter = 0 
        self.z1_init = 16*cm
        self.change = 0
        self.z1_last = 16*cm

    # Insert an element into the circular queue
    def enqueue(self, data):

        if ((self.tail + 1) % self.k == self.head):
            # print("The circular queue is full\n")
            # add a remove thing here 
            self.dequeue()

        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.k
            self.queue[self.tail] = data

    # Delete an element from the circular queue
    def dequeue(self):
        if (self.head == -1):
            print("The circular queue is empty\n")

        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.k
            return temp

    def printCQueue(self):
        if(self.head == -1):
            print("No element in the circular queue")

        elif (self.tail >= self.head):
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=" ")
            print()
        else:
            for i in range(self.head, self.k):
                print(self.queue[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.queue[i], end=" ")
            print()

    def check_peak(self, z1):
        if ((self.queue[self.head]) == None) or ((self.queue[self.head - 1]) == None):
            return
        if (self.queue[self.head]) <= (self.queue[self.head - 1]):
            return
  
        if (self.queue[self.head - 1]) < (self.queue[self.head - 2]):
            #print("No longer growing -> one ring?")
            if z1 > self.z1_last:
                self.ring_counter = self.ring_counter + 1
                self.z1_last = z1

            elif z1 < self.z1_last:
                self.ring_counter = self.ring_counter - 1
                self.z1_last = z1

            elif z1 == self.z1_last:
                self.ring_counter = self.ring_counter + 1
                self.z1_last = z1
                print("same")

            else:
                print("Error")
            print(self.ring_counter)

    def print_rings(self):
        print(self.ring_counter)

    def track_change(self, z1):
        self.change = abs(z1 - self.z1_init)
        #print(self.change)

    def print_lambda(self): 
        #print("Uhh, need to figure out the formula but we have change in mm? and the ring count")
        if self.ring_counter != 0:
            #print(2*self.change/self.ring_counter)
            lambda_value = 2*self.change/self.ring_counter
            print(lambda_value)
            lambda_label.configure( text = "Lambda: " + str(lambda_value) )
        else:
            print(f"Change: {self.change}, zero division")

queue_object = MyCircularQueue(3)

queue_object.enqueue(1)
queue_object.enqueue(1)
queue_object.enqueue(1)



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

    #Calculateing the Lambda 
    queue_object.enqueue(I[255, 255])
    queue_object.check_peak(z1)
    queue_object.track_change(z1)
    queue_object.print_lambda()


    #For debuging 
    #queue_object.print_rings()
    #print(I[255,255])
    print( z1 )    

    subp.clear()
    #subp.imshow(I, cmap = 'jet'); plt.axis('off'); plt.title('intensity pattern')
    subp.axis('off')
    subp.imshow(I, cmap='gist_heat'); #plt.axis('off'); plt.title('intensity pattern')
    canvas.draw()

    Visualizer.slider_update_event(VIS, z1, z2_updated)


master = tk.Tk()
VIS = Visualizer.Window(master)

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
    variable = current_value,
    #resolution = 0.0001,
    resolution = 0.001,
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

master.geometry('1000x700')

# value label
value_label = tk.Label(
    master,
    text = get_current_value(),
    font = ("Arial", 30),
    bg = "black",
    fg = "white"
)

# lambda label
lambda_label = tk.Label(
    master,
    text = "Lambda: ",
    font = ("Arial", 20),
    bg = "black",
    fg = "white"
)

lambda_label.grid(
    column = 0,
    row = 1,                     # high number = bottom of thing
    sticky = 'we'
)

#master.after(20, Visualizer.init(master))

master.mainloop()

