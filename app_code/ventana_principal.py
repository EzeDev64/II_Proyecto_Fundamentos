from tkinter import *
from PIL import Image, ImageTk
import os

class main_window:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(500,500)
        self.window.resizable(False,False)
        self.next_window = None

    def delete(self,window_goto):
        self.next_window = window_goto
        self.window.destroy()
        
    def create(self):
        #Background
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        bg = Image.open(f"{dir_img}\\bg_main.jpg")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_bg = Label(self.window,image=img_bg)
        lbl_bg.image = img_bg
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame_btn = Frame(bg="blue",width=100, height=100)
        btn_play = Button(frame_btn,text="Play",bg="blue",fg="white",command= lambda: self.delete("Play"))
        btn_play.pack(pady=5,fill=X)
        btn_stats = Button(frame_btn,text="Stadistics",bg="blue",fg="white",command= lambda: self.delete("Stats"))
        btn_stats.pack(pady=5,fill=X)
        btn_about = Button(frame_btn,text="About",bg="blue",fg="white",command= lambda: self.delete("About"))
        btn_about.pack(pady=5,fill=X)
        frame_btn.pack_propagate(False)
        frame_btn.pack(side=BOTTOM,pady=10)

        self.window.mainloop()
