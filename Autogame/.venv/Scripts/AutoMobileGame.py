import os
import sys
from PyQt5.QtCore import QRect, Qt
from PIL import Image
import pytesseract
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QApplication, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen
import cv2


# def recognize_character(image_path):
#     """Nhận diện ký tự từ ảnh đã crop."""
#     try:
#         # Đọc ảnh bằng OpenCV
#         image = cv2.imread(image_path)
#
#         # Chuyển ảnh sang dạng grayscale (đơn sắc)
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#         # Áp dụng threshold để làm rõ ký tự
#         _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#
#         # Lưu ảnh đã xử lý (nếu cần kiểm tra)
#         cv2.imwrite("processed_image.png", thresh_image)
#
#         # Nhận diện ký tự bằng pytesseract
#         text = pytesseract.image_to_string(thresh_image, lang='eng', config='--psm 10')
#         # '--psm 10': Cấu hình Tesseract cho nhận diện ký tự đơn lẻ
#
#         return text.strip()
#     except Exception as e:
#         return f"Lỗi: {str(e)}"


class PhoneController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coordinates = []  # Lưu chữ cái và tọa độ
        self.start_pos = None  # Điểm bắt đầu
        self.end_pos = None  # Điểm kết thúc
        self.is_selecting = False  # Trạng thái khi đang chọn vùng
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Điều khiển điện thoại")
        self.setGeometry(100, 100, 480, 800)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        # Khung nhập chữ cái
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Nhập thứ tự chữ cái (VD: A B C)")
        layout.addWidget(self.input_line)

        # Nút thực hiện vuốt
        self.swipe_button = QPushButton("Thực hiện vuốt", self)
        self.swipe_button.clicked.connect(self.execute_swipe)
        layout.addWidget(self.swipe_button)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent
        self.label.mouseMoveEvent = self.mouseMoveEvent

        self.update_screen_image()

    def update_screen_image(self):
        # Chụp màn hình qua ADB
        os.system("adb exec-out screencap -p > screen.png")
        pixmap = QPixmap("screen.png")
        scaled_pixmap = pixmap.scaled(1000, 860, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.resize(scaled_pixmap.width(), scaled_pixmap.height())

    def mousePressEvent(self, event):
        """Bắt đầu chọn vùng trên ảnh"""
        print("start press")
        self.start_pos = event.pos()
        self.is_selecting = True

    def mouseMoveEvent(self, event):
        """Di chuyển chuột và vẽ hình chữ nhật trong khi chọn"""
        if self.is_selecting and self.start_pos:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Kết thúc chọn vùng và xử lý OCR"""
        print("end press")
        self.end_pos = event.pos()
        self.is_selecting = False
        self.recognize_text(QRect(self.start_pos, self.end_pos))
        self.start_pos = None
        self.end_pos = None
        self.update()  # Cập nhật lại giao diện để ẩn hình chữ nhật

    def paintEvent(self, event):
        """Vẽ hình chữ nhật khi di chuyển chuột"""
        if self.is_selecting and self.start_pos and self.end_pos:
            painter = QPainter(self.label.pixmap())
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.setBrush(Qt.transparent)  # Làm cho hình chữ nhật trong suốt
            painter.drawRect(rect)
            painter.end()
            self.label.update()

    def recognize_text(self, rect):
        try:
            print("Handle recognize text")
            pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path if Tesseract is installed elsewhere

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            print(f"Cropping coordinates: x={x}, y={y}, w={w}, h={h}")

            # Open the image and crop it
            image = Image.open("screen.png")
            cropped = image.crop((x, y, x + w, y + h))
            cropped.save("cropped.png")
            print("Cropped image saved as 'cropped.png'")

            # Perform OCR
            custom_config = r'--psm 10'  # Single character mode
            # text = self.recognize_character()recognize_character(cropped);
            # print(f"Recognized text: {text}")
            recognized_text = self.recognize_character("cropped.png")
            print(f"Recognized text: {recognized_text}")

            # Save the text and coordinates
            self.coordinates.append((recognized_text, (x, y, x + w, y + h)))
            print(f"Saved coordinates and text: {self.coordinates}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def recognize_character(self, image_path):
        """
        Nhận diện ký tự từ file ảnh.
        """
        try:
            # Đọc ảnh bằng OpenCV
            image = cv2.imread(image_path)

            # Kiểm tra ảnh có tồn tại hay không
            if image is None:
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Chuyển ảnh sang dạng grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Áp dụng threshold để làm rõ ký tự
            _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Lưu ảnh đã xử lý (tuỳ chọn kiểm tra)
            cv2.imwrite("processed_image.png", thresh_image)

            # Nhận diện ký tự bằng pytesseract
            custom_config = r'--psm 10'  # Nhận diện ký tự đơn lẻ
            text = pytesseract.image_to_string(thresh_image, lang='eng', config=custom_config)

            return text.strip()  # Trả về ký tự nhận diện được
        except Exception as e:
            return f"Lỗi: {str(e)}"

    def execute_swipe(self):
        """Thực hiện vuốt dựa trên tọa độ và thứ tự nhập"""
        # Lấy thứ tự chữ cái từ khung nhập
        order = self.input_line.text().split()
        if not order:
            print("Vui lòng nhập thứ tự chữ cái!")
            return
        print(order)

        # Xác định thứ tự vuốt dựa trên danh sách tọa độ
        try:
            # Lấy tọa độ trung tâm của từng chữ cái
            swipe_points = []
            for ch in order:
                # Tìm kiếm tọa độ của chữ cái trong self.coordinates
                coord = next((coord for letter, coord in self.coordinates if letter == ch), None)
                if coord is None:
                    print(f"Không tìm thấy tọa độ cho chữ cái: {ch}")
                    return
                # Tính toán tọa độ trung tâm của chữ cái
                x1, y1, x2, y2 = coord
                swipe_points.append(((x1 + x2) // 2, (y1 + y2) // 2))

        except Exception as e:
            print(f"An error occurred: {e}")
            return

        # Gửi lệnh vuốt qua ADB
        for i in range(len(swipe_points) - 1):
            x1, y1 = swipe_points[i]
            x2, y2 = swipe_points[i + 1]
            self.swipe(x1, y1, x2, y2)

    def swipe(self, x1, y1, x2, y2):
        """Gửi lệnh vuốt qua ADB"""
        command = f"adb shell input touchscreen swipe {x1} {y1} {x2} {y2} 300"
        os.system(command)
        print(f"Vuốt từ ({x1}, {y1}) đến ({x2}, {y2})")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = PhoneController()
    mainApp.show()
    sys.exit(app.exec_())
