#
#  4/8/19
# --------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------ FRACTALGENERATOR.PY ------------------------------------------------------------
"""
Had to combine GENERATORCODE.PY, FRACTALGENUI.PY, and FRACPARAMETERS.PY into one file for easy packaging. Also removing header image, also for easy packaging.

Contains 3 parts:

    - FRACPARAMETERS.PY
        Parameter options for FRACGENUI.PY scrpit. Edit only the variables here, altering the GUI scrpit can break the app.

    - GENERATORCODE.PY
        Create and plot fractals and complex functions. Contains three methods:

            .createplane:   Creates an xy grid and a null array zmap
            .cgen:          Generates random values of c for julia set
            .julia:         Generates Julia set fractals for a given c

    - FRACTALGENUI.PY
        Creating a GUI for the fractal generation script I wrote in PHYS 129L.
        Editable parameters for fractal generation and GUI configuration are included in the FRACPARAMETERS.PY script.

"""
# 4/4/19 Additionally want to add:
#   - (frameoff = True) support to both preview and output
#   - save dialog to root window
#   - label option on output .png
#   - Mandlebrot set compatability
#   - Julia set z-power setting

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------








# --------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------ FRACPARAMETERS.PY ------------------------------------------------------------

# ------------------------------------------------------------ Imports ------------------------------------------------------------

import math
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt

# ------------------------------------------------------------ Settings ------------------------------------------------------------

class param():

    # Seed choice
    seed = 1

    # Z-power
    zpow = 2

    # Colormaps
    colormaps = [
    'nipy_spectral', 'gist_earth', 'gist_stern', 'CMRmap', 'inferno',
    'afmhot', 'cubehelix', 'twilight_shifted', 'viridis', 'gist_rainbow', 
    'plasma', 'autumn', 'Spectral', 'twilight', 'terrain' 
    ]

    # C-values
    cvalues = [
    (-0.4, 0.6), (-0.8, 0.156), (-0.7269, 0.1889),
    (-0.79, 0.15), (-0.162, 1.04), (0.28, .008)
    ]

    # Render window size
    rensize = ['256', '512', '1024', '2048', '4096']
    winsize = (6, 6)

    # Preview Resolution
    previewres = 128

    # C-gen bias and limits
    clim_x = .8
    clim_y = .5
    cbias = 0.3

    # Preview each random c-value automatically
    randompreview = True

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------








# --------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------ GENERATORCODE.PY ------------------------------------------------------------

# ------------------------------------------------------------ Julia function ------------------------------------------------------------

# Returns the quadratic julia set for a given c
def julia(plane, c, smooth = False, power = 2):
    # Defining the quadratic julia genelrating function f(z)
    def f(z, c, exp):
        f = z ** exp + c
        return f
    # Importing plane
    xx = plane[0]
    yy = plane[1]
    zmap = plane[2]
    xsize = len(xx[0])
    ysize = len(yy)
    # Resursion on each pixel. Reassigns z and n each iteration until abs(z) >= 2 or n == 255
    for x_i in range(xsize):
        for y_i in range(ysize):
            z = complex(xx[y_i, x_i], yy[y_i, x_i])
            n = 0
            # Checking if smooth is enabled
            if smooth == False:
                while abs(z) < 2 and n < 255:
                    z_n = f(z, c, power)
                    z = complex(z_n.real, z_n.imag)
                    n += 1
                zmap[y_i, x_i] = n 
            elif smooth == True:
                # Smoothing subtracts fractional amount from iteration count
                while abs(z) <= 2 and n < 255:
                    z_n = f(z, c, power)
                    z = complex(z_n.real, z_n.imag)
                    n += 1
                zmap[y_i, x_i] = n - math.log(abs(z), 2)
    # Returns array of zmap  
    return zmap

# ------------------------------------------------------------ Create plane ------------------------------------------------------------

