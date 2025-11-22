from tkinter import *
from PIL import Image, ImageTk
import os

class about_window():
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False,False)
        self.window.minsize(500,500)
        self.next_window = "Main"

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
        lbl_title = Label(text="About")
        lbl_title.pack()

        frame_main = Frame(bg="black",height=400)

        frame_text = Frame(frame_main,bg="black",height=200,width=500)
        lbl_CE = Label(frame_text,text="Ingenierìa en computadores",bg="black",fg="white")
        lbl_course = Label(frame_text,text="Fundamentos de sistemas computacionales",bg="black",fg="white")
        lbl_prof =Label(frame_text,text="Milton Villegas",bg="black",fg="white")
        lbl_agrad = Label(frame_text,text="Agradecimientos a Asly Barahona",bg="black",fg="white")
        lbl_year =Label(frame_text,text="2025",bg="black",fg="white")
        lbl_extra = Label(frame_text,text="Producido en Costa Rica, Cartago, TEC. Version 1.0",bg="black",fg="white")
        lbl_CE.pack()
        lbl_course.pack()
        lbl_prof.pack()
        lbl_agrad.pack()
        lbl_year.pack()
        lbl_extra.pack()
        frame_text.grid(column=0,row=0,columnspan=2)

        frame_dataEze = Frame(frame_main,bg="black",width=250,height=400)
        frame_labels_info1 = Frame(frame_dataEze,bg="black",width=250,height=100)
        lbl_name_Eze = Label(frame_labels_info1,text="Ezequiel Bonilla Vega",bg="black",fg="white")
        lbl_carnet_Eze = Label(frame_labels_info1,text="2025098474",bg="black",fg="white")
        bg = Image.open(f"{dir_img}\\eze_foto.jfif")
        bg = bg.resize((250, 300), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_foto_Eze = Label (frame_dataEze, text="Foto",bg="black",fg="white",image=img_bg)
        lbl_foto_Eze.image = img_bg

        frame_dataEze.grid(column=0,row=1)
        frame_dataEze.pack_propagate(False)
        frame_labels_info1.pack()
        frame_labels_info1.pack_propagate(False)
        lbl_foto_Eze.pack()        
        lbl_name_Eze.pack()
        lbl_carnet_Eze.pack()


        frame_dataJavier = Frame(frame_main,bg="black",width=250,height=400)
        frame_labels_info2 = Frame(frame_dataJavier,bg="black",width=250,height=100)
        lbl_name_Javier = Label(frame_labels_info2,text="Javier Solano Redondo",bg="black",fg="white")
        lbl_carnet_Javier = Label(frame_labels_info2,text="2025085024",bg="black",fg="white")
        bg = Image.open(f"{dir_img}\\javier_foto.jpg")
        bg = bg.resize((250, 300), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_foto_Javier = Label (frame_dataJavier, text="Foto",bg="black",fg="white",image= img_bg)
        lbl_foto_Javier.image = img_bg

        frame_dataJavier.grid(column=1,row=1)
        frame_dataJavier.pack_propagate(False)
        frame_labels_info2.pack()
        frame_labels_info2.pack_propagate(False)
        lbl_foto_Javier.pack()
        lbl_name_Javier.pack()
        lbl_carnet_Javier.pack()

        

        frame_main.pack_propagate(False)
        frame_main.pack(fill=X)

        btn_return= Button(text="Regresar",command=self.delete)
        btn_return.pack()

        self.window.mainloop()

    def delete(self):
        self.window.destroy()