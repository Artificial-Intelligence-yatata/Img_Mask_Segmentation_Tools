import tkinter as tk
from PIL import Image, ImageTk

class ImageRotator:
    def __init__(self, image_path, mask_path):
        self.image_path = image_path
        self.mask_path = mask_path
        self.angle = 0
        
        # Load the original image and the mask image
        self.original_image = Image.open(self.image_path)
        self.mask_image = Image.open(self.mask_path)
        
        # Get the dimensions of the images
        self.image_width, self.image_height = self.original_image.size
        
        # Create the GUI
        self.root = tk.Tk()
        self.root.title("Image Rotator")
        
        # Create the slider
        self.angle_slider = tk.Scale(self.root, from_=-180, to=180, orient=tk.HORIZONTAL, command=self.rotate_images)
        self.angle_slider.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a frame to hold the canvas for the original image and the mask image
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()
        
        # Create the canvas to display the original image
        self.image_canvas = tk.Canvas(self.image_frame, width=self.image_width, height=self.image_height)
        self.image_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Display the original image on the canvas
        self.image_tk = ImageTk.PhotoImage(self.original_image)
        self.image_item = self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        
        # Create the canvas to display the mask image
        self.mask_canvas = tk.Canvas(self.image_frame, width=self.image_width, height=self.image_height)
        self.mask_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Display the mask image on the canvas
        self.mask_tk = ImageTk.PhotoImage(self.mask_image)
        self.mask_item = self.mask_canvas.create_image(0, 0, anchor=tk.NW, image=self.mask_tk)
        
        # Run the GUI
        self.root.mainloop()
        
    def rotate_images(self, angle):
        # Convert the angle to degrees
        angle = int(angle)
        
        # Rotate the original image
        rotated_image = self.original_image.rotate(angle)
        
        # Rotate the mask image
        rotated_mask = self.mask_image.rotate(angle)
        
        # Create new PhotoImages from the rotated images
        self.image_tk = ImageTk.PhotoImage(rotated_image)
        self.mask_tk = ImageTk.PhotoImage(rotated_mask)
        
        # Update the canvas items with the new images
        self.image_canvas.itemconfig(self.image_item, image=self.image_tk)
        self.mask_canvas.itemconfig(self.mask_item, image=self.mask_tk)
        
        # Update the angle variable
        self.angle = angle
        
if __name__ == "__main__":
    image_path = r"C:\Users\LENOVO\Desktop\Nova pasta\Projetos\Tese_\Work\Dataset\Concrete\Positive\Images\CRACK500_20160222_080933_721_1921.jpg"
    mask_path = r"C:\Users\LENOVO\Desktop\Nova pasta\Projetos\Tese_\Work\Dataset\Concrete\Positive\Masks\CRACK500_20160222_080933_721_1921.jpg"
    ImageRotator(image_path, mask_path)

