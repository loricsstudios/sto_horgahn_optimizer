# experiments with chatgpt and python gui library TKinter

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import ImageTk, Image
from enum import Enum
from math import pow, sqrt
from sys import float_info
import logging
from functools import partial

log = logging.Logger('default')
log.setLevel(logging.WARN)


class Node:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

class mode(Enum):
    ADD = 1
    EDIT = 2

def dist(node, x, y):
    return( sqrt(pow(x - node.x, 2) + pow(y-node.y, 2)))

def get_nearest(nodes, x, y):
    ret = None
    mindist = float_info.max
    for node in nodes:
        checkdist = dist(node, x, y)
        if(checkdist<mindist):
            mindist = checkdist
            ret = node
    return ret
    

class App:
    def __init__(self):
        self.mode = mode.ADD
        self.nodes = []
        self.mode_status_text = None
        self.nodes_status_text = None

    def nodes_clear(self):
        self.nodes = []
        self.nodes_status_text.delete(1.0, tk.END)

    def mode_switch(self, to_mode):
        log.warning(f'Mode switching to: {to_mode}')
        self.mode = to_mode
        self.mode_status_text.config(text = f'App mode: {self.mode}')

    def process(self, event):
        log.warning(self.nodes)
        match self.mode:
            case mode.ADD:
                self.nodes.append(Node(event.x, event.y, self.nodes.count))
                self.nodes_status_text.insert(tk.END, f"Clicked at ({event.x}, {event.y})\n")
            case mode.EDIT:
                nearest = get_nearest(self.nodes, event.x, event.y)
                log.warning(f'Nearest node found: {nearest}')
                # find nearest, start dragging it until mouse released

def print_location(event):
    x = event.x
    y = event.y
    print(f"Clicked at ({x}, {y})")

def open_image():
    # Prompt the user to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    # Load the selected image
    if file_path:
        image = Image.open(file_path)
        width, height = image.size

        # Calculate the scale factor to fit the image within the window
        max_width = root.winfo_screenwidth() - 300
        max_height = root.winfo_screenheight() - 300
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Clear the canvas
        canvas.delete("all")

        # Convert the image to PhotoImage and display it on the canvas
        photo = ImageTk.PhotoImage(image)
        canvas.config(width=new_width, height=new_height)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo



mainapp = App()

root = tk.Tk()


label = tk.Label(root, text=f'App mode: {mainapp.mode}')
label.grid(column=0, row=0)

# Create a canvas to display the image
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(column=0, row=1, rowspan=5)

# Create an "Open Image" button
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.grid(column=1, row=1)
# open_button.pack()

add_button = tk.Button(root, text="Add Nodes", command=partial(mainapp.mode_switch, mode.ADD)) # mode.ADD
add_button.grid(column=1, row=2)

add_button = tk.Button(root, text="Edit Nodes", command=partial(mainapp.mode_switch, mode.EDIT)) #mode.EDIT
add_button.grid(column=1, row=3)

add_button = tk.Button(root, text="Clear Nodes", command=mainapp.nodes_clear)
add_button.grid(column=1, row=4)

# Add a text box to display the clicked locations
textbox = scrolledtext.ScrolledText(root, width=30, height=10)
textbox.grid(column=1, row=0)


mainapp.nodes_status_text = textbox
mainapp.mode_status_text = label

# Function to handle mouse click events on the canvas
def canvas_click(event):
    # Print the clicked location
    print_location(event)

    # Add the clicked location to the text box
    
    mainapp.process(event) # depending on mode

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", canvas_click)

root.mainloop()
