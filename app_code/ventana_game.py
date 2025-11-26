from tkinter import *
from PIL import Image, ImageTk
import time,os,p2p_connection,pygame,random
#from app_code.ventana_game_stats import stats_subwindow

class game_subwindow():
    def __init__(self,level,players,imgs):
        print(players)
        print(imgs)

        self.window = Tk()
        self.window.minsize(500,500)
        self.window.resizable(False,False)
        self.panelLst = []
        self.selected_players = players[0][:3]
        self.CPU_players = players[1][:3]
        self.teams_img = []
        self.teams_img.append(self.convert_to_teamsImg(self.selected_players))
        self.teams_img.append(self.convert_to_teamsImg(self.CPU_players))
        self.imgs = imgs
        self.CPU_level = level
        
        #Variables list
        self.time = 5 #Control the passing time
        self.total_plays = 10 #Total points or plays that has done during the game
        self.actual_team = 0 #Actual playing team
        self.team_played = False #Controls if the team play or not 
        #Points of each team are lst[0] fails, lst[1] anoted and lst[2] stopped balls
        self.T1_points = [0,0,0]
        self.T2_points = [0,0,0]

        #Sonidos
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        pygame.mixer.init()
        dir_csnd = os.path.join(BASE_DIR, "sound")
        dir_snd = os.path.join(dir_csnd, "silbato_start.ogg")        
        self.start_snd = pygame.mixer.Sound(dir_snd)
        dir_snd = os.path.join(dir_csnd, "silbato_shot.ogg")         
        self.shot_snd = pygame.mixer.Sound(dir_snd)
        dir_snd = os.path.join(dir_csnd, "sfail.ogg") 
        self.fail_snd = pygame.mixer.Sound(dir_snd)
        dir_snd = os.path.join(dir_csnd, "goal.ogg")         
        self.goal_snd = pygame.mixer.Sound(dir_snd)


    def create(self):
        #Background
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        bg = Image.open(f"{dir_img}\\bg_common.jpg")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_bg = Label(self.window,image=img_bg)
        lbl_bg.image = img_bg
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        #Creation of the diferent panels
        color = ["black","blue","black"]
        for i in range(0,3):
            panel = Frame(bg=color[i],width=500)
            panel.pack(fill=X)
            self.panelLst.append(panel)

        #Principal view
        lbl_teams = Label(self.panelLst[0],text="Eq1 VS Eq2",bg="black",fg="white")
        self.lbl_time = Label(self.panelLst[0],text="05:00",bg="black",fg="white")
        self.lbl_goalsT1 = Label(self.panelLst[0],text="Goles:0 Fallos:0",bg="black",fg="white")
        self.lbl_goalsT2 = Label(self.panelLst[0],text="Goles:0 Fallos:0",bg="black",fg="white")
        self.panelLst[0].pack_propagate(False)

        lbl_teams.grid(column=0,row=0,padx=25)
        self.lbl_time.grid(column=1,row=0,padx=25)
        self.lbl_goalsT1.grid(column=2,row=0,padx=25)
        self.lbl_goalsT2.grid(column=3,row=0,padx=25)

        #Provitional kick action
        self.window.bind("<Key-a>",lambda event: self.make_goal(True, event))

        #Teams panels
        self.panel_player = Frame(self.panelLst[1],bg="black",width=500/2,height=400)
        bg = Image.open(f"{dir_img}\\{self.teams_img[0]}")
        bg = bg.resize((200, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T1_escudo =  Label(self.panel_player,bg="black",image=img_bg)
        T1_escudo.image=img_bg
        T1_escudo.pack()
        T1_players_fm = Frame(self.panel_player,bg="black",width=250,height=200)
        
        bg = Image.open(f"{dir_img}\\{self.imgs[0]}.png")
        bg = bg.resize((125, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T1_lbl = Label(T1_players_fm,bg="black",image=img_bg)#,text=self.selected_players[1])
        T1_lbl.image=img_bg
        bg = Image.open(f"{dir_img}\\{self.imgs[1]}.png")
        bg = bg.resize((125, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T1_lbl2 = Label(T1_players_fm,bg="black",image=img_bg)
        T1_lbl2.image=img_bg
        T1_lbl.grid(column=0,row=0)
        T1_lbl2.grid(column=1,row=0)
        T1_players_fm.pack()

        self.panel_goalkeeper = Frame(self.panelLst[1],bg="black",width=500/2,height=400)
        bg = Image.open(f"{dir_img}\\{self.teams_img[1]}")
        bg = bg.resize((200, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T2_escudo =  Label(self.panel_goalkeeper,bg="black",image=img_bg)
        T2_escudo.image=img_bg
        T2_escudo.pack()
        T2_players_fm = Frame(self.panel_goalkeeper,bg="black")
        bg = Image.open(f"{dir_img}\\{self.imgs[2]}.png")
        bg = bg.resize((125, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T2_lbl = Label(T2_players_fm,image=img_bg,bg="black")#,text=self.CPU_players)
        T2_lbl.image = img_bg
        T2_lbl.grid(column=0,row=0)
        bg = Image.open(f"{dir_img}\\{self.imgs[3]}.png")
        bg = bg.resize((125, 200), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        T2_lbl2 = Label(T2_players_fm,image=img_bg,bg="black")#,text=self.CPU_players)
        T2_lbl2.image  = img_bg
        T2_lbl2.grid(column=1,row=0)       
        T2_players_fm.pack()

        self.panel_player.pack(side=LEFT)
        self.panel_player.pack_propagate(False)
        self.panel_goalkeeper.pack(side=RIGHT)
        self.panel_goalkeeper.pack_propagate(False)


        #p2p_connection.start_server()
        #Game time control
        p2p_connection.m_client = f"changeGAME,{self.CPU_level}"
        time.sleep(0.5) 
        #p2p_connection.m_client = "LOC"      
        p2p_connection.value_changed = self.shoot
        p2p_connection.button_pressed = self.gol_tapado        


        self.cronometro = self.window.after(1000,self.arbitro)

        self.window.mainloop()

    def delete(self):
        self.window.destroy()

    def arbitro(self):
        self.time -= 1
        self.lbl_time.config(text="0"+str(self.time)+":00")
        if self.time == 0:
            self.time = 4
            self.start_snd.play()   
            if self.actual_team == 0:
                p2p_connection.m_client = "LOC"
                self.panel_player.config(bg="red")
                self.panel_goalkeeper.config(bg="black")
            else:
                p2p_connection.m_client = "VIS"
                self.panel_player.config(bg="black")
                self.panel_goalkeeper.config(bg="red")

            self.cronometro = self.window.after(1000,self.time_control) 
            return

        self.cronometro = self.window.after(1000,self.arbitro)


    def time_control(self):
        self.time -= 1
        self.lbl_time.config(text="0"+str(self.time)+":00")

        #Checking the time and total plays
        if self.time == 0: #When time reach zero only
            self.total_plays -= 1
            self.time = 5
            #Changing to oponnent if the actual player is the user
            if self.actual_team == 0:
                self.T1_points[0] += 1
                self.actual_team = 1
                self.fail_snd.play()  
                #p2p_connection.m_client = "VIS"
                self.panel_player.config(bg="black")
                self.panel_goalkeeper.config(bg="black")
                self.lbl_goalsT1.configure(text="Goles:"+str(self.T1_points[1])+" Fallos:"+str(self.T1_points[0]))
            else:
                #Changing to user if actual player is the CPU
                iran = random.randint(0,1) 
                if iran == 0:
                    self.T2_points[0] += 1
                    self.fail_snd.play()                     
                else:
                    self.T2_points[1] += 1
                    self.goal_snd.play() 
                self.actual_team = 0         
                #p2p_connection.m_client = "LOC"       
                self.panel_player.config(bg="black")
                self.panel_goalkeeper.config(bg="black")
                self.lbl_goalsT2.configure(text="Goles:"+str(self.T2_points[1])+" Fallos:"+str(self.T2_points[0]))
            
            self.cronometro = self.window.after(1000,self.arbitro)
            return
        if self.total_plays == 0: #In case all the plays were used
            p2p_connection.m_client = "NOMORE"            
            self.delete()
            return
        
        self.cronometro = self.window.after(1000,self.time_control)

    #Only for user used to calc the points
    def make_goal(self,goal_state,event):
        if self.actual_team == 0: #Check if the user is the actual team playing
            #Cancel the actual timer
            self.window.after_cancel(self.cronometro)  

            if goal_state:
                print("Goal anoted")    
                self.goal_snd.play()
                #Modify the total points
                self.T1_points[1] += 1

                #The circuit binary logic
                val = self.T1_points[1]
                if val< 4:
                    val += 8
                    
                #Convertir a binario
                val = bin(val)
                val= val[2:]
                #Reducirlo a 3 terminos
                val = val[len(val)-3:]
                print(val)
                p2p_connection.m_client = "CIRCUIT,"+str(val)
            else:
                self.T1_points[0] += 1
                self.fail_snd.play()   
                print("Goal fail")

            self.time = 5
            self.actual_team = 1
            #p2p_connection.m_client = "VIS"
            self.total_plays -= 1                
            #Change the teams and time label text
            self.lbl_goalsT1.configure(text="Goles:"+str(self.T1_points[1])+" Fallos:"+str(self.T1_points[0]))
            self.panel_player.config(bg="black")
            self.panel_goalkeeper.config(bg="black")
            #self.lbl_time.config(text="0"+str(self.time)+":00")
            #Re-activate the timer            
            self.cronometro = self.window.after(1000,self.arbitro)

    #Determines if the shoot was goal or not
    def shoot(self):
        time.sleep(0.8)
        self.make_goal(True,False)

    def gol_tapado(self):
        self.T1_points[2] += 1
        p2p_connection.m_client = "NOMORE"
        self.make_goal(False,False)


    def convert_to_teamsImg(self,lst):
        if lst[0] == "Real Madrid":
            return "RM_escudo.png"
        elif lst[0] == "Bayer Munich":
            return "BM_escudo.png"
        else:
            return "Chelsea_escudo.png"

#window = game_subwindow(1,[['Chelsea', 'Fernandez', 'Cech', 0, 0, 0], ['Bayer Munich', 'Muller', 'Ulreich', 0, 0, 0]],['CH_fernandez', 'CH_cech', 'BM_muller', 'BM_ulreich']) 
#window.create()