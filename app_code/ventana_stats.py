from tkinter import *
from PIL import Image, ImageTk
import os,json_read

class stats_window:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(500,500)
        self.window.resizable(False,False)
        self.next_window = "Main"

    def create_panels(self,panel,unit,dict):
        color = ["red","blue","red"]
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")

        if dict[0]  == "Real Madrid":  png = "RM_escudo.png"
        if dict[0]  == "Bayer Munich":  png = "BM_escudo.png"
        if dict[0]  == "Chelsea":  png = "Chelsea_escudo.png"
        
        frame1 = Frame(panel,bg="black",height=200,width=166)
        bg = Image.open(f"{dir_img}\\{png}")
        bg = bg.resize((166,200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_team = Label(frame1,text="Equipo escudo", bg="black",image=img_bg)
        lbl_team.image = img_bg
        lbl_team.pack()
  
        frame2 = Frame(panel,bg="black",height=200,width=166)
        bg = Image.open(f"{dir_img}\\{dict[2]}.png")
        bg = bg.resize((83,200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_player = Label(frame2,bg="black",image=img_bg)#text=(dict[5],dict[6],dict[7]))
        lbl_player.image = img_bg
        lbl_player.grid(column=0,row=0)
        
        bg = Image.open(f"{dir_img}\\{dict[4]}.png")
        bg = bg.resize((83,200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_goalkeeper = Label(frame2,bg="black",image=img_bg)
        lbl_goalkeeper.image = img_bg
        lbl_goalkeeper.grid(column=1,row=0)

        #Here we put the different points that the user gain
        frame3 = Frame(panel,bg="black")
        points = f"Puntos Anotados: {dict[6]} \n Puntos Fallidos: {dict[5]} \n Puntos atajados: {dict[7]}"
        lbl_points = Label(frame3,bg="black",fg="white",text=points)
        lbl_points.pack()

        frame1.pack()
        frame1.pack_propagate(False)
        frame2.pack()
        frame2.pack_propagate(False)
        frame3.pack(fill=X)
        return

    def create(self):
        #Background
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        bg = Image.open(f"{dir_img}\\bg_common.jpg")
        bg = bg.resize((520, 520), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_bg = Label(self.window,image=img_bg)
        lbl_bg.image = img_bg
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        json_data = json_read.read_file()
        lbl_title = Label(text="Estadísticas",bg="black",fg="white")
        lbl_title.pack()

        frame_main = Frame(height=400,bg="black")
        frame_fp = Frame(frame_main,bg="black",height=400,width=166)
        self.create_panels(frame_fp,0,json_data["A"])
        frame_sp = Frame(frame_main,bg="black",height=400,width=166)
        self.create_panels(frame_sp,1,json_data["B"])
        frame_tp = Frame(frame_main,bg="black",height=400,width=166)
        self.create_panels(frame_tp,0,json_data["C"])

        frame_fp.grid(column=0,row=0)
        frame_sp.grid(column=1,row=0)
        frame_tp.grid(column=2,row=0)

        frame_main.pack(fill=X)


        btn_return = Button(text="Return",bg="black",fg="white",command=self.delete)
        btn_return.pack(pady=5)
        self.window.mainloop()

    def delete(self):
        self.window.destroy()