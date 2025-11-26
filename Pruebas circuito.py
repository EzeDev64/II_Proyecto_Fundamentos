from machine import *
import random

led_aleat = Pin(16,Pin.OUT)
A = Pin(17,Pin.OUT)
B = Pin(18,Pin.OUT)
C = Pin(19,Pin.OUT)
random.seed()

while True:
    r_value = random.randint(0,1)
    led_aleat.value(r_value)
    print(r_value)
    val = input("Ingrese un número(n para salir)")
    if val == "n":
        break
    
    val = int(val)
    if val< 4:
        val += 8
        
    #Convertir a binario
    val = bin(val)
    val= val[2:]
    #Reducirlo a 3 terminos
    val = val[len(val)-3:]
    
    print("Número en binario",val)
    A.value(int(val[0]))
    B.value(int(val[1]))
    C.value(int(val[2]))
    
    #print(A.value(),B.value(),C.value())


