from ventana_principal import main_window
from ventana_stats import stats_window
from ventana_about import about_window
from ventana_game_select import game_window

#Function for changing the window
def next_window(window):
    if window == "Play":
        window = game_window()
    elif window == "Stats":
        window = stats_window()
    elif window == "About":
        window = about_window()
    elif window == "Main":
        window = main_window()
    else:
        print("Saliendo de la app...")
        window = False

    return window

#Initializating the main window
window_goto = "Main"
while True:
    window = next_window(window_goto)
    if window == False:
        break
    window.create()
    window_goto = window.next_window
    

print("Ejecución finalizada")
