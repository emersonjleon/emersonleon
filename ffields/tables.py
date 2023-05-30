import matplotlib.pyplot as plt
import numpy as np
import ff

#pn=24
#I=[0]
#0 1 3 2 6 7 5 4 12 13 15 14 10 11 9 8 
Balpha= {0:   '0',
        1:   'a',
        2:   'a^3',
        3:   'a^2',
        4:   'a^3 + a^2',
        5:   'a^3 + a + 1',
        6:   'a^2 + a',
        7:   'a + 1',
        8:   'a^3 + a^2 + a + 1',
        9:   'a^3 + a^2 + 1',
        10:   '1',
         11:   'a^3 + 1',
         12:   'a^2 + a + 1',
         13:   'a^3 + a^2 + a',
         14:   'a^3 + a',
         15:   'a^2 + 1'}




    


def row(i,p,n,I):
    """ Generates the content of row i consisting on
    i, xi,g(xi), pi(i), B(xi), B(xi)^2, gpn orbit.
    """
    xi=ff.xiI(i,p,n,I)
    gxi=ff.gI(xi,I,p)
    pii=ff.piI(i,p,n,I)
    Ba=Balpha[i]
    return [i, xi, gxi, pii, Ba]

def printvalues(p,n,I):
    for i in range(p**n):
        print(row(i,p,n,I))

def latexrow(rowtuple):
    print(" & ".join([str(item) for item in rowtuple]), "\\\\")

def latextable(p,n,I):
    for i in range(p**n):
        #print(row(i,p,n,I))
        latexrow(row(i,p,n,I))
p =2
n=4
I=[0]

        
latextable(p,n,I)
