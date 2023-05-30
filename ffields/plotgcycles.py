import matplotlib.pyplot as plt
import numpy as np
import ff

plt.rcParams['font.family'] = 'serif'

def plotgIpn(ax, p,n,I,pcolor="black",lwidth=0.5):
    """generate the line plots corresponding to an increase set I"""
    for i in range(p**n):
        incr =ff.intiIncreases(i,I,p,n)
        xcoords=[i/p**n,(i+1)/p**n]
        if incr:
            ycoords=[0,1]
        else:
            ycoords=[1,0]
        ax.plot(xcoords,ycoords,color=pcolor,
                linewidth=lwidth)

        
def createJSplot(p,n,I):
    """to be used in interactive plot from app.py, templates/ffields.html"""
    final={}
    texts=[]
    count=0
    for cycle in ff.pcycles(p,n):
        xcoords=[]
        ycoords=[]
        cycletexts=[]
        invcycle=ff.piIinvcycle(cycle,p,n,I)
        print("#########  ",cycle)
        #print(invcycle)
        for i in invcycle:
            xi=ff.xiI(i,p,n,I)
            xcoords.extend([xi,xi])
            ycoords.extend([xi,ff.gI(xi,I,p)]) #gI(xi)=x{inext}
            cycletexts.extend([f"X{i}={xi}", f"f(X{i}) = {ff.gI(xi,I,p)}"]) #gI(xi)=x{inext}
        # xcoords.append(xcoords[0])
        # ycoords.append(ycoords[0])
        # cycletexts.append
        # final[count]={"invcycle":invcycle, "xcoords":xcoords, "ycoords":ycoords}

        final[count]=[ [xcoords[i], ycoords[i]] for i in range(len(xcoords))]
        texts.append(cycletexts)
        count+=1
    return final, texts


def createfullpnIplot(p,n,I):
    fig, ax = plt.subplots()# Create a figure and an axes.
    plt.rcParams["figure.figsize"] = (15,15)## Size of picture!!
    ax.plot([0,1],[0,1],color='k')
    plotgIpn(ax, p,1,I,pcolor="black",lwidth=0.8)
    plotgIpn(ax, p,n,I,pcolor="black")
    #ax.set_title(f'p={p}, n={n}; I={I}.') # Add a title
    print("p=",p,": n=",n,"; I=",I)
    #print(ff.pcycles(p,n))
    for cycle in ff.pcycles(p,n):
        xcoords=[]
        ycoords=[]
        invcycle=ff.piIinvcycle(cycle,p,n,I)
        #print(invcycle)
        for i in invcycle:
            xi=ff.xiI(i,p,n,I)
            xcoords.extend([xi,xi])
            ycoords.extend([xi,ff.gI(xi,I,p)])
        xcoords.append(xcoords[0])
        ycoords.append(ycoords[0])
        ax.plot(xcoords, ycoords, marker= 'o')
        
        #ax.legend() # Add a legend.

def saveplot(p,n,I,filename):
    createfullpnIplot(p,n,I)
    plt.savefig(filename)#'tight', transparent=True)

        
if __name__ == '__main__':
    I=[0,2,4]
    p=6
    n=2
    createfullpnIplot(p,n,I)
    plt.savefig(f"plots/p{p}n{n}I{'-'.join(I)}.png")#'tight', transparent=True)

