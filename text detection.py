import cv2
import matplotlib.pyplot as plt
import time
import datetime
import pyfirmata
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
plt.rcParams['figure.figsize'] = [10, 10]

cam = cv2.VideoCapture(0)
today = datetime.date.today()
cv2.namedWindow("test")
img_counter = 0

def move_servo(a):
    print(f"Moving servo by {a}")
    servo.write(a)
    print("Moved.")

class Deg:
    drop = 0
    no_drop = 30

def push():
    move_servo(Deg.drop)
    time.sleep(2)
    move_servo(Deg.no_drop)
    time.sleep(2)

def scan():
    global img_counter
    while True:
        # start_time = time.time()
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        img_name = "opencv_frame_{}.png".format(img_counter)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        data = pytesseract.image_to_string(img_name)
        data = re.sub('[^1234567890]', '', data)
        print(len(data))
        if (len(data) == 8):
            date_obj = datetime.datetime.strptime(data, "%d%m%Y").date()
            print('Today:',today)
            print('Expiry Date', date_obj)
            if (today > date_obj):
                print('Expired')
                push()
        # t = 2.0 - time.time() + start_time
        # if(2.0 - time.time() + start_time)
        # time.sleep(2.0 - time.time() + start_time)
    cam.release()
    cv2.destroyAllWindows()

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

scan()