import cv2
import numpy as np

# Kích thước của hình ảnh trên màn hình
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Khoảng cách tối đa từ camera đến hình chữ nhật
MAX_DISTANCE_CM = 100

# Khởi tạo webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

def calculate_distance(width, height):
    # Tính diện tích hình chữ nhật
    area = width * height
    # Tính khoảng cách dựa trên diện tích của hình chữ nhật
    distance_cm = (20 * 153) / np.sqrt(area)
    if distance_cm > MAX_DISTANCE_CM:
        return -1  # Không thể tính toán khoảng cách
    return distance_cm

while True:
    # Đọc khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển đổi hình ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Thiết lập giới hạn cho màu đỏ
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Kết hợp hai mask để lấy hình ảnh chỉ có màu đỏ
    mask = cv2.bitwise_or(mask1, mask2)

    # Tìm các contour trong hình ảnh
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Tìm hình chữ nhật lớn nhất
    max_area = 0
    max_rect = None
    for contour in contours:
        rect = cv2.boundingRect(contour)
        area = rect[2] * rect[3]
        if area > max_area:
            max_area = area
            max_rect = rect

    if max_rect is not None:
        # Vẽ hình chữ nhật lên hình ảnhq
        x, y, w, h = max_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Tính toán khoảng cách từ camera đến hình chữ nhật
        distance_cm = calculate_distance(w,h)
        if distance_cm != -1:
          cv2.putText(frame, f"Distance: {distance_cm: .2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # Hiển thị khoảng cách trên màn hình

    # Hiển thị hình ảnh lên màn hình
    cv2.imshow("Frame", frame)

    # Thoát khỏi chương trình khi nhấn phím ESC
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()