# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

# Function for opening the
# file explorer window


def browseDirectories():
    filename = filedialog.askdirectory(initialdir='/',
                                          title='Select a Directory to sort')

    # Change label contents
    label_file_explorer.configure(text=f'Directory Opened: {filename}')


# Create the root window
window = Tk()

# Set window title
window.title('File Sort')

# Set window size
window.geometry('400x400')

#Set window background color
window.config(background='white')

# Create a File Explorer label
label_file_explorer = Label(window,
                            text='Select a directory to sort',
                            width=100, height=4,
                            fg="blue")


button_explore = Button(window,
                        text="Browse Files",
                        command=browseDirectories)

button_exit = Button(window,
                    text="Exit",
                    command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.pack()

button_explore.pack()

button_exit.pack()

# Let the window wait for any events
window.mainloop()
