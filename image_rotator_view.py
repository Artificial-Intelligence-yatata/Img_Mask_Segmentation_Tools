import tkinter as tk
from PIL import Image, ImageTk

class ImageRotator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.angle = 0
        
        # Load the image
        self.original_image = Image.open(self.image_path)
        self.image_width, self.image_height = self.original_image.size
        
        # Create the GUI
        self.root = tk.Tk()
        self.root.title("Image Rotator")
        
        # Create the slider
        self.angle_slider = tk.Scale(self.root, from_=-180, to=180, orient=tk.HORIZONTAL, command=self.rotate_image)
        self.angle_slider.pack(fill=tk.X, padx=10, pady=10)
        
        # Create the canvas to display the image
        self.canvas = tk.Canvas(self.root, width=self.image_width, height=self.image_height)
        self.canvas.pack()
        
        # Display the original image on the canvas
        self.image_tk = ImageTk.PhotoImage(self.original_image)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        
        # Run the GUI
        self.root.mainloop()
        
    def rotate_image(self, angle):
        # Convert the angle to degrees
        angle = int(angle)
        
        # Rotate the original image
        rotated_image = self.original_image.rotate(angle)
        
        # Create a new PhotoImage from the rotated image
        self.image_tk = ImageTk.PhotoImage(rotated_image)
        
        # Update the canvas with the new image
        self.canvas.itemconfig(self.image_item, image=self.image_tk)
        
        # Update the angle variable
        self.angle = angle
        
if __name__ == "__main__":
    image_path = r"C:\Users\LENOVO\Desktop\Nova pasta\Projetos\Tese_\Work\Dataset\Concrete\Positive\Images\GAPS384_train_0670_541_641.jpg"
    ImageRotator(image_path)
