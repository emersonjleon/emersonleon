def basep(i,p):
    """i is natural number, return a list with i in base p
    where the  value [0] represent the units, [1] times p, 
    and so on"""
    if i%p==i:
        return [i,]
    else:
        ans= basep(((i-(i%p))/p),p)
        ans.append(i%p)
        return ans

def basepton(bp,p):
    """takes a list with basep description of i and return i"""
    if len(bp)==1:
        return bp[0]
    else:
        return int(p*basepton(bp[0:-1],p)+bp[-1])
    

# for i in range(32):
#     bp= basep(i,2)
#     print(bp)
#     print(basepton(bp,2))


def ppi(i,p,n):
    """permutation \pi_{p^n} described in prop. 4.2 pibasep"""
    a=basep(i,p)
    if len(a)<n:
        a=[0]*(n-len(a))+a
    b=[a[0]]
    for k in range(len(a)-1):  
        k=k+1
        if sum(b)%2==0:
            b.append(a[k])
        else:
            b.append(p-1-a[k])
    return basepton(b,p)



def piI(i,p,n,I):
    """permutation \pi_{p^n,I} according to definition in prop. 6.3 pipnI
        This has to be checked in detail!!!!"""
    a=basep(i,p)
    if len(a)<n:
        a=[0]*(n-len(a))+a
    b=[a[0]]
    increase =True
    for k in range(len(a)-1):  
        k=k+1
        if b[-1] not in I:
            increase= not increase 
        if increase==True:
            b.append(a[k])
        else: 
            b.append(p-1-a[k])
    return basepton(b,p)



def test_ppi():
    p=2
    n=4
    for i in range(p**n):
        print((ppi(i,p,n))) 



def test_piI(p,n,I):
    for i in range(p**n):
        print((piI(i,p,n,I)),end=' ') 


# def test_Iconjecture(p,n,I):
#     """we want to check empirically that B_alpha,I is a proper bijection for the fixed points. (p,n,I)"""
#     for i in range(p**n):
#         a=basep(i,p)
#         piIi=piI(i,p,n,I)
#         print i,   basep(i,p), piIi, basep(piIi,p)


def gI(xval,I,p):
    """create a piecewise linear function from [0,1] to [0,1] with increase pattern I and slope +/-1/p (cadlag)"""
    a0= p*xval- p*xval%1
    #print(a0)
    #print(I)
    if xval==1:
        if p-1 in I:
            return 1
        else:
            return 0
    if a0 in I:
        return p*xval%1
    else:
        return 1-p*xval%1

#we need to know the up-down pattern of In. we do it computationally using gI

def intiIncreases(i,I,p,n):
    xstart=i/p**n +  1/p**(n+2)
    #xend=i/p**n  +  (p-1)/p**(n+1)
    for i in range(n):
        xstart=gI(xstart,I,p)
        #xend=gI(xend,I,p)
    if xstart<0.5:
        return True
    else:
        return False

def test_iupdown(p,n,I):
    for i in range(p**n):
        for j in range(p):
            print((piI(i*p+j,p,n,I)),end=' ') 
        print(intiIncreases(i,I,p,n)) 
    
def xiI(i,p,n,I):
    """compute the ith fixed point of gI"""
    if intiIncreases(i,I,p,n):
        return i/(p**n-1)
    else:
        return (i+1)/(p**n+1)

def test_xiI(p,n,I):
    for i in range(p**n):
        print(i,end=":   ")
        xi= xiI(i,p,n,I)
        xval=xi
        for j in range(n):
            print(xval, end=' ')
            xval=gI(xval,I,p)
        print(xval, end=' ')
        print(approxeq(xi,xval)) 

def FPgIn(p,n,I):
    return [xiI(i,p,n,I) for i in range(p**n)]

def approxeq(x0,x1,tol=0.0000000001):
    if (x0-x1)**2<tol:
        return True
    else:
        return False

def findjxj(xj,p,n,I):
    FP=FPgIn(p,n,I)
    for i in range(p**n):
        if approxeq(FP[i],xj):
            return i
    print("Error:   xj not found")



def test_findjxj(p,n,I):
    for xi in FPgIn(p,n,I):
        print(xi,end=": ")
        print(findjxj(xi,p,n,I),end=";   gI(xi) = ")
        xj=gI(xi,I,p)
        print(xj, end=': ')
        print(findjxj(xj,p,n,I)) 

def test_pi2conjecture(p,n,I):
    """old maybe broken..."""
    for i in range(p**n):
        print(i,end=":   ")
        xi= xiI(i,p,n,I)
        xval=xi
        Bi=BijI(i,p,n,I)
        ival=xi
        #for j in range(n):
        #    print(xval, end=' ')
        #    xval=gI(xval,I,p)
        #print(xval)
        for j in range(n):
            print(aval, end='; ')
            aval=aval^p
        print(aval, end=' ')
        print(Bi==aval) 
   

        
def test_Iconjecture(p,n,I):
    FP= FPgIn(p,n,I)
    for i in range(p**n):
        print(i,end=":   ")
        xi= FP[i]
        print(xi, end=' ')
        xval=gI(xi,I,p)
        print(xval)
        for j in range(n):
            print(ival, end=' ')
            ival=piI(ival,p,n,I)
        print(ival, end=' ')
        print(i==ival) 
        
##########################
def finv(k,x):
    """functions f_{(k)}^{-1} evaluated at x"""
    if k%2==0:
        return xtr[k]+(x*(xtr[k+1]-xtr[k]))
    else:
        return xtr[k]+((1-x)*(xtr[k+1]-xtr[k]))

def test_finv():
    for k in range(5):
        for x in [0, .25, .5, .75, 1]:
            print(finv(k,x))
        
        

