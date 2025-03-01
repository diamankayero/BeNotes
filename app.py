import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageTk
from fpdf import FPDF

def new_page():
    global drawing_image, draw_tool
    canvas.delete("all")
    drawing_image = Image.new("RGB", (800, 500), "white")
    draw_tool = ImageDraw.Draw(drawing_image)

def save_as_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png"),
                                                        ("All Files", "*.*")])
    if file_path:
        drawing_image.save(file_path)
        messagebox.showinfo("Sauvegarde", f"Dessin enregistré sous {file_path}")

def export_as_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        image_temp_path = "temp_drawing.png"
        drawing_image.save(image_temp_path)
        pdf.image(image_temp_path, x=10, y=10, w=190)
        pdf.output(file_path)
        os.remove(image_temp_path)
        messagebox.showinfo("Export", f"Document exporté sous {file_path}")

def change_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color

def set_eraser():
    global pen_color
    pen_color = "white"

def insert_image():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(400, 250, image=img_tk, anchor=tk.CENTER)
        canvas.image = img_tk

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=pen_size.get(), capstyle=tk.ROUND, smooth=True)
    draw_tool.line([(last_x, last_y), (event.x, event.y)], fill=pen_color, width=pen_size.get())
    last_x, last_y = event.x, event.y

root = tk.Tk()
root.title("GoodNotes-Like App")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Toolbar frame
toolbar = tk.Frame(root, bg="#d9d9d9", height=50)
toolbar.pack(fill="x")

# Adding buttons and sliders
tk.Button(toolbar, text="📝 Nouvelle Page", command=new_page).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="🎨 Couleur", command=change_color).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="🧽 Gomme", command=set_eraser).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="🖼️ Image", command=insert_image).pack(side="left", padx=5, pady=5)

# Adding a pen size slider (instead of entering numbers)
pen_size = tk.Scale(toolbar, from_=1, to=10, orient="horizontal", label="Taille du Stylo", length=200)
pen_size.set(3)  # Default pen size
pen_size.pack(side="left", padx=5, pady=5)

# Save and Export buttons
tk.Button(toolbar, text="📷 Enregistrer", command=save_as_image).pack(side="right", padx=5, pady=5)
tk.Button(toolbar, text="📄 Export PDF", command=export_as_pdf).pack(side="right", padx=5, pady=5)

# Canvas for drawing
frame = tk.Frame(root, bg="white")
frame.pack(expand=True, fill="both")

canvas = tk.Canvas(frame, bg="white", width=800, height=500)
canvas.pack(fill="both", expand=True, padx=20, pady=10)
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)

# Initialize drawing image and tool
drawing_image = Image.new("RGB", (800, 500), "white")
draw_tool = ImageDraw.Draw(drawing_image)

pen_color = "black"

root.mainloop()
