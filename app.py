import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser, simpledialog
from PIL import Image, ImageDraw
import os

def new_file():
    canvas.delete("all")
    draw_tool.rectangle([0, 0, 500, 500], fill="white")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png"),
                                                        ("All Files", "*.*")])
    if file_path:
        drawing_image.save(file_path)
        messagebox.showinfo("Sauvegarde", f"Dessin enregistré sous {file_path}")

def exit_app():
    if messagebox.askokcancel("Quitter", "Voulez-vous quitter ?"):
        root.destroy()

def change_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color

def change_pen_size():
    global pen_size
    size = simpledialog.askinteger("Taille du stylo", "Entrez la taille du stylo:")
    if size:
        pen_size = size

def set_eraser():
    global pen_color
    pen_color = "white"

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=pen_size)
    draw_tool.line([(last_x, last_y), (event.x, event.y)], fill=pen_color, width=pen_size)
    last_x, last_y = event.x, event.y

root = tk.Tk()
root.title("Bloc-notes avec dessin")
root.geometry("800x600")
root.configure(bg="lightgray")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouveau", command=new_file)
file_menu.add_command(label="Enregistrer", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=exit_app)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

tool_menu = tk.Menu(menu_bar, tearoff=0)
tool_menu.add_command(label="Changer la couleur", command=change_color)
tool_menu.add_command(label="Changer la taille du stylo", command=change_pen_size)
tool_menu.add_command(label="Gomme", command=set_eraser)
menu_bar.add_cascade(label="Outils", menu=tool_menu)

frame = tk.Frame(root, bg="white")
frame.pack(expand=True, fill="both")

canvas = tk.Canvas(frame, bg="white", width=800, height=500)
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)

drawing_image = Image.new("RGB", (800, 500), "white")
draw_tool = ImageDraw.Draw(drawing_image)

pen_color = "black"
pen_size = 3

root.mainloop()
