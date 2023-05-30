import matplotlib.pyplot as plt
import numpy as np
import ff


I=[0]
p=3
x = np.linspace(0, 1,3600)

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

#x=frange(0,1,0.02)

gI1=[ff.gI(xval,I,p) for xval in x]
gI2=[ff.gI(xval,I,p) for xval in gI1]
gI3=[ff.gI(xval,I,p) for xval in gI2]
gI4=[ff.gI(xval,I,p) for xval in gI3]


fig, ax = plt.subplots() # Create a figure and an axes.
ax.scatter(x, x, label='gI0',s=0.08)
ax.scatter(x, gI1, label='gI1',s=0.08) 
ax.scatter(x, gI2, label='gI2',s=0.08) 
ax.scatter(x, gI3, label='gI3',s=0.28) 
ax.scatter(x, gI4, label='gI4',s=0.38) 
#ax.set_xlabel('x label') # Add an x-label to the axes.
#ax.set_ylabel('y label') # Add a y-label to the axes.
#ax.set_title("Chebyshev Polynomials") # Add a title to the axes.
#ax.legend() # Add a legend.


plt.show()
