import customtkinter as ctk
from tkinter import filedialog
import os
import shutil
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

selected_folder = None


def log(message):
    log_box.insert("end", message + "\n")
    log_box.see("end")


def select_folder():
    global selected_folder
    
    log_box.delete("1.0", "end")
    folder = filedialog.askdirectory()

    if folder:
        selected_folder = folder
        path_label.configure(text=folder)
        log("Folder selected: " + folder)


def organize_files():
    progress.set(0)
    log_box.delete("1.0", "end")

    if not selected_folder:
        path_label.configure(text="Please select a folder first")
        return

    files = [f for f in os.listdir(selected_folder)
         if os.path.isfile(os.path.join(selected_folder, f))]
    total = len(files)
    count = 0
    log(f"Found {len(files)} files")

    file_types = {
        "Images": [".png", ".jpg", ".jpeg", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Videos": [".mp4", ".mkv"],
        "Music": [".mp3", ".wav"],
        "Archives": [".zip", ".rar"]
    }

    log("Starting file organization...")

    for filename in files:

        file_path = os.path.join(selected_folder, filename)

        if os.path.isfile(file_path):

            ext = os.path.splitext(filename)[1].lower()

            for category, extensions in file_types.items():

                if ext in extensions:

                    category_folder = os.path.join(selected_folder, category)

                    os.makedirs(category_folder, exist_ok=True)

                    shutil.move(file_path, os.path.join(category_folder, filename))

                    log(f"Moved {filename} → {category}")

                    break

        count += 1
        progress.set(count / total)
        app.update_idletasks()

    log("Organization complete!")
    path_label.configure(text="Files organized successfully")


app = ctk.CTk()
app.title("File Organizer")
app.geometry("520x480")
icon_path = "file_organizer/assets/icon.ico"

app.iconbitmap("file_organizer/assets/icon.ico")
app.iconbitmap("file_organizer/assets/icon.ico")







icon_image = ctk.CTkImage(
    light_image=Image.open(icon_path),
    dark_image=Image.open(icon_path),
    size=(32, 32)
)

title_frame = ctk.CTkFrame(app, fg_color="transparent")
title_frame.pack(pady=2)

icon_label = ctk.CTkLabel(title_frame, image=icon_image, text="")
icon_label.pack(side="left", padx=7)

title = ctk.CTkLabel(title_frame, text="File Organizer", font=("Arial", 26))
title.pack(side="left", pady=2)

path_label = ctk.CTkLabel(app, text="Select a folder to organize")
path_label.pack(pady=5)

select_button = ctk.CTkButton(app, text="Select Folder", command=select_folder)
select_button.pack(pady=5)

organize_button = ctk.CTkButton(app, text="Organize Files", command=organize_files)
organize_button.pack(pady=5)

progress = ctk.CTkProgressBar(app, width=350)
progress.pack(pady=10)
progress.set(0)




log_box = ctk.CTkTextbox(app, width=420, height=180)
log_box.pack(pady=10)

def clear_log():
    log_box.delete("1.0", "end")

clear_button = ctk.CTkButton(app, text="Clear Log", command=clear_log)
clear_button.pack(pady=5)

app.mainloop()