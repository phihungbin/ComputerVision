import cv2
import numpy as np
import time
red = np.array([[6, 100, 100], [9, 255, 255]])
cap = cv2.VideoCapture(0)

def distance(width, height):
    area = width * height
    distance_cm = 5200 / np.sqrt(area)
    if ((distance_cm > 100) or (distance_cm < 12)):
        return 0
    return distance_cm

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, red[0], red[1])

    #Tìm đường bao
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(i)
            color = None
            if red_mask[y + h // 2, x + w // 2] == 255:
                color = 'Red'
                distance_cm = distance(w, h)
                if distance_cm != 0:
                    area_cm2 = 13.5 * 46.5 / distance_cm
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, f"Distance: {distance_cm:.2f} cm", (10, 30), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"Dien tich: {area_cm2:.2f} cm", (10, 60), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
        
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