# Creates and returns complex xy plane and empty zmap. Domain is x-distance +/- from the center. Center expects a touple and defaults to (0,0)
def createplane(resolution, domain = 2, center = (0, 0)):
    # Assigning coordinates to each pixel
    # Note: array indexing goes array[row,col] == array[y,x]
    x = np.linspace(center[0] - domain, center[0] + domain, resolution)
    y = np.linspace(center[1] - domain, center[1] + domain, resolution)
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros((resolution, resolution))
    return [xx, yy, zz]

# ------------------------------------------------------------ Random c-generation ------------------------------------------------------------

# Generates random values of c for julia set
def cgen(seed, xlim = 1, ylim = 1, bias = .5):
    np.random.seed(seed)
    choice = np.random.rand(4)
    x = choice[0] * xlim
    y = choice[1] * ylim
    if choice[2] >= bias:
        x = -x
    if choice[3] >= .5:
        y = -y
    return x, y

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------








# --------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------ FRACTALGENUI.PY ------------------------------------------------------------

# ------------------------------------------------------------ Initializing window ------------------------------------------------------------

# Initializing root window
root = tk.Tk()
root.title('Fractal Generator v1.1')
root.geometry('600x420')
#root.geometry('600x470')
root.resizable(False, False)
#icon = 'favicon.ico'
#root.iconbitmap(icon)

# Adding header image (DEPRECATED FOR NOW)
#img = tk.PhotoImage(file = "fractalgen_header.png")
#header = tk.Canvas(root, width = 600, height = 80)
#header.create_image(0, 0, anchor = 'nw', image=img)   
#header.grid(columnspan = 2, row = 0)
head = tk.Label(root, text = 'Fractal Generator (v1.1)', font = ('Times New Roman', 14, 'bold italic'))
head.grid(columnspan = 2, row = 0, pady = 5)

# Adding canvas
prev_fig = plt.figure(1, figsize = (3, 3), dpi = 100, frameon = False, facecolor = (1, 1, 1, 0))
ax_p = prev_fig.add_subplot(111)
plt.axis('off')
canvas = FigureCanvasTkAgg(prev_fig, root)
canvas.draw()
canvas.get_tk_widget().grid(column = 1, row = 1, rowspan = 5, padx = 15, pady = 10)

# ------------------------------------------------------------ Adding c-value ------------------------------------------------------------

# Manual c-entry boxes
c_frame = tk.Frame(root)
c_frame.grid(column = 0, row = 2, padx = 5)
c_label = tk.Label(c_frame, text = 'Set c-value or generate randomly:')
c_label.grid(columnspan = 5, row = 0, pady = 5)
c_val_lab = tk.Label(c_frame, text = 'c = ')
c_val_lab.grid(column = 0, row = 1, sticky = 'E')
real_val = tk.DoubleVar()
val1 = tk.Entry(c_frame, textvariable = real_val, width = 5)
val1.grid(column = 1, row = 1)
val1_lab = tk.Label(c_frame, text = ' + ')
val1_lab.grid(column = 2, row = 1)
imag_val = tk.DoubleVar()
val2 = tk.Entry(c_frame, textvariable = imag_val, width = 5)
val2.grid(column = 3, row = 1)
val2_lab = tk.Label(c_frame, text = 'i')
val2_lab.grid(column = 4, row = 1, sticky = 'W')

# Generate random c-value button
seed = param.seed
def c_click():
    global seed
    real, imag = cgen(seed, param.clim_x, param.clim_y, param.cbias)
    real_val.set(real)
    imag_val.set(imag)
    seed += 1
    if param.randompreview == True:
        resolution = param.previewres
        color = color_var.get()
        c = complex(real, imag)
        smooth = smooth_var.get()
        plane = createplane(resolution)
        fractal = julia(plane, c, smooth = smooth, power = param.zpow)
        ax_p.imshow(fractal, cmap = color)
        canvas.draw()
c_button = tk.Button(c_frame, text = 'Random', command = c_click)
c_button.grid(columnspan = 5, row = 2, pady = 3)

