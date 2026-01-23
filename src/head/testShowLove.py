import time
from headClass import Head

head = Head()
v = 60
tau = 3
print("Testing HEAD class")
time.sleep(tau)

#for i in range(10):
#    head.gesture_no(20, 0.5,3)
#    head.gesture_yes(0.5)
#    time.sleep(tau)

#try:
#    while True:
#        word = input("Introduce la palabra (WORD): ")  # Palabra que define la orden
#        value = input("Introduce el valor (VALUE): ")  # Valor que acompaña la orden
##        head.serial_send(word, value)
#        if word == "BLINK":
#            head.blink(value)
#        time.sleep(1)  # Espera de 1 segundo entre órdenes

head.gesture_neutral(0)
time.sleep(2*tau)
head.gesture_laugh(3)
time.sleep(tau)
head.gesture_neutral(0)
time.sleep(tau)
head.gesture_laugh(5)
time.sleep(tau)
head.gesture_neutral(0)
time.sleep(tau)
head.gesture_laugh(10)
time.sleep(tau)
head.gesture_neutral(0)
time.sleep(tau)

#head.gesture_yes(0.04, 3)
#time.sleep(tau)
#head.gesture_neutral(0)
#time.sleep(tau/2)
#head.gesture_no(16, 0.6, 3)
#time.sleep(tau)
#head.gesture_neutral(0)
#time.sleep(tau)
#head.gesture_happy(7)
#time.sleep(tau)
#head.gesture_neutral(0)
#time.sleep(tau)
#head.gesture_sad(7)
#time.sleep(tau)
#head.gesture_neutral(0)
#time.sleep(tau)
#head.gesture_angry(7)
#time.sleep(tau)
#head.gesture_neutral(0)
#time.sleep(tau)

head.close()
