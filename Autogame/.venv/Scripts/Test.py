import cv2
from PIL import Image
import pytesseract
import numpy as np


def recognize_character(image_input):
    """Nhận diện ký tự từ ảnh đã crop."""
    try:
        if isinstance(image_input, str):  # If the input is a file path
            # Đọc ảnh bằng OpenCV
            image = cv2.imread(image_input)
        elif isinstance(image_input, Image.Image):  # If the input is a PIL image
            # Convert PIL Image to OpenCV format
            image = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
        else:
            raise ValueError("Input must be a file path or PIL.Image.Image object")

        # Chuyển ảnh sang dạng grayscale (đơn sắc)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Áp dụng threshold để làm rõ ký tự
        _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Lưu ảnh đã xử lý (nếu cần kiểm tra)
        cv2.imwrite("processed_image.png", thresh_image)

        # Nhận diện ký tự bằng pytesseract
        text = pytesseract.image_to_string(thresh_image, lang='eng', config='--psm 10')
        # '--psm 10': Cấu hình Tesseract cho nhận diện ký tự đơn lẻ

        return text.strip()
    except Exception as e:
        return f"Lỗi: {str(e)}"
