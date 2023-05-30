import matplotlib.pyplot as plt
import numpy as np





x = np.linspace(-1, 1,100)

fig, ax = plt.subplots() # Create a figure and an axes.
ax.plot(x, x, label='T1')
ax.plot(x, 2*x**2-1, label='T2') 
ax.plot(x, 4*x**3-3*x, label='T3')
ax.plot(x, 8*x**4-8*x**2+1, label='T4')
ax.plot(x, 16*x**5-20*x**3+5*x, label='T5')
ax.plot(x, 32*x**6-48*x**4+ 18*x**2-1, label='T6') 
#ax.set_xlabel('x label') # Add an x-label to the axes.
#ax.set_ylabel('y label') # Add a y-label to the axes.
#ax.set_title("Chebyshev Polynomials") # Add a title to the axes.
#ax.legend() # Add a legend.

plt.savefig("plots/chebyshev.png")#'tight', transparent=True)

#plt.show()
