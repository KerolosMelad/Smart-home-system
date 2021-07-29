import os 
from os import mkdir , path
from tkinter import messagebox ,scrolledtext ,filedialog
import time
import tkinter as tk
from tkinter.constants import END, LEFT, TOP
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory, askopenfilename
import script
import threading

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
        
def runsystem():
        import cloudstorage 
        db_path = os.getcwd()
        storage,db  = cloudstorage.start()
        import CreateDB 
        script.run(os.getcwd())
        db.child("system").push({"state" : "close"})
        if(db.child("newUser").get().val()):
            newUser =db.child("newUser").get().val()
            db.child("newUser").remove()
            counter = db.child("counter").get().val()
            db.child("counter").remove()
            homeOwnersPath=db_path+"/"+"HomeOwners"
            newUserPath=homeOwnersPath+"/"+newUser
            if(path.exists(newUserPath)== False):
                os.mkdir(newUserPath)
            if(path.exists(homeOwnersPath+"/"+"representations.pkl")):
                os.remove(homeOwnersPath+"/"+"representations.pkl")
            i= 0
            while(i<int(counter)):
                #print("img downlding")
                storage.child(str(i)+".jpg").download(newUserPath+"/"+newUser+str(i)+".jpg")
                #print(newUserPath+"/"+str(i)+".jpg"+"DDDD")
                i=i+1

            employees =CreateDB.Create_DB(employees,db_path,interpreter , input_details ,output_details)
            DBHomeowners() 
    
def gui ():



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



    def run():
        runsystem()
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



    #--------------------------------

    root.mainloop()
    
    

import cloudstorage 
storage,db  = cloudstorage.start()

def mobAPP():
    DBCHECKER=-1
    while(True):
        if( time.time() - DBCHECKER>=1):
            system=""
            if(db.child("appsystem").get().val()):
                system =db.child("appsystem").get().val()
                #print(system)
                db.child("appsystem").remove()
            #print(firedb.systemOnFlag )
            if(system == 'systemOn' ):
                runsystem()
                db.child("notification").remove()
                
                

thread1 = threading.Thread(target= gui, args = ())
thread2 = threading.Thread(target= mobAPP, args = ())
thread1.start()
thread2.start()
