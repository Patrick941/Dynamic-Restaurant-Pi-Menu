import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Image Display")

# Load the image
image_path = "background.jpg"  # Replace with your image path
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
label = tk.Label(root, image=photo)
label.pack()

# Run the application
root.mainloop()