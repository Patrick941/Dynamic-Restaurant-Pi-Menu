import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
import csv

menu = {}
with open('menu.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        if not row:  # Skip empty lines
            continue
        item, price = row
        menu[item] = float(price)

# Function to create a rounded rectangle
def create_rounded_rectangle(canvas, colour, x1, y1, x2, y2, radius=25, **kwargs):
    def name_to_rgb(name):
        colours = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0),
            'lightblue': (173, 216, 230),
            # Add more named colours as needed
        }
        return colours.get(name.lower(), (0, 0, 0))  # Default to black if colour name not found

    rgb_colour = name_to_rgb(colour)
    alpha = int(transparency * 255)
    rgb_colour_with_alpha = rgb_colour
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, fill=rgb_colour, **kwargs, smooth=True)

# Depth = 0 means not interacting
# Depth = 1 means scrolling menu
# Depth = 2 means editing item name
# Depth = 3 means editing price
depth = 0

transparency = 0.4

# Function to open the application on a specific monitor
def open_on_monitor(monitor_number=0):
    root = tk.Tk()
    root.title("Image Display")

    # Get monitor information
    monitors = get_monitors()
    if monitor_number >= len(monitors):
        print(f"Monitor {monitor_number} not available.")
        return

    monitor = monitors[monitor_number]
    screen_width, screen_height = monitor.width, monitor.height
    x_offset, y_offset = monitor.x, monitor.y
    screen_aspect_ratio = screen_width / screen_height

    # Load and process the image
    image_path = "background.jpg"
    image = Image.open(image_path)
    image_width, image_height = image.size
    image_aspect_ratio = image_width / image_height

    # Crop image to fit the screen aspect ratio
    if image_aspect_ratio > screen_aspect_ratio:
        new_width = int(image_height * screen_aspect_ratio)
        offset = (image_width - new_width) // 2
        image = image.crop((offset, 0, offset + new_width, image_height))
    else:
        new_height = int(image_width / screen_aspect_ratio)
        offset = (image_height - new_height) // 2
        image = image.crop((0, offset, image_width, offset + new_height))

    # Resize image to screen dimensions
    image = image.resize((screen_width, screen_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Create canvas to display the image
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Create the blue semi-transparent box
    box_width = int(screen_width * 0.8)
    box_height = int(screen_height * 0.8)
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2  # Centre the box vertically
    create_rounded_rectangle(
        canvas, 'blue', box_x, box_y, box_x + box_width, box_y + box_height,
        radius=20, outline='blue'
    )

    # Calculate maximum font size
    max_text_width = box_width - 20
    max_text_height = box_height - 20
    num_items = len(menu)
    max_font_size = 100000

    # Temporarily create a text item to calculate font size
    temp_text = canvas.create_text(0, 0, anchor=tk.NW, text="Sample", font=('Arial', max_font_size))
    bbox = canvas.bbox(temp_text)
    text_height = bbox[3] - bbox[1]
    canvas.delete(temp_text)

    # Calculate the font size that fits within the box
    max_font_size = 50
    font_size = min(max_text_height // num_items, max_text_width // len(max(menu, key=len)))
    if (font_size > max_font_size):
        font_size = max_font_size
    font = ('Arial', font_size)

    # Variables to keep track of the selected item
    selected_index = -1
    text_items = []

    # Function to update the display
    def update_display():
        for i, (item, price) in enumerate(menu.items()):
            text_x = box_x + padding
            text_y = box_y + padding + i * (max_text_height // num_items)
            bounding_box_width = box_width - (2 * padding)
            text_box_width = box_width * split - (2 * padding)
            text_box_height = max_text_height // num_items - 5

            # Create a lighter background for each text box            
            if i == selected_index:
                if (depth == 1):
                    bg_colour = 'yellow'
                elif (depth == 2):
                    bg_colour = 'orange'
            else:
                bg_colour = 'lightblue'
            create_rounded_rectangle(
                canvas, bg_colour, text_x, text_y, text_x + bounding_box_width, text_y + text_box_height,
                radius=10, outline='blue'
            )

            # Calculate the vertical centre position for the text
            text_bbox = canvas.create_text(0, 0, anchor=tk.NW, text=item, font=font)
            bbox = canvas.bbox(text_bbox)
            text_height = bbox[3] - bbox[1]
            canvas.delete(text_bbox)
            text_y_centred = text_y + (text_box_height - text_height) // 2

            # Create the text item centred vertically
            if depth != 2:
                item_text = canvas.create_text(text_x + (2*padding), text_y_centred, anchor=tk.NW, text=item, font=font, fill='white')
            else:
                item_text = canvas.create_text(text_x + (2*padding), text_y_centred, anchor=tk.NW, text=item, font=font, fill='red')
            if depth != 3:
                price_text = canvas.create_text(text_x + (2*padding) + text_box_width, text_y_centred, anchor=tk.NW, text=f"€{price:.2f}", font=font, fill='white')
            else:
                price_text = canvas.create_text(text_x + (2*padding) + text_box_width, text_y_centred, anchor=tk.NW, text=f"€{price:.2f}", font=font, fill='red')
            text_items.append((item_text, price_text))

    # Function to handle key press events
    def on_key_press(event):
        nonlocal selected_index
        
        # Depth management
        if (depth == 0):
            if event.keysym == 'Return':
                selected_index = 0
            elif event.keysym == 'Escape':
                selected_index = -1
        elif (depth == 1):
            if event.keysym == 'Return':
                depth = 2
            elif event.keysym == 'Escape':
                depth = 0
                selected_index = -1
        elif (depth == 2):
            if event.keysym == 'Return':
                depth = 3
            elif event.keysym == 'Escape':
                depth = 1
        elif (depth == 3):
            if event.keysym == 'Return':
                depth = 1
            elif event.keysym == 'Escape':
                depth = 2
        
        
        
        
        elif (depth == 1):
            if event.keysym == 'Up':
                selected_index = (selected_index - 1) % num_items
            elif event.keysym == 'Down':
                selected_index = (selected_index + 1) % num_items
        canvas.delete('all')
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        create_rounded_rectangle(
            canvas, box_x, box_y, box_x + box_width, box_y + box_height,
            radius=20, fill='blue', stipple='gray50', outline='blue'
        )
        update_display()

    # Bind the arrow keys to the on_key_press function
    root.bind('<Up>', on_key_press)
    root.bind('<Down>', on_key_press)

    # Initial display update
    split = 0.8
    padding = 10
    update_display()

    # Set the window to be fullscreen and positioned on the selected monitor
    root.geometry(f"{screen_width}x{screen_height}+{x_offset}+{y_offset}")
    root.attributes("-fullscreen", True)
    root.mainloop()

# Open the window on the second monitor (if available)
open_on_monitor(monitor_number=2)
