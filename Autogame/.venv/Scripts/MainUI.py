import tkinter as tk
from tkinter import ttk
from AutoMobileGame import PhoneController  # Import hàm từ file khác

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Danh sách điện thoại")
        self.root.geometry("800x600")

        self.check_vars = []  # Lưu trạng thái của các checkbox

        # Header
        header_frame = tk.Frame(root)
        header_frame.pack(pady=10)

        tk.Entry(header_frame, width=10).grid(row=0, column=0, padx=5)
        tk.Entry(header_frame, width=10).grid(row=0, column=1, padx=5)

        tk.Button(header_frame, text="📸", width=2,command=self.open_phone_controller).grid(row=0, column=2, padx=5)
        tk.Label(header_frame, text="Kịch bản").grid(row=0, column=3, padx=5)
        ttk.Combobox(header_frame, values=["Kịch bản 1", "Kịch bản 2"], width=15).grid(row=0, column=4, padx=5)
        tk.Button(header_frame, text="New").grid(row=0, column=5, padx=5)
        tk.Button(header_frame, text="Edit").grid(row=0, column=6, padx=5)
        tk.Button(header_frame, text="Load").grid(row=0, column=7, padx=5)

        # Danh sách điện thoại
        tk.Label(root, text="Danh sách điện thoại", font=("Arial", 12)).pack(pady=10)

        # Table frame
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10)

        # Header row
        header_row = tk.Frame(table_frame)
        header_row.pack(fill="x")

        tk.Checkbutton(header_row).pack(side=tk.LEFT, padx=5)  # Checkbox
        tk.Label(header_row, text="Tên thiết bị", width=20, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_row, text="Tên kịch bản", width=20, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_row, text="Hành động", width=20, anchor="w").pack(side=tk.LEFT)

        # Render danh sách
        self.render_device_list(table_frame)

        # Chọn đồng loạt
        actions_frame = tk.Frame(root)
        actions_frame.pack(pady=10)

        tk.Label(actions_frame, text="Chọn đồng loạt").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(actions_frame, values=["Kịch bản 1", "Kịch bản 2"], width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="Chạy").pack(side=tk.LEFT, padx=5)

    def render_device_list(self, parent):
        # Data
        devices = [
            ("Máy 1", "Kịch bản 1"),
            ("Máy 2", "Kịch bản 1"),
            ("Máy 3", "Kịch bản 2"),
            ("Máy 4", "Kịch bản 2"),
            ("Máy 5", "Kịch bản 1"),
        ]

        for device in devices:
            row = tk.Frame(parent)
            row.pack(fill="x")

            # Checkbox
            check_var = tk.BooleanVar()
            self.check_vars.append(check_var)
            tk.Checkbutton(row, variable=check_var).pack(side=tk.LEFT, padx=5)

            # Device name
            tk.Label(row, text=device[0], width=20, anchor="w").pack(side=tk.LEFT)

            # Script name
            tk.Label(row, text=device[1], width=20, anchor="w").pack(side=tk.LEFT)

            # Actions
            action_frame = tk.Frame(row)
            action_frame.pack(side=tk.LEFT)
            ttk.Button(action_frame, text="Kịch bản").pack(side=tk.LEFT, padx=5)
            ttk.Button(action_frame, text="Chạy").pack(side=tk.LEFT, padx=5)


    def open_phone_controller(self):
        """Hàm mở cửa sổ PhoneController"""
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)  # Tạo QApplication
        phone_controller = PhoneController()  # Khởi tạo PhoneController
        phone_controller.show()  # Hiển thị cửa sổ
        sys.exit(app.exec_())  # Bắt đầu vòng lặp sự kiện
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
