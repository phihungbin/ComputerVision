import cv2

# Khởi tạo camera
cap = cv2.VideoCapture(1)

while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    # Xoay ngang ảnh
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Xoay ngang 90 độ theo chiều kim đồng hồ (do điện thoại quay dọc)
    # Chuyển ảnh sang đen trắng
    gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)
    # Đặt ngưỡng
    threshold_value = 100
    ret, thresholded_frame = cv2.threshold(gray_frame, threshold_value, 255, cv2.THRESH_BINARY_INV)
    # Tìm contours trong khung hình đã xử lý
    contours, _ = cv2.findContours(thresholded_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        s_thuc = area / 8.0  # 8 là giá trị tỉ lệ giữa S pixel và S thực của hình vuông làm chuẩn
        if 5000 < area < 50000:
            cv2.drawContours(rotated_frame, [contour], 0, (0, 255, 0), 2)
            text = "Dien tich: {:2}".format(s_thuc)
            cv2.putText(rotated_frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Frame", rotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()