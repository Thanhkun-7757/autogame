import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askinteger

# Mock data for installed apps
installed_apps = {
    "MÁY 1": ["Candy Crush", "Đào Vàng", "Câu Cá", "Bắn Cung", "Chụp Ảnh", "Con Mèo", "Con Chó", "Con Gà"],
    "MÁY 2": ["Game A", "Game B", "Game C"],
    "MÁY 3": ["Game D", "Game E"],
    "MÁY 4": ["Game J"],
    "MÁY 5": ["Game K", "Game L"],
    "MÁY 6": []
}

def add_game_action(machine_name, checkbox_var):
    if checkbox_var.get():
        # Create a new window for Bảng 2
        table2_window = tk.Toplevel(root)
        table2_window.title(f"Bảng 2: Installed Apps for {machine_name}")

        # Left frame for installed apps
        left_frame = tk.Frame(table2_window)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text=f"Installed Apps for {machine_name}", font=("Arial", 12, "bold")).pack(pady=5)

        # Right frame for selected apps
        right_frame = tk.Frame(table2_window)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="Selected Apps", font=("Arial", 12, "bold")).pack(pady=5)

        selected_apps_frame = tk.Frame(right_frame)
        selected_apps_frame.pack(fill="both", expand=True)

        def add_to_selected(app_name):
            row = tk.Frame(selected_apps_frame)
            row.pack(fill="x", pady=2)
            label = tk.Label(row, text=app_name, anchor="w", width=25)
            label.pack(side="left", padx=5)

            remove_btn = tk.Button(row, text="Remove", command=lambda: row.destroy())
            remove_btn.pack(side="right", padx=5)

            # Auto-remove after a set time
            set_auto_remove(row)

        def set_auto_remove(row):
            delay = askinteger("Set Time", "Enter time in seconds to auto-remove:")
            if delay and delay > 0:
                row.after(delay * 1000, lambda: row.destroy())

        def remove_all():
            for widget in selected_apps_frame.winfo_children():
                widget.destroy()

        def load_installed_apps():
            for widget in app_list_frame.winfo_children():
                widget.destroy()

            apps = installed_apps.get(machine_name, [])
            if apps:
                for app in apps:
                    app_frame = tk.Frame(app_list_frame)
                    app_frame.pack(fill="x", pady=2)

                    tk.Label(app_frame, text=app, font=("Arial", 10), anchor="w").pack(side="left", padx=5)
                    tk.Button(app_frame, text="Add", command=lambda a=app: add_to_selected(a)).pack(side="right")
            else:
                tk.Label(app_list_frame, text="No apps installed.", font=("Arial", 10), anchor="w").pack(pady=2)

        # Frame for the list of apps
        app_list_frame = tk.Frame(left_frame)
        app_list_frame.pack(fill="both", expand=True)

        # Populate initial apps
        load_installed_apps()

        # Add "Load App Install" button
        load_btn = tk.Button(left_frame, text="Load App Install", bg="blue", fg="white", command=load_installed_apps)
        load_btn.pack(pady=5)

        # Add Remove All button
        tk.Button(right_frame, text="Remove All", bg="red", command=remove_all).pack(pady=5)
    else:
        messagebox.showwarning("Warning", f"Please select the checkbox for {machine_name} to proceed.")

def toggle_run_stop(button, machine_name):
    if button["text"] == "RUN":
        button.config(text="STOP", bg="red")
        messagebox.showinfo("Action", f"Game started for {machine_name}")
    else:
        button.config(text="RUN", bg="green")
        messagebox.showinfo("Action", f"Game stopped for {machine_name}")

# Initialize the main window (Bảng 1)
root = tk.Tk()
root.title("TOOLS AUTO CHANGE GAME - Bảng 1")

# Bảng 1
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

tk.Label(header_frame, text="TÊN MÁY", width=20, font=("Arial", 12, "bold")).grid(row=0, column=1)
tk.Label(header_frame, text="TIẾN TRÌNH", width=30, font=("Arial", 12, "bold")).grid(row=0, column=2)
tk.Label(header_frame, text="", width=20).grid(row=0, column=3)  # Spacer
tk.Label(header_frame, text="", width=20).grid(row=0, column=4)  # Spacer

machines = ["MÁY 1", "MÁY 2", "MÁY 3", "MÁY 4", "MÁY 5", "MÁY 6"]

for machine in machines:
    row_frame = tk.Frame(root)
    row_frame.pack(fill="x", pady=5)

    # Checkbox
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(row_frame, variable=checkbox_var)
    checkbox.grid(row=0, column=0, padx=5)

    # Machine name
    machine_label = tk.Label(row_frame, text=machine, width=20, anchor="w", font=("Arial", 10))
    machine_label.grid(row=0, column=1)

    # Status
    status_label = tk.Label(row_frame, text="ĐANG CHẠY GAME THỨ BAO NHIÊU", width=30, anchor="w", font=("Arial", 10))
    status_label.grid(row=0, column=2)

    # Add Game Button
    add_game_btn = tk.Button(row_frame, text="Add Game", bg="yellow",
                             command=lambda m=machine, v=checkbox_var: add_game_action(m, v))
    add_game_btn.grid(row=0, column=3, padx=5)

    # Run/Stop Button
    run_stop_btn = tk.Button(row_frame, text="RUN", bg="green")
    run_stop_btn.config(command=lambda b=run_stop_btn, m=machine: toggle_run_stop(b, m))
    run_stop_btn.grid(row=0, column=4, padx=5)

# Run the main loop
root.mainloop()
