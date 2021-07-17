import os
from tkinter import messagebox ,scrolledtext ,filedialog

import tkinter as tk
from tkinter.constants import END, LEFT, TOP
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory, askopenfilename
import script


root = tk.Tk()
root.title("Smart Home System")

canvas = tk.Canvas(root, width=800, height = 600)
canvas.grid(rowspan=6, columnspan=3)



logo_frame = tk.Frame(root)

name = tk.Label(logo_frame, text="My Smart Home ", font=("Bauhaus 93", 45))

logo = Image.open(os.getcwd()+"/logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(logo_frame, image=logo)
logo_label.image = logo

#Positions
logo_frame.grid(row=1, column=0, columnspan=3)
name.pack(side=LEFT)
logo_label.pack(side=LEFT)






note=tk.Label(root, text="Kindly press 'q' to exit video surveillance",font=("Raleway", 14))

note.grid(row=5, column=0, columnspan=3 ,pady=(30, 0))


def open():
    db_path = os.getcwd()
    if len(db_path) == 0:
        messagebox.showinfo("Message", "You have to specify a path to the System!")
    else:
        os.startfile(os.getcwd()+"/"+"LOGs", 'open')
def open2():
    db_path = os.getcwd()
    if len(db_path) == 0:
        messagebox.showinfo("Message", "You have to specify a path to the System!")
    else:
        os.startfile(os.getcwd()+"/"+"HomeOwners", 'open')
    
def run():
    db_path = os.getcwd()
    if len(db_path) == 0:
        messagebox.showinfo("Message", "Unkown file locaction!")
    else :
        script.run(db_path)
        root.update()

#Run button

run_btn = tk.Button(root, text="Start", command=run, font="Raleway", bg="green", fg="white", width=10)

#Positions
run_btn.grid(row=3, column=1, columnspan=1, pady=(0, 0))

run_btn2 = tk.Button(root, text="Logs", command=open, font="Raleway", bg="green", fg="white", width=10)

#Positions
run_btn2.grid(row=3, column=0, columnspan=1, pady=(0, 0))


run_btn3 = tk.Button(root, text="Home Owners", command=open2, font="Raleway", bg="green", fg="white", width=11)

#Positions
run_btn3.grid(row=3, column=2, columnspan=1, pady=(0, 0))

#-----------------------------------------------------------------------------------------------------------------

root.mainloop()
