from PIL import Image 

# Import an image from directory:
#input_image = Image.new(mode="RGB", size=(200, 200))
input_image = Image.open("pixel_plot.png") 

# Extracting pixel map: 
pixel_map = input_image.load() 

# Extracting the width and height 
# of the image: 
width, height = input_image.size 

# taking half of the width: 
for i in range(width//2): 
    for j in range(height): 
        # getting the RGB pixel value. 
        #print(input_image.getpixel((i, j)) )
        r, g, b, p = input_image.getpixel((i, j)) 
        # Apply formula of grayscale: 
        grayscale = int(0.299*r + 0.587*g + 0.114*b) 
        # setting the pixel value.
        pixel_map[i, j] = (grayscale, grayscale, grayscale)
# Saving the final output 
# as "grayscale.png": 
input_image.save("grayscale.png") 

# use input_image.show() to see the image on the 
# output screen. 
