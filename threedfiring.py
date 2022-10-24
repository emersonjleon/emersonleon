xsize=45
ysize=xsize
zsize=xsize


def create3dmatrix(firstvalue=0, xsize=xsize, ysize=ysize, zsize=zsize ):
    matrix=[[[0]*zsize for i in range(ysize)] for j in range(xsize)]
    xcenter=int((xsize-1)/2)
    ycenter=int((ysize-1)/2)
    zcenter=int((zsize-1)/2)
    # Entries of a 3d matrix have to be writen in inverse order...
    matrix[zcenter][ycenter][xcenter]=firstvalue
    return matrix


def printmatrix2d(matrix):
    for line in matrix:
        #print(line)
        #print(type(line))
        for char in line:
            if char==0:
                print(' ', end="")                
            else:
                print(char, end="")
        print("")

def printmatrix3d(matrix):
    """print a 3d matrix. z coordinate determine the 2d matrix order, y coordinate the row, x coordinate the column"""
    for m in matrix:
        printmatrix2d(m)
        print("")
    
        
#printmatrix(matrix)

def topling(matrix):
    newmatrix=[[line[:] for line in m] for m in matrix]
    stable=True
    zsize=len(matrix)
    ysize=len(matrix[0])
    xsize=len(matrix[0][0])
    for k in range(zsize):
        for j in range(ysize):
            for i in range(xsize):
                if matrix[k][j][i]>5:
                    stable=False
                    residue=matrix[k][j][i]%6
                    add=int(matrix[k][j][i]/6)
                    newmatrix[k][j][i]=residue
                    if i>0:
                        newmatrix[k][j][i-1]+= add
                    if i < xsize -1:
                        newmatrix[k][j][i+1] += add
                    if j>0:
                        newmatrix[k][j-1][i] += add
                    if j<ysize-1:
                        newmatrix[k][j+1][i] += add
                    if k>0:
                        newmatrix[k-1][j][i] += add
                    if k<zsize-1:
                        newmatrix[k+1][j][i] += add
    return newmatrix,stable

def full3dtopling(matrix):
    toplimit=1000000
    for counter in range(toplimit):
        newmatrix, stable=topling(matrix)
        if stable==True:
            print(counter)
            return newmatrix
        else:
            matrix=newmatrix
    print("top limit reached:", toplimit)
    return newmatrix    
        


def chipfiring3d(value, size=25):
    matrix=create3dmatrix(firstvalue=value,xsize=size, ysize=size, zsize=size)
    matrix=full3dtopling(matrix)
    return matrix

if __name__=="__main__":
    # xsize 25
    for n in range(6):
        value=3*6**n
        print(value)
        printmatrix3d(chipfiring3d(value))
        print("----------------------------")
    
    # value=3*6**6
    # matrix=chipfiring3d(value)
    # printmatrix3d(matrix)
    
