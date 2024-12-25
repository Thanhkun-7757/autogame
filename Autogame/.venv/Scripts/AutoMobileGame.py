import os
import sys
from io import BytesIO
import tkinter as tk
from tkinter import Label, Button
from PyQt5.QtGui import QPainter, QPen
from PIL import Image, ImageTk
import pytesseract
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QApplication, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import subprocess
from PyQt5.QtCore import QRect, Qt, QTimer
from Test import recognize_character
class PhoneController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coordinates = []  # Lưu chữ cái và tọa độ
        self.start_pos = None  # Điểm bắt đầu
        self.end_pos = None    # Điểm kết thúc
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

        # Layout ngang cho hai nút
        button_layout = QHBoxLayout()

        # Nút kiểm tra kết nối
        self.check_connection_button = QPushButton("Kiểm tra kết nối", self)
        self.check_connection_button.clicked.connect(self.check_device_connection)
        button_layout.addWidget(self.check_connection_button)

        # Nút thực hiện chụp màn hình
        self.swipe_button = QPushButton("Chụp màn hình", self)
        self.swipe_button.clicked.connect(self.capture_screen_and_show)
        button_layout.addWidget(self.swipe_button)

        # Thêm layout ngang vào layout chính
        layout.addLayout(button_layout)

        # Label để hiển thị màn hình thiết bị
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Kiểm tra kết nối thiết bị và bắt đầu cập nhật ảnh
        if self.check_device_connection():
            self.start_screen_update()

    def capture_screen_and_show(self):
        """Chụp màn hình thiết bị và hiển thị trong cửa sổ mới"""
        try:
            # Chụp màn hình
            process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
            screenshot_data, _ = process.communicate()

            if not screenshot_data:
                self.show_message("Không thể chụp màn hình thiết bị. Kiểm tra kết nối ADB.", "Lỗi")
                return

            # Tạo cửa sổ mới
            window = tk.Toplevel()
            window.title("Ảnh chụp màn hình")
            window.geometry("480x800")

            # Hiển thị ảnh chụp màn hình
            image = Image.open(BytesIO(screenshot_data))
            image_resized = image.resize((480, 800), Image.Resampling.LANCZOS)
            image_tk = ImageTk.PhotoImage(image_resized)

            img_label = Label(window, image=image_tk)
            img_label.image = image_tk  # Giữ tham chiếu để không bị xóa
            img_label.pack(pady=10)

            # Thêm nút đóng cửa sổ
            close_button = Button(window, text="Đóng", command=window.destroy, font=("Arial", 12))
            close_button.pack(pady=20)

            # Hiển thị cửa sổ mới
            window.mainloop()

        except Exception as e:
            print(f"Lỗi khi chụp màn hình: {e}")
            self.show_message("Đã xảy ra lỗi khi chụp màn hình.", "Lỗi")

    def start_screen_update(self):
        """Bắt đầu cập nhật màn hình tự động"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen_image)
        self.timer.start(1000)  # Làm mới mỗi 1000ms (1 giây)

    def update_screen_image(self):
        """Cập nhật màn hình thiết bị trực tiếp"""
        try:
            process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
            screenshot_data, _ = process.communicate()

            if screenshot_data:
                pixmap = QPixmap()
                pixmap.loadFromData(screenshot_data)
                scaled_pixmap = pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
            else:
                self.show_message("Không thể chụp màn hình thiết bị. Kiểm tra kết nối ADB.", "Lỗi")
        except Exception as e:
            print(f"Lỗi khi lấy ảnh màn hình: {e}")
            self.show_message("Đã xảy ra lỗi khi lấy ảnh màn hình.", "Lỗi")

    def show_message(self, message, title="Thông báo"):
        """Hiển thị thông báo trong một hộp thoại riêng biệt"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def check_device_connection(self):
        """Kiểm tra kết nối với thiết bị qua ADB"""
        result = os.popen("adb devices").read()  # Chạy lệnh adb devices và lấy kết quả
        if "device" in result.splitlines()[1]:  # Kiểm tra nếu có thiết bị được liệt kê
            self.show_message("Kết nối thành công với thiết bị!", "Thành công")
            return True
        else:
            self.show_message("Không tìm thấy thiết bị. Vui lòng kiểm tra kết nối!", "Lỗi")
            return False

    def mousePressEvent(self, event):
        """Bắt đầu chọn vùng trên ảnh"""
        self.start_pos = event.pos()
        self.is_selecting = True

    def mouseMoveEvent(self, event):
        """Di chuyển chuột và vẽ hình chữ nhật trong khi chọn"""
        if self.is_selecting and self.start_pos:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Kết thúc chọn vùng và xử lý OCR"""
        self.end_pos = event.pos()
        self.is_selecting = False
        self.recognize_text(QRect(self.start_pos, self.end_pos))
        self.start_pos = None
        self.end_pos = None
        self.update()

    def paintEvent(self, event):
        """Vẽ hình chữ nhật khi di chuyển chuột"""
        if self.is_selecting and self.start_pos and self.end_pos:
            painter = QPainter(self.label.pixmap())
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos)
            painter.setBrush(Qt.transparent)
            painter.drawRect(rect)
            painter.end()
            self.label.update()

    def recognize_text(self, rect):
        """Nhận diện chữ từ vùng được chọn và hiển thị lên hộp thoại mới"""
        try:
            pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            print("start reco")
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
            screenshot_data, _ = process.communicate()

            image = Image.open(BytesIO(screenshot_data))
            # cropped = image.crop((x, y, x + w, y + h))

            # Nhận diện ký tự
            text = recognize_character(image)
            print('reco text :', text)

            # Thêm tọa độ và ký tự vào danh sách
            self.coordinates.append((text, (x, y, x + w, y + h)))

            # Hiển thị hộp thoại với ảnh đã chọn và thông tin
            self.show_result_dialog(image, text, (x, y, x + w, y + h))

        except Exception as e:
            print(f"An error occurred: {e}")

    def show_result_dialog(self, cropped_image, detected_text, coordinates):
        """Hiển thị hộp thoại với ảnh, ký tự và tọa độ."""
        # Tạo một cửa sổ mới
        window = tk.Toplevel()
        window.title("Kết quả nhận diện")
        window.geometry("400x500")

        # Hiển thị ảnh đã chọn
        image_resized = cropped_image.resize((300, 300), Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(image_resized)
        img_label = Label(window, image=image_tk)
        img_label.image = image_tk  # Giữ tham chiếu để không bị xóa
        img_label.pack(pady=10)

        # Hiển thị ký tự nhận diện được
        text_label = Label(window, text=f"Ký tự phát hiện: {detected_text}", font=("Arial", 14), wraplength=350)
        text_label.pack(pady=10)

        # Hiển thị tọa độ của vùng chọn
        coordinates_label = Label(window, text=f"Tọa độ: {coordinates}", font=("Arial", 12))
        coordinates_label.pack(pady=10)

        # Thêm nút đóng hộp thoại
        close_button = Button(window, text="Đóng", command=window.destroy, font=("Arial", 12))
        close_button.pack(pady=20)

        # Hiển thị hộp thoại
        window.mainloop()

    def execute_swipe(self):
        """Thực hiện vuốt dựa trên tọa độ và thứ tự nhập"""
        order = self.input_line.text().split()
        if not order:
            self.show_message("Vui lòng nhập thứ tự chữ cái!")
            return

        try:
            swipe_points = []
            for ch in order:
                coord = next((coord for letter, coord in self.coordinates if letter == ch), None)
                if coord is None:
                    self.show_message(f"Không tìm thấy tọa độ cho chữ cái: {ch}")
                    return
                x1, y1, x2, y2 = coord
                swipe_points.append(((x1 + x2) // 2, (y1 + y2) // 2))

            for i in range(len(swipe_points) - 1):
                x1, y1 = swipe_points[i]
                x2, y2 = swipe_points[i + 1]
                self.swipe(x1, y1, x2, y2)
        except Exception as e:
            print(f"An error occurred: {e}")

    def swipe(self, x1, y1, x2, y2):
        """Gửi lệnh vuốt qua ADB"""
        command = f"adb shell input touchscreen swipe {x1} {y1} {x2} {y2} 300"
        os.system(command)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = PhoneController()
    mainApp.show()
    sys.exit(app.exec_())
