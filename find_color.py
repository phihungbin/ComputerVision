import cv2
import numpy as np
import Jetson.GPIO as GPIO
from RPi_GPIO_i2c_LCD import lcd
#################################
i2c_address = 0x27
lcdDisplay = lcd.HD44780(i2c_address)
#################################
led1 = 11
led2 = 13
led3 = 15
################################
l1 = 19
l2 = 21
l3 = 22
l4 = 24
################################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

GPIO.setup(l1, GPIO.OUT) #Động cơ dưới
GPIO.setup(l2, GPIO.OUT)
GPIO.setup(l3, GPIO.OUT) #Động cơ trên
GPIO.setup(l4, GPIO.OUT)
###############################
blue = np.array([[100, 100, 100], [130, 255, 255]])
red = np.array([[0, 100, 100], [20, 255, 255]])
yellow = np.array([[20, 100, 100], [30, 255, 255]])
###############################
cap = cv2.VideoCapture(0)
lcdDisplay.clear()
while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(hsv, blue[0], blue[1])
    red_mask = cv2.inRange(hsv, red[0], red[1])
    yellow_mask = cv2.inRange(hsv, yellow[0], yellow[1])

    mask = cv2.bitwise_or(blue_mask, red_mask)
    mask = cv2.bitwise_or(mask, yellow_mask)
    lcdDisplay.set("    HUNG|LINH|SON", 1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(i)
            color = None
            GPIO.output(led1, GPIO.LOW)
            GPIO.output(led2, GPIO.LOW)
            GPIO.output(led3, GPIO.LOW)
            GPIO.output(l1, GPIO.LOW)
            GPIO.output(l2, GPIO.LOW)
            GPIO.output(l3, GPIO.LOW)
            GPIO.output(l4, GPIO.LOW)

            if blue_mask[y + h // 2, x + w // 2] == 255:
                color = 'Blue'
                lcdDisplay.set("       Blue  ", 3)
                GPIO.output(led3, GPIO.HIGH)
                GPIO.output(l1, GPIO.HIGH) #DC Trên quay cùng chiều kimdh
                GPIO.output(l2, GPIO.LOW)
                GPIO.output(l3, GPIO.LOW) #DC dưới quay cùng chiều kimdh
                GPIO.output(l4, GPIO.HIGH)
            elif red_mask[y + h // 2, x + w // 2] == 255:
                color = 'Red'
                lcdDisplay.set("       Red   ", 3)
                GPIO.output(led1, GPIO.HIGH)
                GPIO.output(l1, GPIO.HIGH)  #DC trên quay cùng chiều kimdh
                GPIO.output(l2, GPIO.LOW)
                GPIO.output(l3, GPIO.LOW)   #DC dưới tắt
                GPIO.output(l4, GPIO.LOW)
            elif yellow_mask[y + h // 2, x + w // 2] == 255:
                color = 'Yellow'
                lcdDisplay.set("       Yellow", 3)
                GPIO.output(led2, GPIO.HIGH)
                GPIO.output(l1, GPIO.LOW)   #DC trên tắt
                GPIO.output(l2, GPIO.LOW)
                GPIO.output(l3, GPIO.HIGH)  #DC dưới quay ngược chiều kimdh
                GPIO.output(l4, GPIO.LOW)
                if color:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Color Detection', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()