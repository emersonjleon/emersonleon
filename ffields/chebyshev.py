import math


# T[i] is the T_i Chevyshev polynomial, given by a list of coefficients Tpol,
# where Tpol[i] is the coefficient of x^i of T^i.
T=[[1],[0,1]]

def coeff(Tpol, i):
    if i in range(len(Tpol)):
        return Tpol[i]
    else:
        return 0

def addnew():
    """Recursive formula for Chebyshev polynomials"""
    newlist=[]
    for i in range(len(T[-1])+1):
        newlist.append(2*coeff(T[-1],i-1)-coeff(T[-2],i))
    T.append(newlist)

def init(n):
    for i in range(n-1):
        addnew()

def evalpol(Tpol,x):
    """ Evaluate Tpol at x"""
    total=0
    for k in range(len(Tpol)):
        total+= Tpol[k]*(x**k)
    return total

        
if __name__=="__main__":        
    init(10)
    print(T[10])
    x=0.25
    print(evalpol(T[3],evalpol(T[3],x)))
    print(evalpol(T[9],x))
    