def h(a):
    """computes the function h of a number given by a finite 
    representation in base p, given in a list a. We assume 
    0<=a[i]<p for all values, and understand that 
    $x=\frac{a_1}{p}+\frac{a_2}{p^2}+\cdots+\frac{a_k}{p^k},$
    (in fact a[0] is ignored)"""
    if len(a)==2:
        return xtr[a[1]]
    else:
        if a[1]%2==0:
            return finv(a[1],h(a[1:]))
        else:
            xp=h([p-1-ak for ak in a[1:-1]]+[p-a[-1]])
            return finv(a[1],xp)

def test_h(k):
    for i in range(p**k):
        print((basep(i+p**k,p), h(basep(i+p**k,p))))

def tikzplot_h(k):
    f = open("tikz/h2.tex", 'w') #puede fallar en windows
    f.write("\draw ")
    for i in range(p**k):
        f.write( "("+ str(float(i)/p**k) +" , "+ str(h(basep(i+p**k,p)))+ ") --\n")
    f.write("(1,1);\n")

def slope_h():
    for k in range(10):
        k=2*k+2
        i=3*(p**k-1)/8+10
        print(( h(basep(i+1+p**k,p)), h(basep(i+p**k,p))))
        print((float(h(basep(i+1+p**k,p))-h(basep(i+p**k,p)) )/p**k))

    


def pcycle(a,p,n):
    """ Create the  cycle of $a$ by multiplying by $p$ modulo $p^n-1$  many times. 
    """
    if a==p**n-1:
        return [a]
    else:
        cycle=[a%(p**n-1)]
        while True:
            new=p*cycle[-1]%(p**n-1)
            if new== cycle[0]:
                break
            else:
                cycle.append(p*cycle[-1]%(p**n-1))
        return cycle

def piIinverse(j,p,n,I):
    """brute force  of the inverse function piI**-1(i)"""
    for i in range(p**n):
        if piI(i,p,n,I)==j:
            return i

def piIinvcycle(cycle,p,n,I):
    return [piIinverse(j,p,n,I) for j in cycle]


def piIcycle(i,p,n,I):
    """ Create the  cycle of $i$ by applying piI  many times.    not useful.... """
    cycle=[i%(p**n-1)]
    while True:
        next=piI(cycle[-1],p,n,I)
        if cycle[0] == next:
            break
        else:
            cycle.append(next)
    return cycle



def pcycles(p,n):
    """ Create a list of all cycles by multiplying a number by $p$ 
    modulo $p^n-1$
    """
    cycles=[]
    
    for i in range(p**n):
        c=pcycle(i,p,n)
        addc=True
        for cycle in cycles:
            #print(c,cycle)
            if c[0] in cycle:
                addc=False
        if addc:
            cycles.append(c)

    return cycles



#############################
if __name__=="__main__":   
    #p=5
    #xtr =[0, 0.1, 0.5, 0.6, 0.95, 1]
    #for i in range(16):
    #    print( pcycle(i,2,4) )

    #####################
    #print(pcycles(2,4))


    #test_h(3)
    #test_finv()
    #test_ppi()
    #tikzplot_h(3)
    #slope_h()
    #print((gI(0.25,[],13)))
    #print((4.0/13))

    I=[2]
    p=3
    n=3
    test_piI(p,n,I)
    #test_iupdown(3,3,[0])
    print("")
    #test_xiI(p,n,[0])
    #test_Iconjecture(3,3,I)
    #test_findjxj(p,n,I)
    for i in range(p**n):
        print(intiIncreases(i,I,p,n))

    
    """
    FPgIn(p, n, I)
    
    approxeq(x0, x1, tol=1e-10)
    
    basep(i, p)
        i is natural number, return a list with i in base p
        where the  value [0] represent the units, [1] times p, 
        and so on
    
    basepton(bp, p)
        takes a list with basep description of i and return i
    
    findjxj(xj, p, n, I)
    
    finv(k, x)
        functions f_{(k)}^{-1} evaluated at x
    
    gI(xval, I, p)
        create a piecewise linear function from [0,1] to [0,1] with increase pattern I and slope +/-1/p (cadlag)
    
    h(a)
        computes the function h of a number given by a finite 
        representation in base p, given in a list a. We assume 
        0<=a[i]<p for all values, and understand that 
        $x=^Lrac{a_1}{p}+^Lrac{a_2}{p^2}+\cdots+^Lrac{a_k}{p^k},$
        (in fact a[0] is ignored)
    
    intiIncreases(i, I, p, n)
    
    pcycle(a, p, n)
        Create the  cycle of $a$ by multiplying by $p$ modulo $p^n-1$  many times.
    
    pcycles(p, n)
        Create a list of all cycles by multiplying a number by $p$ 
        modulo $p^n-1$


   piI(i, p, n, I)
        permutation \pi_{p^n,I} according to definition in prop. 6.3 pipnI
        This has to be checked in detail!!!!
    
    piIcycle(i, p, n, I)
        Create the  cycle of $i$ by applying piI  many times.    not useful....
    
    ppi(i, p, n)
        permutation \pi_{p^n} described in prop. 4.2 pibasep
    
    slope_h()
    
    test_Iconjecture(p, n, I)
    
    test_findjxj(p, n, I)
    
    test_finv()
    
    test_h(k)
    
    test_iupdown(p, n, I)
    
    test_pi2conjecture(p, n, I)
        old maybe broken...
    
    test_piI(p, n, I)
    
    test_ppi()
    
    test_xiI(p, n, I)
    
    tikzplot_h(k)
    
    xiI(i, p, n, I)
        compute the ith fixed point of gI
    """
