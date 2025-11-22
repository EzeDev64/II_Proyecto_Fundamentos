from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import p2p_connection, os, random, time
from ventana_game import game_subwindow
from ventana_game_stats import stats_subwindow

class game_window():
    def __init__(self):
        #Definition of the window
        self.window = Tk()
        self.window.minsize(500,500)
        self.window.resizable(False,False)
        self.next_window = "Main"
        self.selected_players = [[],[]] #Team-Player-Goalkeeper
        #Un diagrama que sea [[lista de team 1][lista de team 2]]
        #Dentro de cada team[Team-Player-Goalkeeper-goles-fails-atajadas] Esto para tabla de stats

        #List of differents components
        self.teams_lst = []
        self.player_lst = []
        self.goalkeeper_lst = []
        #The actual selecting id
        self.selecting = "T"
        self.selecting_info = "Nada"
        self.players_img = []

        #Definition of the diferent players for each team
        self.players_nameLst = [["Ronaldo","Bale","Benzema"],["Wagner","Robben","Muller"],["Palmer","Fernandez","Garnacho"]]
        self.players_imgLst =[["RM_ronaldo","RM_bale","RM_benzema"],["BM_wagner","BM_roben","BM_muller"],["CH_palmer","CH_fernandez","CH_garnacho"]]
        self.goalkeeper_nameLst = [["Navas","Casillas","Courtuis"],["Neuer","Peretz","Ulreich"],["Jorgensen","Cech","Sanchez"]]
        self.goalkeeper_imgLst = [["RM_navas","RM_casillas","RM_courtois"],["BM_neuer","BM_peretz","BM_ulreich"],["CH_jorgensen","CH_cech","CH_sanchez"]]

    #Create the window function
    def create(self):
        #Background
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")
        bg = Image.open(f"{dir_img}\\bg_game.jpg")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_bg = Label(self.window,image=img_bg)
        lbl_bg.image = img_bg
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.potenc_value = 0
        lbl_title = Label(text="Select your team",bg="black",fg="white")
        lbl_title.pack()
        self.panel_main = Frame(height=400,bg="black")

        #First part panel with cards
        self.teams_panels()
        
        self.window.bind("<Right>", lambda event: self.change_pot(1,event))
        self.window.bind("<Left>",lambda event: self.change_pot(-1,event))
        #self.window.bind("<Return>",lambda event: self.select_command(1,event))
        
        #Second Panel with player cards
        self.panel_two_test = Frame(self.panel_main,bg = "cyan",height=400,width=332)
        self.player_panels(self.player_lst,0)
        self.player_panels(self.goalkeeper_lst,1)

        #Panel with selected data and buttons
        data_frame = Frame(bg="black")
        self.lbl_data = Label(data_frame,text=self.selecting_info,bg="black",fg="white")
        self.lbl_data.grid(column=3,row=0)
        
        lbl_dificulty = Label(data_frame,text="CPU Level:",bg="black",fg="white")
        lbl_dificulty.grid(column=0,row=0)

        self.combo_CPU = ttk.Combobox(data_frame,state="readonly",background="black")
        self.combo_CPU['values'] =('1','2','3')
        self.combo_CPU.current(0)
        self.combo_CPU.grid(column=1,row=0)

        self.btn_select = Button(data_frame,text="Select",state=DISABLED,command=lambda:self.change_window(False),bg="black",fg="white")
        self.btn_select.grid(column=4,row=0)
        self.btn_select.bind("<Return>",self.change_window)

        self.btn_back = Button(data_frame,text="Back",command=lambda:self.back_select(False),bg="black",fg="white")
        self.btn_back.bind("<Return>",self.back_select)
        self.btn_back.grid(column=2,row=0)

        self.teams_lst.append(self.btn_back)
        self.player_lst.append(self.btn_back)
        self.goalkeeper_lst.append(self.btn_back)

        data_frame.pack()

        #Other components
        btn_return = Button(text="Return",command=self.delete,bg="black",fg="white")
        btn_return.pack()

        self.teams_lst[0].focus()
        try:
            p2p_connection.start_server()
        except:
            print("Server ya activo")

        p2p_connection.value_changed = lambda: self.change_pot(1,False)
        p2p_connection.button_pressed = lambda: self.select_team(self.teams_lst[p2p_connection.potec_value],False)
        p2p_connection.fnc_aux = lambda: self.change_window(False)
        p2p_connection.m_client = "changeSELECT"
        time.sleep(1)
        p2p_connection.m_client = "a"
        self.window.mainloop()

    #Destroy the window function
    def delete(self):
        self.window.destroy()

    def change_window(self,event):
        #Destroy the actual window
        self.delete()

        #Configure the player lst with stats and the CPU players lst 
        self.selected_players[0] = self.selecting_info.rsplit("-")
        for i in range(0,3):
          self.selected_players[0].append(0)  

        #Create the CPU lst with stats
        n = self.random_team_selection(["Real Madrid","Bayer Munich","Chelsea"])
        p = self.random_team_selection(self.players_nameLst[n])
        self.players_img.append(self.players_imgLst[n][p])
        g = self.random_team_selection(self.goalkeeper_nameLst[n])
        self.players_img.append(self.goalkeeper_imgLst[n][g])

        for i in range(0,3): self.selected_players[1].append(0)
        #The tournament is starting!!!
        time.sleep(2)
        #p2p_connection.m_client = "changeGAME"
        self.window = game_subwindow(1,self.selected_players,self.players_img)
        self.window.create()

        #Configuring the lsts for the stats window
        for i in range(0,3):
            self.selected_players[0][i+3] = int(self.window.T1_points[i])
            self.selected_players[1][i+3] = int(self.window.T2_points[i])
            
        self.window = stats_subwindow(self.selected_players,self.players_img)
        self.window.create()

    #If the user select a team
    def select_team(self, comp,event):
        #Changing the team panels to players panels
        self.panel_Bayer.grid_forget()
        self.panel_Real.grid_forget()
        self.panel_Chelsea.grid_forget()
        comp.grid(column=0,row=0)

        #Changing label with selected team info
        widgets_lst = comp.winfo_children()
        for w in widgets_lst:
            if isinstance(w,Label):
                self.selecting_info = w.cget("textvariable")
                self.lbl_data.config(text=self.selecting_info)

        #Activating the players panels
        self.panel_two_test.grid(column=1,row=0,columnspan=2)
        self.panel_two_test.pack_propagate(False)

        #Definiting the team for the list
        if self.selecting_info == "Real Madrid": team = 0
        if self.selecting_info == "Bayer Munich": team = 1
        if self.selecting_info == "Chelsea": team = 2

        #Changing the players names
        widgets_lst = self.panel_two_test.winfo_children()
        player_count = 0 #The count to put the list and the names list (Players or goalkeepers)
        player_lst = self.players_nameLst[team]
        img_lst = self.players_imgLst[team]

        #Searching the players labels
        for w in widgets_lst:
            lbl = w.winfo_children()
            for l in lbl:
                if isinstance(l,Label):
                    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
                    dir_img = os.path.join(BASE_DIR, "images")
                    img = Image.open(f"{dir_img}\\{img_lst[player_count]}.png")
                    img = img.resize((110,200), Image.Resampling.LANCZOS)
                    img_bg = ImageTk.PhotoImage(img)
                    l.config(text=player_lst[player_count],image=img_bg)
                    l.image = img_bg
                    player_count += 1
                    if player_count >= 3:
                        player_count = 0
                        player_lst = self.goalkeeper_nameLst[team]
                        img_lst = self.goalkeeper_imgLst[team]
               
        
        #Changing the actual selection and focus the players panels
        self.selecting = "P"
        #self.player_lst[self.potenc_value].focus()
        self.player_lst[p2p_connection.potec_value].focus()
        p2p_connection.button_pressed = lambda: self.select_player(self.player_lst[p2p_connection.potec_value],False)
    
    #If user select a player
    def select_player(self,comp,event):
        #The counter of players, changing the label with the actual selection
        comp.configure(bg="cyan")
        widgets_lst = comp.winfo_children()
        for w in widgets_lst:
            if isinstance(w,Label):
                if self.selecting_info == "Real Madrid": team = 0
                if self.selecting_info == "Bayer Munich": team = 1
                if self.selecting_info == "Chelsea": team = 2
                self.players_img.append(self.players_imgLst[team][p2p_connection.potec_value])#self.potenc_value]) #
                self.selecting_info += "-"+w.cget("text")
                self.lbl_data.config(text=self.selecting_info)


        #Changing the actual selection to the goalkeepers
        self.selecting = "G"
        #self.goalkeeper_lst[self.potenc_value].focus()
        self.goalkeeper_lst[p2p_connection.potec_value].focus()
        p2p_connection.button_pressed = lambda: self.select_goalkeeper(self.goalkeeper_lst[p2p_connection.potec_value],False)

    #If user select a goalkeeper
    def select_goalkeeper(self,comp,event):
        #If we select after selecting the goalkeeper
        if self.selecting == "N":
            return
        
        #Changing the label with the actual selection
        comp.configure(bg="cyan")
        widgets_lst = comp.winfo_children()
        for w in widgets_lst:
            if isinstance(w,Label):
                a = self.selecting_info.rsplit("-")
                if a[0] == "Real Madrid": team = 0
                if a[0] == "Bayer Munich": team = 1
                if a[0] == "Chelsea": team = 2
                self.players_img.append(self.goalkeeper_imgLst[team][p2p_connection.potec_value]) #self.potenc_value
                self.selecting_info += "-"+w.cget("text")
                self.lbl_data.config(text=self.selecting_info)

        #Changing the select button state to normal to pass to game
        self.btn_select.focus()
        p2p_connection.button_pressed = lambda: p2p_connection.close()

        self.selecting = "N"
        self.btn_select.config(state=NORMAL)

    #Changing potenciometro xd value function
    def change_pot(self,operation,event):
        #Changing the value localy only for testing purpuses
        """
        self.potenc_value += operation
        if self.potenc_value > 3:
            self.potenc_value = 3
        elif self.potenc_value < 0:
            self.potenc_value = 0
        """
        print("a",p2p_connection.potec_value)

        #Focus the component depending the selection
        if self.selecting == "T":
            #self.teams_lst[self.potenc_value].focus()
            self.teams_lst[p2p_connection.potec_value].focus()
        elif self.selecting == "P":
            #self.player_lst[self.potenc_value].focus()
            self.player_lst[p2p_connection.potec_value].focus()
        elif self.selecting == "G":
            #self.goalkeeper_lst[self.potenc_value].focus()
            self.goalkeeper_lst[p2p_connection.potec_value].focus()

    #Selecting the team, player and goalkeeper of the opponent
    def random_team_selection(self,lst):
        number = random.randint(0,2)
        self.selected_players[1].append(lst[number])
        return number

    #If back button was pressed. To returning the selection
    def back_select(self,event):
        #Changing the selected players panels to default
        colors = ["red","blue"]
        color_id = 0
        lst = self.panel_two_test.winfo_children()
        for w in lst:
            w.configure(bg=colors[color_id])
            color_id += 1
            if color_id > 1:
                color_id = 0

        #Deleting the panels
        lst = self.panel_main.winfo_children()
        for w in lst:
            w.grid_forget()

        #Re-creating the teams panels and the default selection configuration
        self.teams_panels()
        self.players_img = []
        self.teams_lst.append(self.btn_back)
        self.selecting = "T"
        
        self.teams_lst[p2p_connection.potec_value].focus()
        #self.teams_lst[self.potenc_value].focus()
        self.btn_select.config(state=DISABLED)

    #For teams panels creation
    def teams_panels(self):
        #Imgs
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir_img = os.path.join(BASE_DIR, "images")

        self.panel_Real = Frame(self.panel_main,bg="white",height=400,width=166,
                                highlightcolor="black",highlightthickness=5)
        bg = Image.open(f"{dir_img}\\RM_escudo.png")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_RealTitle = Label(self.panel_Real,image=img_bg,textvariable="Real Madrid")
        lbl_RealTitle.image = img_bg
        lbl_RealTitle.pack(padx=10, pady=10)

        self.panel_Bayer = Frame(self.panel_main,bg="red",height=400,width=166,
                                 highlightcolor="black",highlightthickness=5)
        bg = Image.open(f"{dir_img}\\BM_escudo.png")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_BayerTitle = Label(self.panel_Bayer,image=img_bg,textvariable="Bayer Munich")
        lbl_BayerTitle.image = img_bg
        lbl_BayerTitle.pack(padx=10, pady=10)

        self.panel_Chelsea = Frame(self.panel_main,bg="blue",height=400,width=166,
                                highlightcolor="black",highlightthickness=5)        
        bg = Image.open(f"{dir_img}\\Chelsea_escudo.png")
        bg = bg.resize((500, 500), Image.Resampling.LANCZOS)
        img_bg = ImageTk.PhotoImage(bg)
        lbl_Chelsea = Label(self.panel_Chelsea,text="Chelsea",image=img_bg,textvariable="Chelsea")
        lbl_Chelsea.image = img_bg
        lbl_Chelsea.pack(padx=10, pady=10)

        self.panel_Real.grid(column=0,row=0)
        self.panel_Real.pack_propagate(False)
        self.panel_Bayer.grid(column=1,row=0)
        self.panel_Bayer.pack_propagate(False)
        self.panel_Chelsea.grid(column=2,row=0)
        self.panel_Chelsea.pack_propagate(False)

        self.panel_main.pack(fill=X)

        self.panel_Real.bind("<Return>", lambda event: self.select_team(self.panel_Real,event))
        self.panel_Bayer.bind("<Return>", lambda event: self.select_team(self.panel_Bayer,event))
        self.panel_Chelsea.bind("<Return>", lambda event: self.select_team(self.panel_Chelsea,event))

        self.teams_lst = [self.panel_Real,self.panel_Bayer,self.panel_Chelsea]
        p2p_connection.button_pressed = lambda: self.select_team(self.teams_lst[p2p_connection.potec_value],False)
        return

    #For player panels creation
    def player_panels(self,lst,c_index):
        #Variable que no va a durar mucho
        colors = ["red","blue"]
        text = "Player"
        fun = self.select_player
        row_position = 0
        if lst is self.goalkeeper_lst:
            row_position = 1
            text = "Goalkeeper"
            fun = self.select_goalkeeper

        for i in range(0,3):
            #colors[c_index]
            player_panel =  Frame(self.panel_two_test,bg="black",width=110,height=200,
                                  highlightcolor="white",highlightthickness=5,highlightbackground="black")
            pl1 = Label(player_panel,text= text+str(i),bg="black")
            pl1.pack()
            player_panel.grid(column=i,row=row_position)
            player_panel.pack_propagate(False)
            lst.append(player_panel)
            c_index += 1
            if c_index > 1:
                c_index=0

        lst[0].bind("<Return>", lambda event: fun(lst[0],event))
        lst[1].bind("<Return>", lambda event: fun(lst[1],event))
        lst[2].bind("<Return>", lambda event: fun(lst[2],event))
        return


#window = game_window() window.create()