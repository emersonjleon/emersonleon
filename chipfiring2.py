
xsize=121
ysize=121

def creatematrix(firstvalue=0, xs=xsize, ys=ysize ):
    matrix=[[0]*xs for i in range(ys)]
    xcenter=int((xs+1)/2)
    ycenter=int((ys+1)/2)
    matrix[ycenter][xcenter]=firstvalue
    return matrix


def printmatrix(matrix):
    for line in matrix:
        #print(line)
        #print(type(line))
        for char in line:
            if char==3:
                print(' ', end="")                
            else:
                print(char, end="")
        print("")

#printmatrix(matrix)

def topling(matrix):
    newmatrix=[line[:] for line in matrix]
    stable=True
    for j in range(ysize):
        for i in range(xsize):
            if matrix[i][j]>3:
                stable=False
                residue=matrix[i][j]%4
                add=int(matrix[i][j]/4)
                newmatrix[i][j]=residue
                if i>0:
                    newmatrix[i-1][j]+= add
                if i<xsize-1:
                    newmatrix[i+1][j]+= add
                if j>0:
                    newmatrix[i][j-1]+= add
                if j<ysize-1:
                    newmatrix[i][j+1]+= add
    return newmatrix,stable

def fulltopling(matrix):
    toplimit=1000000
    for counter in range(toplimit):
        newmatrix, stable=topling(matrix)
        if stable==True:
            print(counter)
            return newmatrix
        else:
            matrix=newmatrix
    print("top limit reached:", toplimit)
        
        





if __name__=="__main__":
    for n in range(8):
        value=3*4**n
        print(value)
        matrix=creatematrix(firstvalue=value)
        matrix=fulltopling(matrix)
        printmatrix(matrix)
        #print("")
    