# Pick c-value presets
pick_frame = tk.Frame(root)
pick_frame.grid(column = 0, row = 3, padx = 5)
pick_lab = tk.Label(pick_frame, text = 'Or use a preset c-value:')
pick_lab.grid(columnspan = 2, row = 0, sticky = 'W')
pick_var = tk.StringVar()
options = param.cvalues
pick_options = range(1, len(options) + 1)
pick_options = [str(i) for i in pick_options]
pick_options.insert(0, '--Choose--')
pick_menu = tk.OptionMenu(pick_frame, pick_var, *pick_options)
pick_menu.configure(state = 'disabled')
pick_menu.grid(column = 1, row = 1, padx = 5)
pick_var.set(pick_options[0])

# Pick preset checkbox
pickchk_var = tk.BooleanVar()
pickchk_var.set(False)
def pick_click():
    temp = pickchk_var.get()
    if temp == True:
        pick_menu.configure(state = 'normal')
        val1.configure(state = 'disabled')
        val2.configure(state = 'disabled')
        c_button.configure(state = 'disabled')
    else:
        pick_menu.configure(state = 'disabled')
        val1.configure(state = 'normal')
        val2.configure(state = 'normal')
        c_button.configure(state = 'normal')
pickbox = tk.Checkbutton(pick_frame, text = 'Preset', variable = pickchk_var, command = pick_click)
pickbox.grid(column = 0, row = 1, padx = 5)

# ------------------------------------------------------------ Adding set selector ------------------------------------------------------------

# Defining functions
mandle = False
def mandle_click():
    val1.configure(state = 'disabled')
    val2.configure(state = 'disabled')
    c_button.configure(state = 'disabled')
    pickbox.configure(state = 'disabled')
    pick_menu.configure(state = 'disabled')
    global mandle
    mandle = True
def julia_click():
    pickbox.configure(state = 'normal')
    temp = pickchk_var.get()
    if temp == True:
        pick_menu.configure(state = 'normal')
        val1.configure(state = 'disabled')
        val2.configure(state = 'disabled')
        c_button.configure(state = 'disabled')
    else:
        pick_menu.configure(state = 'disabled')
        val1.configure(state = 'normal')
        val2.configure(state = 'normal')
        c_button.configure(state = 'normal')
    global mandle
    mandle = False

# Set type
type_frame = tk.Frame(root)
type_frame.grid(column = 0, row = 1, padx = 5, pady = 5)
type_label = tk.Label(type_frame, text ='Choose fractal set type:')
type_label.grid(columnspan = 2, row = 0)
julia_button = tk.Radiobutton(type_frame, text = 'Julia', value = 1, command = julia_click)
julia_button.grid(column = 0, row = 1)
julia_button.select()
mandle_button = tk.Radiobutton(type_frame, text = 'Mandlebrot', value = 2, command = mandle_click)
mandle_button.configure(state = 'disabled')
mandle_button.grid(column = 1, row = 1)

# ------------------------------------------------------------ Adding color choice ------------------------------------------------------------

color_frame = tk.Frame(root)
color_frame.grid(column = 0, row = 4, padx = 5, pady = 5)
color_label = tk.Label(color_frame, text ='Choose colormap:')
color_label.grid(column = 0, row = 0)
color_var = tk.StringVar()
color_options = param.colormaps
color_list = tk.OptionMenu(color_frame, color_var, *color_options)
color_list.grid(column = 1, row = 0)
color_var.set(color_options[0])

# ------------------------------------------------------------ Adding render size ------------------------------------------------------------

# Render size (restricted)
size_frame = tk.Frame(root)
size_frame.grid(column = 0, row = 5, padx = 5, pady = 5)
genrestrict_label = tk.Label(size_frame, text ='Canvas size (restricted):')
genrestrict_label.grid(column = 0, row = 0)
size_var = tk.StringVar()
size_options = param.rensize
size_list = tk.OptionMenu(size_frame, size_var, *size_options)
size_list.grid(column = 1, row = 0)
size_var.set(size_options[0])

# Render size (unrestricted)
genfree_label = tk.Label(size_frame, text ='Canvas size (unrestricted):')
genfree_label.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'E')
res_var = tk.StringVar()
res_ent = tk.Entry(size_frame, textvariable = res_var, state = 'disabled', width = 10)
res_ent.grid(column = 1, row = 2, sticky = 'W', padx = 5, pady = 5)

