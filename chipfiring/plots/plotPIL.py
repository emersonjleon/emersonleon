from PIL import Image 


colormap=[(0,0,255),
          (200,200,255),
          (255,255,0),
          (100,30,50),
          (100,50,150),
          (0,0,0)]




# Import an image from directory:
input_image = Image.new(mode="RGB", size=(200, 200))
#input_image = Image.open("pixel_plot.png") 


# Extracting pixel map: 
pixel_map = input_image.load() 

# Extracting the width and height 
# of the image: 
width, height = input_image.size 

#print(input_image.getpixel((i, j)) )

# taking half of the width: 
for i in range(width//2): 
    for j in range(height): 
        # setting the pixel value.
        pixel_map[i, j] = colormap[database(i,j)]
# Saving the final output 
# as "grayscale.png": 
input_image.save("grayscale.png") 

# use input_image.show() to see the image on the 
# output screen. 
