import cv2
from PIL import Image
import pytesseract


# Đường dẫn đến tesseract nếu sử dụng Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def recognize_character(image_path):
    """Nhận diện ký tự từ ảnh đã crop."""
    try:
        # Đọc ảnh bằng OpenCV
        image = cv2.imread(image_path)

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


if __name__ == "__main__":
    # Đường dẫn đến ảnh crop (ảnh chứa ký tự đơn lẻ)
    image_path = "croppedN.png"  # Thay bằng đường dẫn đến ảnh của bạn
    character = recognize_character(image_path)
    print("Ký tự nhận diện được:")
    print(character)
