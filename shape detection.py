import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)  # Mở kết nối với camera

    while True:
        ret, frame = cap.read()  # Đọc hình ảnh từ camera

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        edges = cv2.Canny(blurred_frame, 50, 150)

        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
            num_sides = len(approx)
            
            if num_sides == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.9 <= aspect_ratio <= 1.1:
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                    cv2.putText(frame, 'Hinh chu nhat', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif num_sides == 3:
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                cv2.putText(frame, 'Hinh tam giac', tuple(approx[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                circles = cv2.HoughCircles(
                    blurred_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50
                )
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for circle in circles[0, :]:
                        center = (circle[0], circle[1])
                        radius = circle[2]
                        cv2.circle(frame, center, radius, (0, 255, 0), 2)
                        cv2.circle(frame, center, 2, (0, 255, 255), 3)
                        cv2.putText(frame, 'Hinh tron', (circle[0] - radius, circle[1] + radius + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Shape Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Giải phóng camera
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()