import socket, threading,time, sys

#Creating the Host and connection port
HOST = "0.0.0.0"  #Listening and writing
PORT = 8081       #The port where we received client data
SERVER_IP = "192.168.77.140" #'192.168.100.88'
PORT_CLIENT = 8080

#"Potenciometro" value
global potec_value,button_value,conection,m_client
conection = True
potec_value = 0
button_value = 0
m_client = "a"

# Starting the server
def start_server():
    #Trying to connect in the destinated host
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(9)
    print(f"Servidor escuchando en puerto {PORT}")
    threading.Thread(target=accept_connections, args=(server,), daemon=True).start()

#Open the space to accept conections
def accept_connections(server):
    global conection
    server.settimeout(1.0) #The time limit the server will wait

    #If the conection is successfully the server will accept data from client
    while conection:
        try:
            client, addr = server.accept()
            print(f"Cliente conectado: {addr}")
            threading.Thread(target=handle_client, args=(client,), daemon=True).start() 

        except socket.timeout:
            continue
    server.close()

#The client manipulation
def handle_client(client):
    global potec_value, button_value,conection,m_client
    client.settimeout(1.0) #The time limit the client will wait

    while conection:
        try:
            #Received client's data
            data = client.recv(1024)
            if len(data) == 0:
                break
            message = data.decode()
            
            if "yes" in message:
                print("yes")
                value_changed()
            elif message == "no":
                print("no")
            elif message == "nada":
                print("Procesando info")
            elif message == "tapado":
                print("Gol tapado")
                button_pressed()
            elif message == "CLOSE":
                print("Message was close")
                break
            else:
                #Manipulation of the received information
                message = message.rsplit("/")
                button_value = int(message[0])
                potec_value = int(message[1][0])

                if button_value == 0:
                    print("Button Pressed")
                    button_pressed()
                    time.sleep(1)

                value_changed()
    
            client.sendall(m_client.encode())

        except socket.timeout:
            continue
        #except Exception as e:
        #    print("Error:", e)

    #Closing the conection if the variable conection is false
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    print("Se cerró la conección")
    #fnc_aux()

#Function when the "potenciometro" change value
def value_changed():
     return

#Function when the button state change
def button_pressed():
     return

#Auxiliar function when the app need to close
def fnc_aux():
    return

#Function that allows the server clossing
def close():
    global conection
    conection = False

#connect_client("loc")