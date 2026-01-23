import time
from headClass import Head

head = Head()
v = 60
tau = 3
print("Testing HEAD class")
time.sleep(tau)

def test_happy():
    head.gesture_happy(1)
    time.sleep(tau)
    head.gesture_neutral(0)
    time.sleep(tau)
    head.gesture_happy(5)
    time.sleep(tau)
    head.gesture_neutral(0)
    time.sleep(tau)
    head.gesture_happy(10)
    time.sleep(tau)
    head.gesture_neutral(0)
    time.sleep(tau)

def test_sad():
    head.gesture_sad(7)
    time.sleep(tau)
    head.gesture_neutral(0)
    time.sleep(tau)
    head.gesture_angry(7)
    time.sleep(tau)
    head.gesture_neutral(0)
    time.sleep(tau)

def test_queue():
    print("happy")
    head.act("HAPPY", 5)
    print("yes")
    head.act("YES", 5)
    print("surprise")
    head.act("SURPRISED", 5)
    print("blink")
    head.act("BLINK", 5)
    print("yes")
    head.act("YES", 10)
    print("no")
    head.act("NO", 10)
    print("neutral")
    head.act("NEUTRAL", 7)
    for i in range(len(head.gesture_queue)):
        input("Pulse una tecla para continuar...")
        head.tick()

test_queue()
input("Pulse una tecla para terminar...")
print("close")
head.close()
