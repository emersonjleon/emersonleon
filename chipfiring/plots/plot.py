# importing modules 
import numpy as np 
import matplotlib.pyplot as plt 

# creating a dataset 
# data is an array with four sub 
# arrays with 10 elements in each 
data = np.random.random((200, 200)) 

# creating a plot 
pixel_plot = plt.figure() 

# plotting a plot 
#pixel_plot.add_axes() 

# customizing plot 
#plt.title("pixel_plot") 
pixel_plot = plt.imshow( 
data, cmap='twilight', interpolation='nearest') 

plt.colorbar(pixel_plot) 

# save a plot 
plt.savefig('pixel_plot.png') 

# show plot 
plt.show(pixel_plot) 
