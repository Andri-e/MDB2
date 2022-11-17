import tkinter as tk

import numpy as np


def _photo_image(image: np.ndarray):
    height, width = image.shape
    data = f'P5 {width} {height} 255 '.encode() + image.astype(np.uint8).tobytes()
    return tk.PhotoImage(width=width, height=height, data=data, format='PPM')


root = tk.Tk()

array = np.ones((40, 40)) * 255
img = _photo_image(array)

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()
canvas.create_image(20, 20, anchor="nw", image=img)

root.mainloop()