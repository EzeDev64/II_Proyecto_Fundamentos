from machine import *
import network, socket, rp2, sys
import socket,time,random

#Configuration:
ssid = 'AndroidAP2361'
password = 'javier28272'
SERVER_IP = "192.168.77.140"
PORT = 8081
"""
Aditional data - for connecting other ip's
WR: Coffe PS: X3bazy20 IPL: "192.168.100.88" IPE: "192.168.100.50"
WR: 'AndroidAP2361' PS: 'javier28272' IPL: "192.168.247.140" IPE: ------
"""

led = Pin("LED",Pin.OUT)
#Potenciometro y botón
pot = ADC(26) #GPIO 26 (31)
button = Pin(5,Pin.IN,Pin.PULL_UP)
#Leds de los equipos
ledVisitante = Pin(27,Pin.OUT)
ledLocal = Pin(22,Pin.OUT)
#Para el circuito decremento 3 circular
led_aleat = Pin(16,Pin.OUT)
A = Pin(17,Pin.OUT)
B = Pin(18,Pin.OUT)
C = Pin(19,Pin.OUT)
#Registro corrimiento
#AB = Pin(18,Pin.OUT)
#CLK = Pin(19,Pin.OUT)
secuencia = [0,1,1,1,1,1]
nivel = 1 #para el portero
#Para las paletas:
pines = [12,7,11,8,10,9]
paletas = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in pines]
user_turn = True

#WIFI Connection
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    #Trying to connect to the WLAN
    while wlan.isconnected() == False:
        #Out the program with boot button
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        #Led
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    
    #If the connection was succesfully
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led.on()

# Senfing data to the server
def send_data():
    #control the actual sending data
    w_send = 0 #Where 0 is potec and button value and 1 is the paletes
    user_turn = True
    
    #Data mannagement
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    print("Conectado al servidor")

    #try:
    while True:
        if w_send == 0:
            adc_value = pot.read_u16() #Read "Potenciometro" value
            volt = (3.3/65535)*adc_value #Convert the value to equivalent in volts
            data = str(button.value()) + "/" + str(round(volt,0)) #Round the number for accesibility
            #also capture button value
        
        if w_send == 1 and user_turn:
            secuencia = EjecutarSecuencia()
            print(secuencia)
            for i, paleta in enumerate(paletas):
                if paleta.value() == 1:  # Circuito cerrado, tocó el cable
                    """
                    for c in range(6):
                        bit = secuencia[5-i]
                        AB(bit)
                        CLK(1)
                        CLK(0)
                    """    

                    #print(pines[i],secuencia[i])
                    if secuencia[i] == 1:
                        #print(secuencia, bit)
                        data = "tapado"
                        break
                    else:
                        #print(f"Paleta {i+1} tocó el cable")
                        data = f"yes{i+1}"
                        r_value = random.randint(0,1)                        
                        break
                else:
                    #print(f"Paleta {i+1} sin contacto")
                    data = "no"
                    
        if user_turn == False:
            data="nada"
                    
        print(data)
        client.send(data.encode())
                        
        response = client.recv(1024) # Recibe hasta 1024 bytes de datos
        print("Respuesta del servidor:", response.decode())
        response = response.decode()
        if "changeGAME" in response:
            dt = response.split(",")[1]
            print(dt)
            nivel = dt
            w_send = 1
            user_turn = False
        if response == "changeSELECT":
            w_send = 0
            user_turn = True
            print("Cambiando",w_send,user_turn)
        if response == "VIS":
            ledVisitante.on()
            ledLocal.off()
            user_turn = False
        if response == "LOC":
            ledVisitante.off()
            ledLocal.on()
            user_turn = True
        if "CIRCUIT" in response:
            led_aleat.value(r_value)
            print("Val_al", r_value)
            values = response.split(",")[1]
            A.value(int(values[0]))
            B.value(int(values[1]))
            C.value(int(values[2]))
            user_turn = False
            
        if response == "NOMORE":
            user_turn = False
                
        time.sleep(0.5)
            
    #except Exception as e:
        #print("Error:", e)
        #led.off()
    """
    finally:
        #When the connection is over
        print("Cerrando conexión")
        client.close()
    """
def EjecutarSecuencia():
    #Nivel = 1 AN1 Nivel = 2 AN2 Nivel = 3 AN3
    AN = 0
    portero_lst = [0,0,0,0,0,0]
    random.seed()

    if nivel == 1:
    #while True:
        AN = random.randint(0,2) * 2
        portero_lst[AN] = 1
        portero_lst[AN+1] = 1
        print(portero_lst)  
    if nivel == 2:
        AN = random.randint(0,2) * 3
        portero_lst[AN] = 1
        portero_lst[AN+1] = 1
        portero_lst[AN+2] = 1
        print(portero_lst) 
    if nivel == 3:
        AN = AN = random.randint(0,1)
        portero_lst[AN] = 1
        portero_lst[AN+2] = 1
        portero_lst[AN+4] = 1
        print(portero_lst)
    
    return portero_lst
    
#Main:
connect()
send_data()
#connect_server()