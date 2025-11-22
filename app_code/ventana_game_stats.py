from tkinter import *
from PIL import Image, ImageTk
import os,json_read

class stats_subwindow():
    def __init__(self,players,imgs):
        self.window = Tk()
        self.window.minsize(600,500)
        self.window.resizable(False,False)
        self.selected_players = players[0]
        self.CPU_players = players[1]
        self.teams_img = []
        self.teams_img.append(self.convert_to_teamsImg(self.selected_players))
        self.teams_img.append(self.convert_to_teamsImg(self.CPU_players))
        self.imgs = imgs

    def create_panels(self,panel,unit,type=False): #Type es si es para equipo 0 o 1
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        color = ["red","blue","red"]
        lst = []
        team_img_index = 0
        player_img_index= 0

        if type:
            lst = self.selected_players
            team_img_index = 0
            player_img_index= 0
        else:
            lst = self.CPU_players
            team_img_index = 1
            player_img_index= 2

        frame1 = Frame(panel,bg=color[unit],height=200,width=300)
        bg = Image.open(f"{dir_img}\\{self.teams_img[team_img_index]}")
        bg = bg.resize((250, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_team = Label(frame1,image=img_bg,width=300,height=200,bg="black")#text=lst[0])
        lbl_team.image = img_bg
        lbl_team.pack()

        frame2 = Frame(panel,bg="black",height=300,width=200)
        bg = Image.open(f"{dir_img}\\{self.imgs[player_img_index]}.png")
        bg = bg.resize((150, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_player = Label(frame2,image=img_bg,bg="black")
        lbl_player.image = img_bg
        bg = Image.open(f"{dir_img}\\{self.imgs[player_img_index+1]}.png")
        bg = bg.resize((150, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_goalkeeper = Label(frame2,image=img_bg,bg="black")
        lbl_goalkeeper.image = img_bg

        lbl_player.grid(column=0,row=0)
        lbl_goalkeeper.grid(column=1,row=0)
        
        txt = ""
        txt += "Puntos anotados:"+str(lst[4])
        txt += " Puntos fallidos:"+str(lst[3])
        txt += " Puntos tapados:"+str(lst[5])
        lbl_players = Label(panel,text=txt)

        frame1.pack()
        frame1.pack_propagate(False)
        frame2.pack()
        frame2.pack_propagate(False)
        lbl_players.pack()
        return

    def create(self):
        #Background
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        bg = Image.open(f"{dir_img}\\bg_common.jpg")
        bg = bg.resize((620, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_bg = Label(self.window,image=img_bg)
        lbl_bg.image = img_bg
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame_main = Frame(height=500,bg="black")
        frame_fp = Frame(frame_main,bg="black",height=500,width=300)
        self.create_panels(frame_fp,0,True)
        frame_sp = Frame(frame_main,bg="black",height=500,width=300)
        self.create_panels(frame_sp,1)

        frame_fp.grid(column=0,row=0)
        frame_sp.grid(column=1,row=0)

        frame_main.pack(fill=X)

        btn_return = Button(text="Return",command=self.delete,bg="black",fg="white")
        btn_return.pack()

        #Aquí hacer llamado de fnc data
        json_read.change_scores(self.selected_players,self.imgs)
        self.window.mainloop()

    def delete(self):
        self.window.destroy()

    def convert_to_teamsImg(self,lst):
        if lst[0] == "Real Madrid":
            return "RM_escudo.png"
        elif lst[0] == "Bayer Muninch":
            return "BM_escudo.png"
        else:
            return "Chelsea_escudo.png"

#window = stats_subwindow([['Real Madrid', 'Ronaldo', 'Navas', 0, 3, 0], ['Bayer Muninch', 'Muller', 'Ulreich', 0, 0, 0]],
#                         ['RM_ronaldo', 'RM_navas', 'RM_benzema', 'RM_casillas']) 
#window.create()