import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from screeninfo import get_monitors
import csv
import os
import re

images = []
menu = {}

with open('menu.csv', mode='r') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        if not row:  # Skip empty lines
            continue
        item_name, price = row
        menu[index] = {'name': item_name, 'price': float(price)}
        
if os.path.exists('auto_complete.csv'):
    with open('auto_complete.csv', 'r') as file:
        reader = csv.reader(file)
        auto_complete_data = {}
        for index, row in enumerate(reader):
            if not row:  # Skip empty lines
                continue
            item_name, price = row
            auto_complete_data[index] = {'name': item_name, 'price': float(price)}
else:
    auto_complete_data = []
    with open('auto_complete.csv', 'w') as file:
        file.write('')
    with open('menu.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for item in menu.values():
            writer.writerow([item['name'], item['price']])
        auto_complete_data = [item['name'] for item in menu.values()]

def write_to_csv():
    with open('menu.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in menu.values():
            writer.writerow([item['name'], item['price']])

def create_rounded_rectangle(root, canvas, colour, x1, y1, x2, y2, radius=25, transparency=0.5, **kwargs):
    alpha = int(transparency * 255)
    rgb_fill = root.winfo_rgb(colour)
    rgba_fill = (rgb_fill[0] // 256, rgb_fill[1] // 256, rgb_fill[2] // 256, alpha)
    width, height = x2 - x1, y2 - y1
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=rgba_fill)
    photo_image = ImageTk.PhotoImage(image)
    canvas.create_image(x1, y1, image=photo_image, anchor='nw')
    images.append(photo_image)
    return photo_image

def create_background_rectangle(root, canvas, screen_width, screen_height):
    box_width = int(screen_width * 0.8)
    box_height = int(screen_height * 0.8)
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2
    create_rounded_rectangle(
        root, canvas, 'blue', box_x, box_y, box_x + box_width, box_y + box_height,
        radius=20, outline=''
    )
    return box_x, box_y, box_width, box_height

depth = 0
temp_price = None
transparency = 0.3

def open_on_monitor(monitor_number=0):
    global num_items
    root = tk.Tk()
    root.title("Restaurant Menu")
    root.after(100, lambda: root.focus_force())
    root.focus_force()
    root.focus_set()
    root.attributes("-topmost", True)
    root.after(200, lambda: root.attributes("-topmost", False))
    monitors = get_monitors()
    if monitor_number >= len(monitors):
        print(f"Monitor {monitor_number} not available.")
        return

    monitor = monitors[monitor_number]
    screen_width, screen_height = monitor.width, monitor.height
    x_offset, y_offset = monitor.x, monitor.y
    screen_aspect_ratio = screen_width / screen_height
    # Find the number file
    number_file = None
    for file in os.listdir('.'):
        if re.match(r'number\d+', file):
            number_file = file
            break

    if number_file:
        with open(number_file, 'r') as f:
            number = f.read().strip()

    image_path = f"background{number}.jpg"
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
    box_x, box_y, box_width, box_height = create_background_rectangle(root, canvas, screen_width, screen_height)
    images.clear()
            
    max_text_width = box_width - 20
    max_text_height = box_height - 20
    num_items = len(menu)
    max_font_size = 50
    font_size = min(max_text_height // num_items, max_text_width // max(len(item['name']) for item in menu.values()))
    font_size = min(font_size, max_font_size)
    font = ('Arial', font_size)

    selected_index = -1
    text_items = []

    def update_display():
        create_background_rectangle(root, canvas, screen_width, screen_height)
        for i, (index, item_data) in enumerate(menu.items()):
            item_name, price = item_data['name'], item_data['price']
            text_x = box_x + padding
            text_y = box_y + padding + i * (max_text_height // num_items)
            bounding_box_width = box_width - (2 * padding)
            text_box_width = box_width * split - (2 * padding)
            text_box_height = max_text_height // num_items - 5

            if i == selected_index:
                bg_colour = 'yellow' if depth == 1 else 'orange' if depth >= 2 else 'lightblue'
                name_text_color = 'red' if depth == 2 else 'white'
                price_text_color = 'red' if depth == 3 else 'white'
            else:
                bg_colour = 'lightblue'
                name_text_color = 'white'
                price_text_color = 'white'

            create_rounded_rectangle(
                root, canvas, bg_colour, text_x, text_y, text_x + bounding_box_width, text_y + text_box_height,
                radius=10, outline=''
            )

            text_y_centred = text_y + (text_box_height - font_size) // 2
            item_text = canvas.create_text(text_x + (2 * padding), text_y_centred, anchor=tk.NW, text=item_name, font=font, fill=name_text_color)
            if depth != 3 or i != selected_index:
                price_text = canvas.create_text(text_x + (2 * padding) + text_box_width, text_y_centred, anchor=tk.NW, text=f"€{price:.2f}", font=font, fill=price_text_color)
            else:
                price_text = canvas.create_text(text_x + (2 * padding) + text_box_width, text_y_centred, anchor=tk.NW, text=f"€{temp_price}", font=font, fill=price_text_color)
            text_items.append((item_text, price_text))
            
    def pop_item(selected_index):
        menu.pop(selected_index)
        for i in range(selected_index, len(menu)):
            menu[i] = menu.pop(i + 1, None)

    def on_key_press(event):
        nonlocal selected_index
        global depth, num_items, temp_price

        for item_text, price_text in text_items:
            canvas.delete(item_text)
            canvas.delete(price_text)
        text_items.clear()
        images.clear()
        
        print(event.keysym)

        if depth == 0:
            if event.keysym == 'Return':
                selected_index = 0
                depth = 1
            elif event.keysym == 'Escape':
                selected_index = -1
                depth = 0
            elif event.keysym == 'minus':
                exit()
        elif depth == 1:
            if event.keysym == 'Return':
                depth = 2
            elif event.keysym == 'Escape':
                depth = 0
                selected_index = -1
            elif event.keysym == 'Up':
                selected_index = (selected_index - 1) % num_items
            elif event.keysym == 'Down':
                selected_index = (selected_index + 1) % num_items
            elif event.keysym == 'BackSpace':
                pop_item(selected_index)
                num_items -= 1
                selected_index = 0
            elif event.keysym == 'plus':
                menu[len(menu)] = {'name': '', 'price': 0.0}
                num_items += 1
        elif depth == 2:
            if event.keysym == 'Return':
                depth = 3
                write_to_csv()
            elif event.keysym == 'Escape':
                depth = 1
                write_to_csv()
            elif event.keysym == 'BackSpace' and selected_index >= 0:
                item = menu[selected_index]
                item['name'] = item['name'][:-1]
            elif event.keysym == 'space' and selected_index >= 0:
                item = menu[selected_index]
                item['name'] += ' '
            elif (event.char.isalnum() or event.char in "&") and selected_index >= 0:
                item = menu[selected_index]
                item['name'] += event.char
            elif event.keysym == 'Tab' and selected_index >= 0:
                item = menu[selected_index]
                item['name'] += '\t'
        elif depth == 3:
            item = menu[selected_index]
            if temp_price is None:
                temp_price = ""

            if event.char.isdigit():
                if temp_price == "":
                    item['price'] = 0
                temp_price += event.char
                item['price'] = float(temp_price)
            
            elif event.keysym == 'BackSpace' and temp_price:
                temp_price = temp_price[:-1]
                item['price'] = float(temp_price) if temp_price else 0.0

            elif event.char == '.' and '.' not in temp_price:
                temp_price += event.char

            elif event.keysym == 'Return':
                item['price'] = float(temp_price) if temp_price else 0.0
                temp_price = None
                depth = 1
                write_to_csv()
            elif event.keysym == 'Escape':
                temp_price = None
                depth = 1
                write_to_csv()

        update_display()

    padding = 10
    split = 0.7

    root.geometry(f"{screen_width}x{screen_height}+{x_offset}+{y_offset}")
    root.attributes("-fullscreen", True)
    root.overrideredirect(True)

    root.bind("<KeyPress>", on_key_press)
    update_display()
    root.mainloop()


open_on_monitor(monitor_number=0)
