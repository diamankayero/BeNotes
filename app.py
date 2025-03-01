import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser, simpledialog
from PIL import Image, ImageDraw
import os

def new_file():
    text_area.delete("all")
    canvas.delete("all")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                      ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("all")
            text_area.insert("insert", file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        image_path = os.path.splitext(file_path)[0] + ".png"
        drawing_image.save(image_path)
        messagebox.showinfo("Sauvegarde", f"Dessin enregistré sous {image_path}")

def exit_app():
    if messagebox.askokcancel("Quitter", "Voulez-vous quitter ?"):
        root.destroy()

def change_font():
    font_family = simpledialog.askstring("Police", "Entrez le nom de la police (ex: Arial, Courier, Times):")
    font_size = simpledialog.askinteger("Taille de police", "Entrez la taille de la police:")
    if font_family and font_size:
        text_area.configure(font=(font_family, font_size))

def change_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.configure(fg=color)

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill="black", width=2)
    draw_tool.line([(last_x, last_y), (event.x, event.y)], fill="black", width=2)
    last_x, last_y = event.x, event.y

def insert_image():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = tk.PhotoImage(file=file_path)
        canvas.create_image(250, 250, image=img, anchor=tk.CENTER)
        canvas.image = img

root = tk.Tk()
root.title("Bloc-notes avancé")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouveau", command=new_file)
file_menu.add_command(label="Ouvrir", command=open_file)
file_menu.add_command(label="Enregistrer", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=exit_app)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Changer la police", command=change_font)
edit_menu.add_command(label="Changer la couleur", command=change_color)
menu_bar.add_cascade(label="Édition", menu=edit_menu)

insert_menu = tk.Menu(menu_bar, tearoff=0)
insert_menu.add_command(label="Insérer une image", command=insert_image)
menu_bar.add_cascade(label="Insertion", menu=insert_menu)

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

canvas = tk.Canvas(frame, bg="white", width=500, height=500)
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)

drawing_image = Image.new("RGB", (500, 500), "white")
draw_tool = ImageDraw.Draw(drawing_image)

root.mainloop()
