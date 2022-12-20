import pyfirmata
import queue
import sys
sys.path.insert(0, 'C:/Users/ThePig0/Desktop/python/modules')
import multi_threading
import time

def move_servo(a):
    print(f"Moving servo by {a}")
    servo.write(a)
    print("Moved.")

class Deg:
    drop = 0
    no_drop = 20

def push():
    time.sleep(8)
    move_servo(Deg.drop)
    time.sleep(6)
    move_servo(Deg.no_drop)
    time.sleep(2)

STEPPER_PIN_1 = 7
STEPPER_PIN_2 = 6
STEPPER_PIN_3 = 5
STEPPER_PIN_4 = 4
step_number = 0
HIGH = 1
LOW = 0
turn = False

def digitalWrite(pin, sig):
    board.digital[pin].write(sig)

def OneStep(dir):
    global step_number
    step_number += 1
    if(step_number > 3):
        step_number = 0
    if(dir):
        if(step_number == 0):
            digitalWrite(STEPPER_PIN_1, HIGH)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, LOW)
            return
        if(step_number == 1):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, HIGH)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, LOW)
            return
        if(step_number == 2):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, HIGH)
            digitalWrite(STEPPER_PIN_4, LOW)
            return
        if(step_number == 3):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, HIGH)
            return
    else:
        if(step_number == 0):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, HIGH)
            return
        if(step_number == 1):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, HIGH)
            digitalWrite(STEPPER_PIN_4, LOW)
            return
        if(step_number == 2):
            digitalWrite(STEPPER_PIN_1, LOW)
            digitalWrite(STEPPER_PIN_2, HIGH)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, LOW)
            return
        if(step_number == 3):
            digitalWrite(STEPPER_PIN_1, HIGH)
            digitalWrite(STEPPER_PIN_2, LOW)
            digitalWrite(STEPPER_PIN_3, LOW)
            digitalWrite(STEPPER_PIN_4, LOW)
            return

print("Connecting board")
board = pyfirmata.Arduino('COM3')
print("Connecting servo")
servo = board.get_pin('d:3:s')
print("Resetting servo")
move_servo(Deg.no_drop)
time.sleep(2)
print("Testing turn")
push()
print("Done")

def func(num):
    print(num)
    global turn, img_counter
    if(num == 1):
        while True:
            f = open("C:/Users/ThePig0/Desktop/python/WTH/hi.txt", "r", encoding="utf8")
            if(f.read() == "T"):
                turn = True
            f.close()
            f = open("C:/Users/ThePig0/Desktop/python/WTH/hi.txt", "w", encoding="utf8")
            f.write("F")
            f.close()
            if(turn == True):
                push()
                turn = False
            time.sleep(0.5)
    elif(num == 2):
        while True:
            OneStep(False)
            for i in range(500):
                print(i, end="")
    else:
        pass
Q = queue.Queue()
Q.put(1)
Q.put(2)
multi_threading.start(func, Q, 3)