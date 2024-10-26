import tkinter as tk
from PIL import Image, ImageTk

menu = {
    "apple": 1,
    "banana": 2,
    "cherry": 3,
    "date": 4,
    "elderberry": 5
}

root = tk.Tk()
root.title("Image Display")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_aspect_ratio = screen_width / screen_height

image_path = "background.jpg"
image = Image.open(image_path)

image_width, image_height = image.size
image_aspect_ratio = image_width / image_height

if image_aspect_ratio > screen_aspect_ratio:
    new_width = int(image_height * screen_aspect_ratio)
    offset = (image_width - new_width) // 2
    image = image.crop((offset, 0, offset + new_width, image_height))
else:
    new_height = int(image_width / screen_aspect_ratio)
    offset = (image_height - new_height) // 2
    image = image.crop((0, offset, image_width, offset + new_height))

image = image.resize((screen_width, screen_height), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=photo)

box_width = int(screen_width * 0.8)
box_height = 200
box_x = (screen_width - box_width) // 2
box_y = 50
canvas.create_rectangle(
    box_x, box_y, box_x + box_width, box_y + box_height,
    fill='blue', stipple='gray50', outline='blue'
)

max_text_width = box_width - 20
max_text_height = box_height - 20
num_items = len(menu)
max_font_size = 100000

temp_text = canvas.create_text(0, 0, anchor=tk.NW, text="Sample", font=('Arial', max_font_size))
bbox = canvas.bbox(temp_text)
text_height = bbox[3] - bbox[1]
canvas.delete(temp_text)

while text_height * num_items > max_text_height and max_font_size > 1:
    max_font_size -= 2
    temp_text = canvas.create_text(0, 0, anchor=tk.NW, text="Sample", font=('Arial', max_font_size))
    bbox = canvas.bbox(temp_text)
    text_height = bbox[3] - bbox[1]
    canvas.delete(temp_text)

text_x = box_x + 10
text_y = box_y + 10
for item, price in menu.items():
    canvas.create_text(
        text_x, text_y, anchor=tk.NW,
        text=f"{item}: ${price}", fill='black', font=('Arial', max_font_size)
    )
    text_y += text_height

root.attributes("-fullscreen", True)
root.mainloop()
