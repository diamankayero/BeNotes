import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime

# Fonction pour créer une nouvelle page
def new_page():
    global drawing_image, draw_tool
    canvas.delete("all")
    drawing_image = Image.new("RGB", (800, 500), "white")
    draw_tool = ImageDraw.Draw(drawing_image)

# Fonction pour enregistrer l'image
def save_as_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png"),
                                                       ("All Files", "*.*")])
    if file_path:
        drawing_image.save(file_path)
        messagebox.showinfo("Sauvegarde", f"Dessin enregistré sous {file_path}")

# Fonction pour exporter en PDF
def export_as_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        drawing_image.save("temp_drawing.png")
        img = Image.open("temp_drawing.png")
        img.save(file_path, "PDF")
        messagebox.showinfo("Export", f"Document exporté sous {file_path}")

# Fonction pour exporter en HTML
def export_as_html():
    file_path = filedialog.asksaveasfilename(defaultextension=".html",
                                             filetypes=[("HTML Files", "*.html")])
    if file_path:
        html_content = f"""
        <html>
        <head><title>Notes Exportées</title></head>
        <body>
        <h1>Notes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        <img src="temp_drawing.png" alt="Drawing">
        </body>
        </html>
        """
        with open(file_path, "w") as f:
            f.write(html_content)
        messagebox.showinfo("Export", f"Document exporté sous {file_path}")

# Changer la couleur du stylo
def change_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color

# Sélectionner la gomme avec différentes tailles
def set_eraser(size):
    global pen_color, eraser_mode, eraser_size
    pen_color = "white"
    eraser_mode = True
    eraser_size = size
    canvas.config(cursor="circle")  # Change le curseur en cercle pour la gomme

# Réinitialiser l'outil pour le stylo
def reset_tool(size):
    global pen_color, eraser_mode, pen_size
    pen_color = "black"
    eraser_mode = False
    pen_size = size
    canvas.config(cursor="pencil")  # Change le curseur en crayon pour le stylo

# Insérer une image dans le canevas
def insert_image():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(400, 250, image=img_tk, anchor=tk.CENTER)
        canvas.image = img_tk

# Initialiser la prise en main du dessin
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    if eraser_mode:
        return

# Fonction de dessin
def draw(event):
    global last_x, last_y, eraser_mode, eraser_size
    if eraser_mode:
        erase_area(last_x, last_y, event.x, event.y, eraser_size)
    else:
        canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=pen_size, capstyle=tk.ROUND, smooth=True)
        draw_tool.line([(last_x, last_y), (event.x, event.y)], fill=pen_color, width=pen_size)
    last_x, last_y = event.x, event.y

# Effacer une zone
def erase_area(x1, y1, x2, y2, size):
    global drawing_image, draw_tool
    draw_tool.line([(x1, y1), (x2, y2)], fill="white", width=size)
    canvas.create_line(x1, y1, x2, y2, fill="white", width=size, capstyle=tk.ROUND)

# Interface principale
root = tk.Tk()
root.title("GoodNotes-Like App")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Barre d'outils
toolbar = tk.Frame(root, bg="#d9d9d9", height=50)
toolbar.pack(fill="x")

# Ajouter les boutons
tk.Button(toolbar, text="📝 Nouvelle Page", command=new_page).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="🎨 Couleur", command=change_color).pack(side="left", padx=5, pady=5)

# Ajouter des boutons circulaires pour la taille du stylo
pen_frame = tk.Frame(toolbar, bg="#d9d9d9")
pen_frame.pack(side="left", padx=5, pady=5)

# Petites tailles de stylo
tk.Button(pen_frame, text="●", width=3, height=1, command=lambda: reset_tool(3), relief="solid").pack(side="left", padx=5, pady=5)
tk.Button(pen_frame, text="●", width=4, height=1, command=lambda: reset_tool(5), relief="solid").pack(side="left", padx=5, pady=5)
tk.Button(pen_frame, text="●", width=5, height=1, command=lambda: reset_tool(8), relief="solid").pack(side="left", padx=5, pady=5)

# Ajouter des boutons circulaires pour la gomme
eraser_frame = tk.Frame(toolbar, bg="#d9d9d9")
eraser_frame.pack(side="left", padx=5, pady=5)

tk.Button(eraser_frame, text="●", width=3, height=1, command=lambda: set_eraser(5), relief="solid").pack(side="left", padx=5, pady=5)
tk.Button(eraser_frame, text="●", width=4, height=1, command=lambda: set_eraser(10), relief="solid").pack(side="left", padx=5, pady=5)
tk.Button(eraser_frame, text="●", width=5, height=1, command=lambda: set_eraser(15), relief="solid").pack(side="left", padx=5, pady=5)

tk.Button(toolbar, text="🖼️ Image", command=insert_image).pack(side="left", padx=5, pady=5)

# Sauvegarde et exportation
tk.Button(toolbar, text="📷 Enregistrer", command=save_as_image).pack(side="right", padx=5, pady=5)
tk.Button(toolbar, text="📄 Export PDF", command=export_as_pdf).pack(side="right", padx=5, pady=5)
tk.Button(toolbar, text="📄 Export HTML", command=export_as_html).pack(side="right", padx=5, pady=5)

# Canvas pour dessiner
frame = tk.Frame(root, bg="white")
frame.pack(expand=True, fill="both")

canvas = tk.Canvas(frame, bg="white", width=800, height=500)
canvas.pack(fill="both", expand=True, padx=20, pady=10)
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)

# Initialisation de l'image et du dessin
drawing_image = Image.new("RGB", (800, 500), "white")
draw_tool = ImageDraw.Draw(drawing_image)

pen_color = "black"
eraser_mode = False
pen_size = 3
eraser_size = 5  # Taille de la gomme par défaut

# Initialisation du curseur (stylo)
canvas.config(cursor="pencil")

root.mainloop()