# Unrestrict checkbox
unrest_var = tk.BooleanVar()
unrest_var.set(False)
def restrict_click():
    temp = unrest_var.get()
    if temp == True:
        res_ent.configure(state = 'normal')
        size_list.configure(state = 'disabled')
    else:
        res_ent.configure(state = 'disabled')
        size_list.configure(state = 'normal')
unrest = tk.Checkbutton(size_frame, text = 'Unrestricted', variable = unrest_var, command = restrict_click)
unrest.grid(column = 1, row = 1, sticky = 'E', padx = 3, pady = 3)

# ------------------------------------------------------------ Adding render options ------------------------------------------------------------

# Smooth option checkbox
smooth_frame = tk.Frame(root)
smooth_frame.grid(column = 0, row = 6, padx = 5)
smooth_var = tk.BooleanVar()
smooth_var.set(True)
smoothbox = tk.Checkbutton(smooth_frame, text = 'Smooth', variable = smooth_var)
smoothbox.grid(column = 0, row = 0)
smoothbox.select()

# Label checkbox (UNDER CONSTRUCTION)
labelbox = tk.Checkbutton(smooth_frame, text = 'Label')
labelbox.grid(column = 1, row = 0)
labelbox.configure(state = 'disabled')

# ------------------------------------------------------------ Adding preview ------------------------------------------------------------

# Generating preview
def prev_click():

    # Fractal parameters
    resolution = param.previewres
    color = color_var.get()
    if pickchk_var.get() == True:
        choice = options[int(pick_var.get()) - 1]
        c = complex(choice[0], choice[1])
    else:
        c = complex(real_val.get(), imag_val.get())
    smooth = smooth_var.get()

    # Catching errors while drawing
    try:
        plane = createplane(resolution)
        fractal = julia(plane, c, smooth = smooth, power = param.zpow)
        ax_p.imshow(fractal, cmap = color)
        canvas.draw()
    except:
        tk.messagebox.showerror('Math Domain Error', 'You must enter, generate, or pick a value for c.\nIf you have a value entered then this is an unecxpected error.')

# Preview button
render_frame = tk.Frame(root)
render_frame.grid(column = 1, row = 6, padx = 5, pady = 10)
prev_button = tk.Button(render_frame, text = 'Preview', command = prev_click)
prev_button.grid(column = 0, row = 1)

# ------------------------------------------------------------ Adding generator ------------------------------------------------------------

# Generating render
def generate_click():

    # Fractal parameters
    if unrest_var.get() == True:
        resolution = int(res_var.get())
    else:
        resolution = int(size_var.get())
    color = color_var.get()
    if pickchk_var.get() == True:
        choice = options[int(pick_var.get()) - 1]
        c = complex(choice[0], choice[1])
    else:
        c = complex(real_val.get(), imag_val.get())
    smooth = smooth_var.get()

    # Catching errors in drawing
    try:
        
        # Generating fractal
        plane = createplane(resolution)
        fractal = julia(plane, c, smooth = smooth, power = param.zpow)

        # Generating figure
        render = plt.figure(2, figsize = param.winsize, dpi = 100, frameon = False)
        plt.clf()
        ax_r = render.add_subplot(111)
        plt.axis('off')
        ax_r.imshow(fractal, cmap = color)

        # Generating window
        win = tk.Toplevel()
        win.resizable(False, False)
        graph = FigureCanvasTkAgg(render, win)
        toolbar = NavigationToolbar2Tk(graph, win)
        toolbar.update()
        graph.get_tk_widget().pack()
        graph.draw()
    
    # Errors
    except:
        tk.messagebox.showerror('Math Domain Error', 'You must enter, generate, or pick a value for c.\nIf you have a value entered then this is an unecxpected error.')

# Generator button
gen_button = tk.Button(render_frame, text = 'Generate', command = generate_click)
gen_button.grid(column = 1, row = 1)

# ------------------------------------------------------------ Closing window ------------------------------------------------------------
root.mainloop()