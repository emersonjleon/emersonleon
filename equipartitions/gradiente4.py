from dbm.dumb import error
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import copy
import time, timeit
from scipy.spatial import Voronoi, voronoi_plot_2d
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from matplotlib.path import Path
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#from IPython.display import display, clear_output

# Funión que retorna las coordenadas de un n-agono regular de radio especificado
def agono(m, radio): #m lados, radio= radio del n-agon regular
    A = np.empty((m,2))
    for i in range(m):
        A[i,0]= -radio*np.sin(2*np.pi*i/m)
        A[i,1]= radio*np.cos(2*np.pi*i/m)
    return A

# Función que toma los puntos iniciales (sitios) y un punto cualquiera. Devuelve el índice del punto más
#cercano al punto que se recibe
def punto_mas_cercano(puntos_iniciales, punto, pesos_iniciales):
    c=0
    dist=(puntos_iniciales[0][0]-punto[0])**2+(puntos_iniciales[0][1]-punto[1])**2+pesos_iniciales[0]
    for i in range(0,np.shape(puntos_iniciales)[0],1):
        if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2+pesos_iniciales[i]< dist:
            c=i
            dist = (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2+pesos_iniciales[i]
    return(c) 

# Función que toma los puntos iniciales (sitios) y un punto cualquiera. Devuelve los índices de los puntos más
#cercanos al punto que se recibe. Es una lista y mejora la función anterior. Hay que tener cuidado cuando un punto
# es equidistante a varios
def puntos_mas_cercanos(puntos_iniciales, punto, pesos_iniciales):
    c=0
    v=[]
    dist=(puntos_iniciales[0][0]-punto[0])**2+(puntos_iniciales[0][1]-punto[1])**2+pesos_iniciales[0]
    for i in range(0,np.shape(puntos_iniciales)[0],1):
        if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2+pesos_iniciales[i]< dist:
            c=i
            dist = (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2+pesos_iniciales[i]
    v.append(c)
    for i in range(c+1,np.shape(puntos_iniciales)[0],1):
        if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2+pesos_iniciales[i] == dist:
            v.append(i)        
    return(v) 
       
# Función que toma los puntos iniciales (sitios), otra matriz de puntos y un número de región j y devuelve
# la matrix de puntos restringida a aquellos que están en la región.
def puntos_en_region_n(puntos_iniciales, points,j, pesos_iniciales):
    v=[]
    for i in range(0,np.shape(points)[0]):
        if j in puntos_mas_cercanos(puntos_iniciales, points[i], pesos_iniciales):
            v.append(i)  
    return(v) 

#Estos códigos hallan la intersección de dos segmentos
#y de segmento linea

def segment_segment_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        #print('uA={}, uB={}'.format(uA,uB))
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1 ): 
        return
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
 
    return x, y

def segment_line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2): #line starts in B1 and goes in the direction of B2
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        #print('uA={}, uB={}'.format(uA,uB))
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB  ):  # sin desigualdad para punto vector
        return
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
 
    return x, y   


from numpy.ma.core import sqrt

# Función que retorna dos puntos que definen la recta entre dos puntos pt1 y pt2 con dos pesos l1 y l2
def weighted_ridge(pt1,pt2,l1,l2): #retorna dos puntos que generan la recta que definen los puntos pt1 y pt2 con los pesos l1 y l2
    a=(-l1+l2+(sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2))**2)/(2*(sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)))
    uni=sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)
    ridge=np.array([pt1[0]+a*((pt2[0]-pt1[0])/uni),pt1[1]+a*((pt2[1]-pt1[1])/uni)])
     # los puntos que define el ridge_vertice y ridge vertice
    dir = pt1-pt2
    dir_perp=np.array([dir[1],-dir[0]])
    vertice=ridge+dir_perp
    #plt.scatter(points[:,0],points[:,1])
    #plt.scatter(vertice[0],vertice[1])
    return np.array([ridge,vertice])                                                                               

# Retorna el punto de intersección de las dos líneas line1 y line2 definidas por dos puntos cada una
def vect_intersect(line1,line2): #retorna el punto de intersección de definen las lineas generadas por un par de puntos cada una
  d = (line2[1][1] - line2[0][1]) * (line1[1][0] - line1[0][0]) - (line2[1][0] - line2[0][0]) * (line1[1][1] - line1[0][1])
  if d:
    uA = ((line2[1][0] - line2[0][0]) * (line1[0][1] - line2[0][1]) - (line2[1][1] - line2[0][1]) * (line1[0][0] - line2[0][0])) / d
    uB = ((line1[1][0] - line1[0][0]) * (line1[0][1] - line2[0][1]) - (line1[1][1] - line1[0][1]) * (line1[0][0] - line2[0][0])) / d
    x = line1[0][0] + uA * (line1[1][0] - line1[0][0])
    y = line1[0][1] + uA * (line1[1][1] - line1[0][1])
    return np.array([x, y]) 
  else:
    return 

# retorna la interesección de las tres líneas que definen los tres puntos con los tres pesoss
def triple_intersect(pt1,pt2,pt3,l1,l2,l3): #interesección de las rectas que definen 3 puntos y 3 pesos
  return vect_intersect(weighted_ridge(pt1,pt2,l1,l2),weighted_ridge(pt2,pt3,l2,l3))


#Grafica las regiones de Voronoi. REcibe una lista con los 2d- arrays
# de las regiones.
def graph_regiones(regiones,sitios):
    paleta = cm.get_cmap('nipy_spectral', 8)
    for n in range(0,len(regiones),1):
        plt.scatter(regiones[n][:,0], regiones[n][:,1], c='k')
        for i in range(-1,np.shape(regiones[n])[0]-1,1):
            plt.plot([regiones[n][i][0],regiones[n][i+1][0]],[regiones[n][i][1],regiones[n][i+1][1]],c='blue')
        #plt.fill(regiones[n][:,0],regiones[n][:,1], color=paleta((n+1)/len(regiones)))
        plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5)) 
    plt.scatter(sitios[:,0], sitios[:,1], c='r')    
    plt.show() 

#Grafica las regiones de Voronoi. REcibe una lista con los 2d- arrays
# de las regiones.
def graph_only_regiones(regiones):
    paleta = cm.get_cmap('nipy_spectral', 8)
    for n in range(0,len(regiones),1):
        plt.scatter(regiones[n][:,0], regiones[n][:,1], c='k')
        for i in range(-1,np.shape(regiones[n])[0]-1,1):
            plt.plot([regiones[n][i][0],regiones[n][i+1][0]],[regiones[n][i][1],regiones[n][i+1][1]],c='blue')
        #plt.fill(regiones[n][:,0],regiones[n][:,1], color=paleta((n+1)/len(regiones)))
        #plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5)) 
    #plt.scatter(sitios[:,0], sitios[:,1], c='r')    
    plt.show()     

#Grafica las regiones de Voronoi. REcibe una lista con los 2d- arrays
# de las regiones.
def graph_regiones_filled(regiones,sitios):
    paleta = cm.get_cmap('nipy_spectral', 8)
    for n in range(0,len(regiones),1):
        plt.scatter(regiones[n][:,0], regiones[n][:,1], c='k')
        for i in range(-1,np.shape(regiones[n])[0]-1,1):
            plt.plot([regiones[n][i][0],regiones[n][i+1][0]],[regiones[n][i][1],regiones[n][i+1][1]],c='blue')
        plt.fill(regiones[n][:,0],regiones[n][:,1], color=paleta((n+1)/len(regiones)))
        #plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5)) 
    #plt.scatter(sitios[:,0], sitios[:,1], c='r')    
    plt.show()    

# Devuelve el área de un poligono

def area(R):
    respuesta=0
    region = np.append(R, np.array([R[0]]),  axis=0)
    for i in range(np.shape(R)[0]):
        respuesta = respuesta + (region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])/2
    return respuesta

#Devuelve el centroide de un polígono
def centroide(R):
    centrox=0
    centroy=0
    region = np.append(R, np.array([R[0]]),  axis=0)
    for i in range(np.shape(R)[0]):
        centrox = centrox + (region[i][0]+region[i+1][0])*(region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])
        centroy = centroy + (region[i][1]+region[i+1][1])*(region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])
    areatotal=area(R)
    centrox = centrox/(6*areatotal)
    centroy = centroy/(6*areatotal)
    return np.array([[centrox,centroy]])

#Grafica las regiones de Voronoi. REcibe una lista con los 2d- arrays
# de las regiones. Añade centroides
def graph_regiones_centroides(regiones,sitios):
    paleta = cm.get_cmap('nipy_spectral', 8)
    for n in range(0,len(regiones),1):
        plt.scatter(regiones[n][:,0], regiones[n][:,1], c='k')
        for i in range(-1,np.shape(regiones[n])[0]-1,1):
            plt.plot([regiones[n][i][0],regiones[n][i+1][0]],[regiones[n][i][1],regiones[n][i+1][1]],c='blue')
        #plt.fill(regiones[n][:,0],regiones[n][:,1], color=paleta((n+1)/len(regiones)))
        plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5)) 
        centro = centroide(regiones[n])
        plt.scatter(centro[:,0], centro[:,1], c='g', marker='^')
        #plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5))
    plt.scatter(sitios[:,0], sitios[:,1], c='r')    
    plt.show()     

#Grafica las regiones de Voronoi. REcibe una lista con los 2d- arrays
# de las regiones. Añade centroides
def graph_only_regiones_centroides(regiones):
    paleta = cm.get_cmap('nipy_spectral', 8)
    for n in range(0,len(regiones),1):
        plt.scatter(regiones[n][:,0], regiones[n][:,1], c='k')
        for i in range(-1,np.shape(regiones[n])[0]-1,1):
            plt.plot([regiones[n][i][0],regiones[n][i+1][0]],[regiones[n][i][1],regiones[n][i+1][1]],c='blue')
        #plt.fill(regiones[n][:,0],regiones[n][:,1], color=paleta((n+1)/len(regiones)))
        #plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5)) 
        centro = centroide(regiones[n])
        plt.annotate("{}".format(n), (centro[0][0],centro[0][1]), textcoords="offset points", xytext=(0,5))
        plt.scatter(centro[:,0], centro[:,1], c='g', marker='^')
        #plt.annotate("{}".format(n), (sitios[n][0],sitios[n][1]), textcoords="offset points", xytext=(0,5))
    #plt.scatter(sitios[:,0], sitios[:,1], c='r')    
    plt.show() 

# Función que define los diagramas de Voronoi con pesos. 
def weight_dist(punto,sitio,peso):
  value = -2*(punto[0]*sitio[0]+punto[1]*sitio[1]) +sitio[0]**2 + sitio[1]**2 + peso
  return value

# Función que retorna el diagrama de VORONOI CON PESOS de unos sitios iniciales y unos pesos iniciales
# Sitios es np.array de (n,2) y pesos es un array de n.
# Retorna vertices (intersección de las líneas del diagrama de Voronoi) np.array de puntos
# regiones: lista de lista de vértices de cada región
# ridge_vertices: lista de aristas, con la información de los puntos que definen la arista. Comienza con -1 si la arista es aboerta.
# ridge_points: lista de parejas de puntos (sitios) que definen las aristas.
def weighted_voronoi(sitios,pesos):  #retorna: vertices en array(n,2), regiones (lista de listas con el número de fila de sus resp vertices), ridge_vertices (indices de los vertices que definen frontera), ridge_points (indices de sitios que definen el ridge)
    lista=[]
    length_sitios=len(sitios)
    for i in range (0,length_sitios-2,1):
      for j in range (i+1,length_sitios-1,1):
        for k in range (j+1,length_sitios,1): #para cada tripla de indices, hallamos el punto de intersección de las rectas
          interseccion= triple_intersect(sitios[i],sitios[j],sitios[k],pesos[i],pesos[j],pesos[k])
          if length_sitios==3:
            #if poligon_path.contains_point(interseccion) == True:
            lista.append([i,j,k,interseccion])
          else: 
            new_sitios=np.delete(sitios,[i,j,k],0)
            new_pesos=np.delete(pesos,[i,j,k],0)  
            w=True 
            value = weight_dist(interseccion, sitios[i], pesos[i])
            for q in range(len(new_sitios)):
              w=w*(value < weight_dist(interseccion, new_sitios[q],new_pesos[q]))
            if w==True:
              lista.append([i,j,k,interseccion])
            #value = -2*(interseccion[0]*sitios[i][0]+interseccion[1]*sitios[i][1])+sitios[i][0]**2+sitios[i][1]**2+pesos[i]
            #while (value <= -2*(interseccion[0]*new_sitios[w][0]+interseccion[1]*new_sitios[w][1])+new_sitios[w][0]**2+new_sitios[w][1]**2+pesos[w])&(w<length_sitios-4):
            #while (value < weight_dist(interseccion, new_sitios[w],pesos[w]))&(w<length_sitios-4):
            #  w=w+1  
            #if ((value < weight_dist(interseccion, new_sitios[w],pesos[w]))&(w==length_sitios-4)):
            #if value <= -2*(interseccion[0]*new_sitios[w][0]+interseccion[1]*new_sitios[w][1])+new_sitios[w][0]**2+new_sitios[w][1]**2+pesos[w]:
              #if poligon_path.contains_point(interseccion) == True:
            #  lista.append([i,j,k,interseccion])  #añadimos indices y punto de intersección
    df = pd.DataFrame(lista, columns=['l','m','n','inter']) #convertimos en dataframe indices e intersecciones
    vertices = np.vstack(df['inter'])
    regiones = [ [] for i in range(len(sitios))]
    ridge_vertices=[]
    ridge_points=np.empty([0,2], dtype=np.int32)
    for i in range(0,len(sitios),1):
      regiones[i] = df[(df['l']==i)|(df['m']==i)|(df['n']==i)].index.to_list() #vertices de cada región, numerados por su fila en la matriz de vértices
      for j in range(0,len(sitios),1):
        data=df[((df['l']==i)&(df['m']==j))|((df['l']==i)&(df['n']==j))|((df['m']==i)&(df['n']==j))]
        if len(data)==1:
          ridge_vertices.append([-1,data.index[0]])  #ridge abierto en una dirección
          ridge_points = np.vstack((ridge_points, np.array([[i,j]]))) #sitios que definen el ridge
        elif len(data)==2:
          ridge_vertices.append([data.index[0],data.index[1]])   #ridge cerrado de dos interesecciones
          ridge_points = np.vstack((ridge_points, np.array([[i,j]]))) #sitios que definen el ridge
    return vertices, regiones, ridge_vertices,ridge_points #en 0 devuelve vertices, en 1 devuelve points  



# Para cada región (numeradas por el índice del punto que define la región de Voronoi con pesos,
# se toman los vértices del diagrama de Voronoi (intersecciones), y se añaden los puntos de la región externa
# que están en esa región (puntos de menor distancia con pesos). Posteriormente se añaden
# los puntos de intersección de aristas del diagrama de Voronoi con los puntos de intersección
# con las aristas de la región externa.

def particion_wv(poligono, sitios, pesos):
    number_of_regions = np.shape(sitios)[0]
    #pesos=np.array([0,10,0,0,0,0])
    vertices_wv, regiones_wv, ridge_vertices_wv, ridge_points_wv = weighted_voronoi(sitios,pesos)  #(vor.vertices)
    regiones=[]
    for i in range(0,number_of_regions,1):
        list= regiones_wv[i].copy()  #La indexación de las regiones la dan los sitios (puntos originales). Hay que corregir porque en Voronoi salen otros.  
        vert = vertices_wv[list].copy()
        rows_to_remove=[]  
        for j in range(0,np.shape(vert)[0],1):  # Aquí se quitan los puntos de cada región que están por fuera de la región acotada
            if poligon_path.contains_point(vert[j]) == False:
                rows_to_remove.append(j)
        vert=np.delete(vert,rows_to_remove,0)
        a =  np.vstack((vert,poligono[puntos_en_region_n(sitios,poligono,i,pesos)]))
        regiones.append(a)
        
    for row, side in enumerate(ridge_vertices_wv): #se hace un loop sobre las líneas que forman el diagrama de Voronoi
        if side[0]!=-1:   #aquí se escogen las líneas del diagrama de Voronoi que son acotadas. Estás no tienen -1 en la primera coordenada
            v1x = vertices_wv[side[0]][0]  #vértice 1 del segmento
            v1y = vertices_wv[side[0]][1]
            v2x = vertices_wv[side[1]][0]  #vértice 2 del segmento
            v2y = vertices_wv[side[1]][1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]   #vértice 1 del lado de la región externa
                w1y = poligono[j][1]
                w2x = poligono[j+1][0]   #vértice 2 del lado de la región externa
                w2y = poligono[j+1][1]
                if segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y) != None:
                    x , y = segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y)  #punto de intersección
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = ridge_points_wv[row][0]  #el punto se le añade a las regiones con frontera el segmento
                    region_2_to_add = ridge_points_wv[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))
                    #plt.plot(new_intersection[0][0], new_intersection[0][1], marker="o", markersize=10, markeredgecolor="black", markerfacecolor="magenta")
            #plt.plot([v1x,v2x],[v1y,v2y], c='r')  #Segment line between to vertices
        else:
            vertex = vertices_wv[side[1]]   # Vértice del diagrama de Voronoi de donde sale una línea no acotada
            point_1= ridge_points_wv[row][0]  #puntos más cercanos al vértice cuya línea equidistante a estos dos puntos definen la línea no acotada del diagrama de Voronoi
            point_2= ridge_points_wv[row][1]
            normal = sitios[point_1]-sitios[point_2]   #vector normal a la línea no acotada. 
            dir = np.array([normal[1],-normal[0]])            #Perpendicular al vector que une a los dos puntos
            sitios_sin = np.delete(sitios,[point_1, point_2],axis=0)  #Se le quitan los dos puntos para poder ubicar el tecero más cercano (en los vértices hay tres puntos equidistantes)
            pesos_sin = np.delete(pesos,[point_1, point_2],axis=0)
            cercano= punto_mas_cercano(sitios_sin,vertex,pesos_sin)  #se usa la función punto más cercano pero...
            if cercano>=min(point_1,point_2):
                cercano = cercano+1                       # al quitar los dos puntos que definen la línea se mueven las filas. Hay que corregir este error. Son los dos if
            if cercano>=max(point_1,point_2):
                cercano = cercano+1
            #print('vertice = {}, puntos = {}, {}, punto cercano = {}, dir = {}'.format(side[1], point_1, point_2,cercano, dir))
            if weight_dist(vertex+dir, sitios[cercano], pesos[cercano]) < weight_dist(vertex+dir, sitios[point_1], pesos[point_1]):
            #if -2*((vertex+dir)[0]*sitios[cercano][0]+(vertex+dir)[1]*sitios[cercano][1])+sitios[cercano][0]**2+sitios[cercano][1]**2+pesos[cercano] < -2*((vertex+dir)[0]*sitios[point_1][0]+(vertex+dir)[1]*sitios[point_1][1])+sitios[point_1][0]**2+sitios[point_1][1]**2+pesos[point_1]:
                dir = -dir
            v1x = vertex[0]
            v1y = vertex[1]
            v2x = (vertex+dir)[0]
            v2y = (vertex+dir)[1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]
                w1y = poligono[j][1]
                w2x = poligono[j+1][0]
                w2y = poligono[j+1][1]
                if segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y) != None:
                    x , y = segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y)
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = ridge_points_wv[row][0]
                    region_2_to_add = ridge_points_wv[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))
                    #plt.plot(new_intersection[0][0], new_intersection[0][1], marker="o", markersize=10, markeredgecolor="black", markerfacecolor="magenta")
            #plt.plot([vertex[0],(vertex+dir)[0]],[vertex[1], (vertex+dir)[1]],c='r', linestyle='--')   #pinta la recta que sale del vértice sin ser acotado
        
    #plt.scatter(vertices_wv[:,0], vertices_wv[:,1], c='k')
    #plt.scatter(sitios[:,0], sitios[:,1], c='b')
    #plt.scatter(poligono[:,0], poligono[:,1], c='red')
    #for i in range(0,(np.shape(sitios)[0]),1):
    #    label = "{}".format(i)
    #    plt.annotate(label, (sitios[i][0],sitios[i][1]), textcoords="offset points", xytext=(0,5)) 
    #for i in range(0,(np.shape(poligono)[0]),1):
    #    label = "{}".format(i)
    #    plt.annotate(label, (poligono[i][0],poligono[i][1]), textcoords="offset points", xytext=(0,5))     
    #for i in range(0,(np.shape(vertices_wv)[0]),1):
    #    label = "{}".format(i)
    #    plt.annotate(label, (vertices_wv[i][0],vertices_wv[i][1]), textcoords="offset points", xytext=(0,5))     
    #plt.plot(punto[0], punto[1], marker="o", markersize=10, markeredgecolor="yellow", markerfacecolor="green")
    #for simplex in poligon.simplices:
    #    plt.plot([poligon.points[simplex][0][0],poligon.points[simplex][1][0]],[poligon.points[simplex][0][1],poligon.points[simplex][1][1]], c='g' )
    #plt.show()
    areas=[]
    perimetros=[]
    for n in range(0,len(regiones),1):
        if len(regiones[n].tolist()) != 0:
            zona = ConvexHull(regiones[n])
            regiones[n] = zona.points[zona.vertices]
            areas.append(zona.volume)
            perimetros.append(zona.area)
        else:
            areas.append(0)
            perimetros.append(0)    
    lista_respuesta = []    
    lista_respuesta.append(regiones)
    lista_respuesta.append(np.asarray(areas))
    lista_respuesta.append(np.asarray(perimetros))
    # Lista de respuesta. Devuelve en [0] las regiones, en [1] las areas, en [2] los perimetros
    return lista_respuesta #




#-----------------------------------------------

#Función que retorna np.array de vertices en el interior del polígono,
#con lista de listas, cada una con los vertices del interior de la región específica.
def internal_vertices_wv(poligono,sitios,pesos):  #retorna: vertices en array(n,2), regiones (lista de listas con el número de fila de sus resp vertices),
    lista=[]
    length_sitios=len(sitios)
    for i in range (0,length_sitios-2,1):
      for j in range (i+1,length_sitios-1,1):
        for k in range (j+1,length_sitios,1): #para cada tripla de indices, hallamos el punto de intersección de las rectas
          interseccion= triple_intersect(sitios[i],sitios[j],sitios[k],pesos[i],pesos[j],pesos[k])
          if poligon_path.contains_point(interseccion) == True: #se revisa si el punto está en el interior
            if length_sitios==3:
              #if poligon_path.contains_point(interseccion) == True:
              lista.append([i,j,k,interseccion])
            else: 
              new_sitios=np.delete(sitios,[i,j,k],0)
              new_pesos=np.delete(pesos,[i,j,k],0)  
              w=True 
              value = weight_dist(interseccion, sitios[i], pesos[i])
              for q in range(len(new_sitios)):
                w=w*(value < weight_dist(interseccion, new_sitios[q],new_pesos[q]))
              if w==True:
                lista.append([i,j,k,interseccion])
    df = pd.DataFrame(lista, columns=['l','m','n','inter']) #convertimos en dataframe indices e intersecciones
    vertices = np.vstack(df['inter'])
    regiones = [ [] for i in range(len(sitios))]
    ridge_vertices=[]
    ridge_points=np.empty([0,2], dtype=np.int32)
    for i in range(0,len(sitios),1):
      regiones[i] = df[(df['l']==i)|(df['m']==i)|(df['n']==i)].index.to_list() #vertices de cada región, numerados por su fila en la matriz de vértices  
    return vertices, regiones #en 0 devuelve vertices internos, en 1 devuelve lista, con lista de puntos de cada región  






#-------------------------------------------

# Retorna sitios (vértices externos) y por cada región el índice de los vértices externos que le correspondden

def external_vertices_wv(poligono, sitios, pesos):
    number_of_regions = np.shape(sitios)[0]
    regiones=[]
    for i in range(0,number_of_regions,1):
        regiones.append(puntos_en_region_n(sitios,poligono,i,pesos))
    return poligono, regiones

#------------------------------------------------------------------------------

# Se retornan los vértices que provienen de la intersección de las aristas del diagrama de voronoi 
# con el polígono. Se retorna el array de vertices, la lista de regiones con su listado de vertices por cada región
# y por cada vértice se definen los dos índices de los vertíces de polígono donde cae.

def intermediate_vertices_wv(poligono, sitios, pesos):
    number_of_regions = np.shape(sitios)[0]
    #pesos=np.array([0,10,0,0,0,0])
    vertices_wv, regiones_wv, ridge_vertices_wv, ridge_points_wv = weighted_voronoi(sitios,pesos)  #(vor.vertices)
    regiones=[]
    for i in range(0,number_of_regions,1):
        list= regiones_wv[i].copy()  #La indexación de las regiones la dan los sitios (puntos originales). Hay que corregir porque en Voronoi salen otros.  
        vert = vertices_wv[list].copy()
        rows_to_remove=[]  
        for j in range(0,np.shape(vert)[0],1):  # Aquí se quitan los puntos de cada región que están por fuera de la región acotada
            if poligon_path.contains_point(vert[j]) == False:
                rows_to_remove.append(j)
        vert=np.delete(vert,rows_to_remove,0)
        a =  np.vstack((vert,poligono[puntos_en_region_n(sitios,poligono,i,pesos)]))
        regiones.append(a)

    intermediate_vertices=np.empty((0,2))
    regiones_intermediate=[ [] for i in range(len(sitios))]
    sides_intermediate=[]
    count=0
    for row, side in enumerate(ridge_vertices_wv): #se hace un loop sobre las líneas que forman el diagrama de Voronoi
        if side[0]!=-1:   #aquí se escogen las líneas del diagrama de Voronoi que son acotadas. Estás no tienen -1 en la primera coordenada
            v1x = vertices_wv[side[0]][0]  #vértice 1 del segmento
            v1y = vertices_wv[side[0]][1]
            v2x = vertices_wv[side[1]][0]  #vértice 2 del segmento
            v2y = vertices_wv[side[1]][1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]   #vértice 1 del lado de la región externa
                w1y = poligono[j][1]
                w2x = poligono[j+1][0]   #vértice 2 del lado de la región externa
                w2y = poligono[j+1][1]
                if segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y) != None:
                    x , y = segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y)  #punto de intersección
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = ridge_points_wv[row][0]  #el punto se le añade a las regiones con frontera el segmento
                    region_2_to_add = ridge_points_wv[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))
                    
                    intermediate_vertices = np.append(intermediate_vertices, new_intersection,axis=0)
                    regiones_intermediate[region_1_to_add].append(count)
                    regiones_intermediate[region_2_to_add].append(count)
                    sides_intermediate.append([j,j+1])
                    count=count+1

                    #plt.plot(new_intersection[0][0], new_intersection[0][1], marker="o", markersize=10, markeredgecolor="black", markerfacecolor="magenta")
            #plt.plot([v1x,v2x],[v1y,v2y], c='r')  #Segment line between to vertices
        else:
            vertex = vertices_wv[side[1]]   # Vértice del diagrama de Voronoi de donde sale una línea no acotada
            point_1= ridge_points_wv[row][0]  #puntos más cercanos al vértice cuya línea equidistante a estos dos puntos definen la línea no acotada del diagrama de Voronoi
            point_2= ridge_points_wv[row][1]
            normal = sitios[point_1]-sitios[point_2]   #vector normal a la línea no acotada. 
            dir = np.array([normal[1],-normal[0]])            #Perpendicular al vector que une a los dos puntos
            sitios_sin = np.delete(sitios,[point_1, point_2],axis=0)  #Se le quitan los dos puntos para poder ubicar el tecero más cercano (en los vértices hay tres puntos equidistantes)
            pesos_sin = np.delete(pesos,[point_1, point_2],axis=0)
            cercano= punto_mas_cercano(sitios_sin,vertex,pesos_sin)  #se usa la función punto más cercano pero...
            if cercano>=min(point_1,point_2):
                cercano = cercano+1                       # al quitar los dos puntos que definen la línea se mueven las filas. Hay que corregir este error. Son los dos if
            if cercano>=max(point_1,point_2):
                cercano = cercano+1
            #print('vertice = {}, puntos = {}, {}, punto cercano = {}, dir = {}'.format(side[1], point_1, point_2,cercano, dir))
            if weight_dist(vertex+dir, sitios[cercano], pesos[cercano]) < weight_dist(vertex+dir, sitios[point_1], pesos[point_1]):
            #if -2*((vertex+dir)[0]*sitios[cercano][0]+(vertex+dir)[1]*sitios[cercano][1])+sitios[cercano][0]**2+sitios[cercano][1]**2+pesos[cercano] < -2*((vertex+dir)[0]*sitios[point_1][0]+(vertex+dir)[1]*sitios[point_1][1])+sitios[point_1][0]**2+sitios[point_1][1]**2+pesos[point_1]:
                dir = -dir
            v1x = vertex[0]
            v1y = vertex[1]
            v2x = (vertex+dir)[0]
            v2y = (vertex+dir)[1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]
                w1y = poligono[j][1]
                w2x = poligono[j+1][0]
                w2y = poligono[j+1][1]
                if segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y) != None:
                    x , y = segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y)
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = ridge_points_wv[row][0]
                    region_2_to_add = ridge_points_wv[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))

                    intermediate_vertices = np.append(intermediate_vertices, new_intersection,axis=0)
                    regiones_intermediate[region_1_to_add].append(count)
                    regiones_intermediate[region_2_to_add].append(count)
                    sides_intermediate.append([j,j+1])
                    count=count+1
    
    return intermediate_vertices, regiones_intermediate, sides_intermediate
    #return lista_respuesta #


#------------------------------------------------------------------

#Partición recibiendo los vértices externos, intermedios e internos
#DEvuelve las regiones, las áreas y los perímetros
#Lo que recibe debe provenir de un diagrama de Voronoi con pesos.
# Las funciones que retornan la información que se puede poner al inicio son:
#external_vertices_wv(poligono, sitios, pesos)
#intermediate_vertices_wv(poligono, sitios, pesos)
#internal_vertices_wv(poligono, sitios, pesos)

def particion_vertices(external, intermediate, internal):
    regiones=[]
    areas=[]
    perimetros=[]
    #convex=[]
    #todos_convexos=True
    for n in range(0,len(external[1]),1):
        a=np.empty((0,2))
        a = np.append(a, external[0][external[1][n]],axis=0)
        a = np.append(a, intermediate[0][intermediate[1][n]],axis=0)
        a = np.append(a, internal[0][internal[1][n]],axis=0)
        size = np.shape(a)[0]
        if size != 0:
            zona = ConvexHull(a)
            a = zona.points[zona.vertices]
            #if np.shape(a)[0] < size:
            #    convex.append(False)
            #    todos_convexos=False
            #else:    
            #    convex.append(True)
            regiones.append(a)
            areas.append(zona.volume)
            perimetros.append(zona.area)
        else:
            regiones.append([])
            areas.append(0)
            perimetros.append(0) 
            #convex.append(True)

    lista_respuesta = []    
    lista_respuesta.append(regiones)
    lista_respuesta.append(np.asarray(areas))
    lista_respuesta.append(np.asarray(perimetros))
    #lista_respuesta.append(convex)
    #lista_respuesta.append(todos_convexos)
    return lista_respuesta

#-----------------------------------------------------

# FUnción a optimizar. DIstancia al vector de áreas promedio por un peso,
# más distancia al perímetro promedio, por un peso.
# SI los pesos se inicializan en 1 y 1 es sencillamente la suma  de las distancias
# a las áreas y perímetros promedio.
def optimizador(areas,perimetros,peso_areas,peso_perimetros):
    #dist_areas = np.linalg.norm(areas - areas.mean())
    #dist_perimetros = np.linalg.norm(perimetros - perimetros.mean())
    areas_mean = area_del_poligono/(len(areas))
    perimetros_mean = perimetros.mean()
    #dist_areas = sum((areas/areas_mean - 1)**2)
    #dist_perimetros=sum((perimetros/perimetros_mean - 1)**2)
    dist_areas = sum((areas-areas_mean)**2)
    dist_perimetros=sum((perimetros-perimetros_mean)**2)
    #dist_areas = sum(abs(areas - areas.mean()))/areas.mean()
    #dist_perimetros=sum(abs(perimetros - perimetros.mean()))/perimetros.mean()
    return dist_areas*peso_areas + dist_perimetros*peso_perimetros

def optimizador_areas(areas,perimetros,peso_areas,peso_perimetros):
    areas_mean = area_del_poligono/(len(areas))
    perimetros_mean = perimetros.mean()
    dist_areas = sum(np.abs((areas-areas_mean)))
    #dist_perimetros=sum((perimetros/perimetros_mean - 1)**2)
    return dist_areas*peso_areas

def f_wv(poligono,sites,weights):
    part = particion_wv(poligono,sites,weights)
    return optimizador(part[1],part[2],1,1)

def f_wv_areas(poligono,sites,weights):
    part = particion_wv(poligono,sites,weights)
    return optimizador_areas(part[1],part[2],1,0)    

def grad_f_wv(poligono, sitios, pesos, delta):
    grad_sitios = np.empty((0,2))
    grad_pesos = np.empty(0)
    value = f_wv(poligono, sitios, pesos)
    for row in range(0,np.shape(sitios)[0],1):
        base_x = np.zeros(np.shape(sitios))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(sitios))
        base_y[row] = np.array([0,1])
        base_p = np.zeros(np.shape(pesos))
        base_p[row] = 1
        cambio_x = (f_wv(poligono, sitios+base_x*delta, pesos)- value)/delta
        cambio_y = (f_wv(poligono, sitios+base_y*delta, pesos)-value)/delta
        cambio_p = (f_wv(poligono, sitios, pesos+base_p*delta)-value)/delta
        grad_sitios = np.append(grad_sitios, np.array([[cambio_x,cambio_y]]),axis=0)
        grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return [grad_sitios, grad_pesos] #Retorna el gradiente en sitios y el gradiente en pesos 



def grad_f_wv_areas_pesos(poligono, sitios, pesos, delta):
    #grad_sitios = np.empty((0,2))
    grad_pesos = np.empty(0)
    part=particion_wv(poligono, sitios, pesos)
    value = optimizador_areas(part[1],part[2],1,0)
    for row in range(0,np.shape(sitios)[0],1):
        #base_x = np.zeros(np.shape(sitios))
        #base_x[row] = np.array([1,0])
        #base_y = np.zeros(np.shape(sitios))
        #base_y[row] = np.array([0,1])
        base_p = np.zeros(np.shape(pesos))
        base_p[row] = 1
        #cambio_x = (f_wv(poligono, sitios+base_x*delta, pesos)- value)/delta
        #cambio_y = (f_wv(poligono, sitios+base_y*delta, pesos)-value)/delta
        part_delta=particion_wv(poligono, sitios, pesos+base_p*delta)
        value_delta = optimizador_areas(part_delta[1],part_delta[2],1,0)
        cambio_p = (value_delta-value)/delta
        #grad_sitios = np.append(grad_sitios, np.array([[cambio_x,cambio_y]]),axis=0)
        grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return [grad_pesos] #Retorna el gradiente en sitios y el gradiente en pesos 

#Gradiente de los puntos internos del diagrama de Voronoi
#

def grad_part_vert_internal(external, intermediate, internal, delta):
    grad_internal = np.empty((0,2))
    #grad_pesos = np.empty(0)
    particion=particion_vertices(external,intermediate,internal)
    value = optimizador(particion[1],particion[2],1,1) 
    for row in range(0,np.shape(internal[0])[0],1):
        base_x = np.zeros(np.shape(internal[0]))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(internal[0]))
        base_y[row] = np.array([0,1])
        #base_p = np.zeros(np.shape(pesos))
        #base_p[row] = 1
        internal_new_x=[]
        internal_new_x.append(internal[0]+base_x*delta)
        internal_new_x.append(internal[1])
        particion_new_x=particion_vertices(external,intermediate,internal_new_x)
        value_new_x = optimizador(particion_new_x[1],particion_new_x[2],1,1) 
        cambio_x = (value_new_x- value)/delta
        internal_new_y=[]
        internal_new_y.append(internal[0]+base_y*delta)
        internal_new_y.append(internal[1])
        particion_new_y=particion_vertices(external,intermediate,internal_new_y)
        value_new_y = optimizador(particion_new_y[1],particion_new_y[2],1,1) 
        cambio_y = (value_new_y- value)/delta
        grad_internal = np.append(grad_internal, np.array([[cambio_x,cambio_y]]),axis=0)
        #grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return grad_internal #Retorna el gradiente en sitios y el gradiente en pesos

#Gradiente de los puntos intermedios en el diagrama de voronoi. 
#El gradiente es la dirección en que se pueden mover, es decir en el lado en que están,
#multiplicado por la derivada direccional

def grad_part_vert_intermediate(external, intermediate, internal, delta):
    grad_intermediate = np.empty((0,2))
    #grad_pesos = np.empty(0)
    particion=particion_vertices(external,intermediate,internal)
    value = optimizador(particion[1],particion[2],1,1) + 1*(sum(particion[1])-area_del_poligono)**2
    for row in range(0,np.shape(intermediate[0])[0],1):
        inicio=external[0][intermediate[2][row][0]] #primer vértice del lado del polígono donde el cruce está
        final=external[0][intermediate[2][row][1]]  #segundo vértice del del lado del polígono
        dir=(final-inicio)/np.linalg.norm(final-inicio) #dirección unitaria de movimiento, paralelo al lado
        base = np.zeros(np.shape(intermediate[0]))  # array donde sólo se mueve el punto row
        base[row] = dir
        intermediate_new=[]
        intermediate_new.append(intermediate[0]+base*delta)
        intermediate_new.append(intermediate[1])
        intermediate_new.append(intermediate[2])
        particion_new=particion_vertices(external,intermediate_new,internal)
        value_new = optimizador(particion_new[1],particion_new[2],1,1) + 1*(sum(particion_new[1])-area_del_poligono)**2
        cambio = (value_new- value)/delta
        grad_intermediate = np.append(grad_intermediate, np.array([dir])*cambio,axis=0)
        #grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return grad_intermediate #Retorna el gradiente de las coordenadas intermedias. solo en la dirección apropiada


#___________ gradientes de la función punishment (fuera de la región convexa)

def grad_part_vert_internal_extra(external, intermediate, internal, delta):
    grad_internal = np.empty((0,2))
    #grad_pesos = np.empty(0)
    particion=particion_vertices(external,intermediate,internal)
    value = (sum(particion[1])-area_del_poligono)**2
    for row in range(0,np.shape(internal[0])[0],1):
        base_x = np.zeros(np.shape(internal[0]))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(internal[0]))
        base_y[row] = np.array([0,1])
        #base_p = np.zeros(np.shape(pesos))
        #base_p[row] = 1
        internal_new_x=[]
        internal_new_x.append(internal[0]+base_x*delta)
        internal_new_x.append(internal[1])
        particion_new_x=particion_vertices(external,intermediate,internal_new_x)
        value_new_x = 1*(sum(particion_new_x[1])-area_del_poligono)**2
        cambio_x = (value_new_x- value)/delta
        internal_new_y=[]
        internal_new_y.append(internal[0]+base_y*delta)
        internal_new_y.append(internal[1])
        particion_new_y=particion_vertices(external,intermediate,internal_new_y)
        value_new_y = 1*(sum(particion_new_y[1])-area_del_poligono)**2
        cambio_y = (value_new_y- value)/delta
        grad_internal = np.append(grad_internal, np.array([[cambio_x,cambio_y]]),axis=0)
        #grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return grad_internal #Retorna el gradiente en sitios y el gradiente en pesos

#Gradiente de los puntos intermedios en el diagrama de voronoi. 
#El gradiente es la dirección en que se pueden mover, es decir en el lado en que están,
#multiplicado por la derivada direccional

def grad_part_vert_intermediate_extra(external, intermediate, internal, delta):
    grad_intermediate = np.empty((0,2))
    #grad_pesos = np.empty(0)
    particion=particion_vertices(external,intermediate,internal)
    value =  1*(sum(particion[1])-area_del_poligono)**2
    for row in range(0,np.shape(intermediate[0])[0],1):
        inicio=external[0][intermediate[2][row][0]] #primer vértice del lado del polígono donde el cruce está
        final=external[0][intermediate[2][row][1]]  #segundo vértice del del lado del polígono
        dir=(final-inicio)/np.linalg.norm(final-inicio) #dirección unitaria de movimiento, paralelo al lado
        base = np.zeros(np.shape(intermediate[0]))  # array donde sólo se mueve el punto row
        base[row] = dir
        intermediate_new=[]
        intermediate_new.append(intermediate[0]+base*delta)
        intermediate_new.append(intermediate[1])
        intermediate_new.append(intermediate[2])
        particion_new=particion_vertices(external,intermediate_new,internal)
        value_new = 1*(sum(particion_new[1])-area_del_poligono)**2
        cambio = (value_new- value)/delta
        grad_intermediate = np.append(grad_intermediate, np.array([dir])*cambio,axis=0)
        #grad_pesos = np.append(grad_pesos, np.array([cambio_p]),axis=0)
    return grad_intermediate #Retorna el gradiente de las coordenadas intermedias. solo en la dirección apropiada







# FUnción que retorna las áreas (menos el promedio) y los perímetros (menos el promedio)
# Lo que uno busca entonnces es exactamente los ceros de esta función vectorial
def F(poligono,X):
    n=len(X)
    n=int(n/3)
    sitios = X[0:2*n].reshape(n,2)
    pesos = X[2*n:3*n].transpose()[0,:]
    part=particion_wv(poligono,sitios,pesos)
    a = part[1]-part[1].mean()
    b = part[2]-part[2].mean()
    return np.array([np.append(a,b)]).transpose()

def Jac_F(poligono,X,delta):
    b = F(poligono,X)
    n = np.size(X)
    m = np.size(b)
    jac = np.empty((m,0))
    for column in range(0,n,1):
        base = np.zeros(n)
        base[column] = 1
        base = np.array([base]).transpose()
        cambio = (F(poligono, X+base*delta)-F(poligono, X))/delta
        jac = np.append(jac,cambio,axis=1)
    return jac

#---------------------------------------------------------------

#----------------------------------------------------------------

#X = np.array([np.append(sitios.flatten(),pesos,axis=0)]).transpose()  
# Función que toma los puntos iniciales (sitios) y un punto cualquiera. Devuelve el índice del punto más
#cercano al punto que se recibe
def punto_mas_cercano_sin_pesos(puntos_iniciales, punto):
    c=0
    dist=np.linalg.norm(puntos_iniciales[0]-punto)
    for i in range(0,np.shape(puntos_iniciales)[0],1):
        if np.linalg.norm(puntos_iniciales[i]-punto)< dist:
            c=i
            dist = np.linalg.norm(puntos_iniciales[i]-punto)
    return(c)      

# Función que toma los puntos iniciales (sitios) y un punto cualquiera. Devuelve los índices de los puntos más
#cercanos al punto que se recibe. Es una lista y mejora la función anterior. Hay que tener cuidado cuando un punto
# es equidistante a varios
def puntos_mas_cercanos_sin_pesos(puntos_iniciales, punto):
    c=0
    v=[]
    dist=np.linalg.norm(puntos_iniciales[0]-punto)
    for i in range(0,np.shape(puntos_iniciales)[0],1):
        if np.linalg.norm(puntos_iniciales[i]-punto)< dist:
            c=i
            dist = np.linalg.norm(puntos_iniciales[i]-punto)
    v.append(c)
    for i in range(c+1,np.shape(puntos_iniciales)[0],1):
        if np.linalg.norm(puntos_iniciales[i]-punto) == dist:
            v.append(i)        
    return(v) 


# Función que toma los puntos iniciales (sitios), otra matriz de puntos y un número de región j y devuelve
# la matrix de puntos restringida a aquellos que están en la región.
def puntos_en_region_n_sin_pesos(puntos_iniciales, points,j):
    v=[]
    for i in range(0,np.shape(points)[0]):
        if j in puntos_mas_cercanos_sin_pesos(puntos_iniciales, points[i]):
            v.append(i)  
    return(v)        

#Estos códigos hallan la intersección de dos segmentos
#y de segmento linea

# Para cada región (numeradas por el índice del punto que define la región de Voronoi
# se toman los vértices del diagrama de Voronoi, y se añaden los puntos de la región externa
# que están en esa región (puntos de menor distancia). Faltan
# los puntos de intersección de aristas del diagrama de Voronoi con los puntos de intersección
# con las aristas de la región externa.
def particion(poligono, sitios):
    number_of_regions = np.shape(sitios)[0]
    vor = Voronoi(sitios, furthest_site=False)
    regiones=[]
    for i in range(0,number_of_regions,1):
        list= vor.regions[vor.point_region[i]].copy()  #La indexación de las regiones la dan los sitios (puntos originales). Hay que corregir porque en Voronoi salen otros.
        if -1 in list:
            list.remove(-1)
    #print('region {}'.format(i))
    #print('voronoi vertices ={}'.format(vor.vertices[list]))
    #print('puntos en poligono = {}'.format(poligono[puntos_en_region_n_sin_pesos(sitios,poligono,i)]))    
        vert = vor.vertices[list].copy()
        rows_to_remove=[]  
        for j in range(0,np.shape(vert)[0],1):  # Aquí se quitan los puntos de cada región que están por fuera de la región acotada
            if poligon_path.contains_point(vert[j]) == False:
                rows_to_remove.append(j)
        vert = np.delete(vert,rows_to_remove,0)
        a = np.vstack((vert,poligono[puntos_en_region_n_sin_pesos(sitios,poligono,i)]))
        regiones.append(a) #aquí están las regiones con los puntos del polígono y los vértices de voronoi

    for row, side in enumerate(vor.ridge_vertices): #se hace un loop sobre las líneas que forman el diagrama de Voronoi
        if side[0]!=-1:   #aquí se escogen las líneas del diagrama de Voronoi que son acotadas. Estás no tienen -1 en la primera coordenada
            v1x = vor.vertices[side[0]][0]  #vértice 1 del segmento
            v1y = vor.vertices[side[0]][1]
            v2x = vor.vertices[side[1]][0]  #vértice 2 del segmento
            v2y = vor.vertices[side[1]][1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]   #vértice 1 del lado de la región externa
                w1y = poligono[j][1]
                w2x = poligono[j+1][0]   #vértice 2 del lado de la región externa
                w2y = poligono[j+1][1]
                if segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y) != None:
                    x , y = segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y)  #punto de intersección
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = vor.ridge_points[row][0]  #el punto se le añade a las regiones con frontera el segmento
                    region_2_to_add = vor.ridge_points[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))
                    #plt.plot(new_intersection[0][0], new_intersection[0][1], marker="o", markersize=10, markeredgecolor="black", markerfacecolor="magenta")
            #plt.plot([v1x,v2x],[v1y,v2y], c='r')  #Segment line between to vertices
        else:
            vertex = vor.vertices[side[1]]   # Vértice del diagrama de Voronoi de donde sale una línea no acotada
            point_1= vor.ridge_points[row][0]  #puntos más cercanos al vértice cuya línea equidistante a estos dos puntos definen la línea no acotada del diagrama de Voronoi
            point_2= vor.ridge_points[row][1]
            normal = vor.points[point_1]-vor.points[point_2]   #vector normal a la línea no acotada. 
            dir = np.array([normal[1],-normal[0]])            #Perpendicular al vector que une a los dos puntos
            sitios_sin = np.delete(sitios,[point_1, point_2],axis=0)  #Se le quitan los dos puntos para poder ubicar el tecero más cercano (en los vértices hay tres puntos equidistantes)
            cercano= punto_mas_cercano_sin_pesos(sitios_sin,vertex)  #se usa la función punto más cercano pero...
            if cercano>=min(point_1,point_2):
                cercano = cercano+1                       # al quitar los dos puntos que definen la línea se mueven las filas. Hay que corregir este error. Son los dos if
            if cercano>=max(point_1,point_2):
                cercano = cercano+1
            #print('vertice = {}, puntos = {}, {}, punto cercano = {}, dir = {}'.format(side[1], point_1, point_2,cercano, dir))
            if np.linalg.norm(vertex+dir-vor.points[cercano]) < np.linalg.norm(vertex+dir-vor.points[point_1]):# si el vertex+dir está más cerca al tercer punto que a los dos originales, se reversa dir
                dir = -dir
            v1x = vertex[0]  #vértice inicial del rayo
            v1y = vertex[1]
            v2x = (vertex+dir)[0]  #vértice hacia donde el rayo abre
            v2y = (vertex+dir)[1]
            for j in range(-1,np.shape(poligono)[0]-1,1):
                w1x = poligono[j][0]  #vértice 1 del lado del polígono
                w1y = poligono[j][1]
                w2x = poligono[j+1][0] #vértice 2 del lado del polígono
                w2y = poligono[j+1][1]
                if segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y) != None:  #intersección punto rayo
                    x , y = segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y)
                    new_intersection = np.array([[x,y]])
                    region_1_to_add = vor.ridge_points[row][0]  #se añade la intersección a la región
                    region_2_to_add = vor.ridge_points[row][1]
                    regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                    regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))
                    #plt.plot(new_intersection[0][0], new_intersection[0][1], marker="o", markersize=10, markeredgecolor="black", markerfacecolor="magenta")
            #plt.plot([vertex[0],(vertex+dir)[0]],[vertex[1], (vertex+dir)[1]],c='r', linestyle='--')   #pinta la recta que sale del vértice sin ser acotado
    areas=[]
    perimetros=[]
    for n in range(0,len(regiones),1):
        if len(regiones[n].tolist()) != 0:
            zona = ConvexHull(regiones[n])
            regiones[n] = zona.points[zona.vertices]
            areas.append(zona.volume)
            perimetros.append(zona.area)
        else:
            areas.append(0)
            perimetros.append(0)    
    areas = np.array(areas)
    perimetros = np.array(perimetros)    
    lista_respuesta = []    
    lista_respuesta.append(regiones)
    lista_respuesta.append(areas)
    lista_respuesta.append(perimetros)
    # Lista de respuesta. Devuelve en [0] las regiones, en [1] las areas, en [2] los perimetros
    return lista_respuesta #


# FUnción a optimizar. DIstancia al vector de áreas promedio por un peso,
# más distancia al perímetro promedio, por un peso.
# SI los pesos se inicializan en 1 y 1 es sencillamente la suma  de las distancias
# a las áreas y perímetros promedio.
def optimizador_sin_pesos(areas,perimetros,peso_areas,peso_perimetros):
    area_promedio = areas.mean()
    perimetro_promedio = perimetros.mean()

    dist_areas = sum(((areas-area_promedio))**2)  ##Sin normalizar
    dist_perimetros=sum(((perimetros-perimetro_promedio)**2))

    #dist_areas = sum(((areas/area_promedio-1))**2)  ##Convergencia lenta. Avanza más rápido en áreas.
    #dist_perimetros=sum(((perimetros/perimetro_promedio-1)**2))
    
    #dist_areas = sum(np.abs((areas/area_promedio-1))) ##Convergencia rápida en áreas. En perímetros se vuelve constante!!!
    #dist_perimetros=sum((perimetros/perimetro_promedio-1)**2)

    #dist_areas = sum(np.abs((areas/area_promedio-1))) ##Esta es la raíz cuadrada de la original, norma l1
    #dist_perimetros=sum(np.abs(perimetros/perimetro_promedio-1))
    
    #dist_areas = sum(abs((areas - area_promedio)/area_promedio))
    #dist_perimetros=sum(abs(perimetros - perimetros.mean()))/perimetros.mean()
    return dist_areas*peso_areas + dist_perimetros*peso_perimetros

def f(poligono,sites):
    part = particion(poligono,sites)
    return optimizador_sin_pesos(part[1],part[2],1,1) #return optimizador(part[1],part[2],1,1)

def gradiente(poligono, sitios, delta, peso_areas, peso_perimetros):
    grad = np.empty((0,2))
    part=particion(poligono,sitios)
    initial_value = optimizador_sin_pesos(part[1],part[2], peso_areas, peso_perimetros)
    for row in range(0,np.shape(sitios)[0],1):
        base_x = np.zeros(np.shape(sitios))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(sitios))
        base_y[row] = np.array([0,1])
        part_x=particion(poligono,sitios+base_x*delta)
        cambio_x = (optimizador_sin_pesos(part_x[1],part_x[2], peso_areas, peso_perimetros)-initial_value)/delta
        part_y=particion(poligono,sitios+base_y*delta)
        cambio_y = (optimizador_sin_pesos(part_y[1],part_y[2], peso_areas, peso_perimetros)-initial_value)/delta
        grad = np.append(grad, np.array([[cambio_x,cambio_y]]),axis=0)
    return grad

def grad_f(poligono, sitios, delta):
    grad = np.empty((0,2))
    initial_value = f(poligono, sitios)
    for row in range(0,np.shape(sitios)[0],1):
        base_x = np.zeros(np.shape(sitios))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(sitios))
        base_y[row] = np.array([0,1])
        cambio_x = (f(poligono, sitios+base_x*delta)-initial_value)/delta
        cambio_y = (f(poligono, sitios+base_y*delta)-initial_value)/delta
        grad = np.append(grad, np.array([[cambio_x,cambio_y]]),axis=0)
    return grad

def grad_f_area(poligono, sitios, delta):
    grad = np.empty((0,2))
    part=particion(poligono, sitios)
    initial_value = optimizador_sin_pesos(part[1],part[2],1,0)
    for row in range(0,np.shape(sitios)[0],1):
        base_x = np.zeros(np.shape(sitios))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(sitios))
        base_y[row] = np.array([0,1])
        part_x=particion(poligono, sitios+base_x*delta)
        cambio_x = (optimizador_sin_pesos(part_x[1],part_x[2],1,0)-initial_value)/delta
        part_y=particion(poligono, sitios+base_y*delta)
        cambio_y = (optimizador_sin_pesos(part_y[1],part_y[2],1,0)-initial_value)/delta
        grad = np.append(grad, np.array([[cambio_x,cambio_y]]),axis=0)
    return grad    

def grad_f_perimetro(poligono, sitios, delta):
    grad = np.empty((0,2))
    part=particion(poligono, sitios)
    initial_value = optimizador_sin_pesos(part[1],part[2],0,1)
    for row in range(0,np.shape(sitios)[0],1):
        base_x = np.zeros(np.shape(sitios))
        base_x[row] = np.array([1,0])
        base_y = np.zeros(np.shape(sitios))
        base_y[row] = np.array([0,1])
        part_x=particion(poligono, sitios+base_x*delta)
        cambio_x = (optimizador_sin_pesos(part_x[1],part_x[2],0,1)-initial_value)/delta
        part_y=particion(poligono, sitios+base_y*delta)
        cambio_y = (optimizador_sin_pesos(part_y[1],part_y[2],0,1)-initial_value)/delta
        grad = np.append(grad, np.array([[cambio_x,cambio_y]]),axis=0)
    return grad

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

#AQuí comienza el código de búsqueda con cuatro metodologías
# 1. Primero se acerca a que los centros de voronoi sean los centros de masa
# 2. Despues se itera el método del gradiente con los centros de voronoi
# 3. depues se itera el gradiente con los centros de voronoi con pesos (no se hace muchas veces es ineficiente)
# 4. despues se iterea el gradiante moviendo vertices
#   en el procedimiento 4 se puede violar la convexidad.
#   se le añadió en el funcional el error de convexidad con un peso de 10**-1
#   para que force la búsqueda de una solución convexa, así el gradiente apunte a una solución no convexa.


# importing date class from datetime module
from datetime import date
  
# creating the date object of today's date
fecha = date.today()

#Número de regiones
number_of_regions=8

#Número de veces que busca solucionar polinomios aleatorios
number_of_random_poligons=1

#Número de veces que repetirá la búsqueda comenzando en puntos aleatorios si no es satisfactoria la anterior
number_of_repetitions=1

df_error=pd.DataFrame(columns=['fig','rep','tiempo','t','er_vor','er_conv','er_tot_nor'])
df_poligono=pd.DataFrame(columns = ['x','y','fig'])

figura=0
while (figura < number_of_random_poligons) :
    
    ##POLIGONO

    #Region acotada que se va a particionar. Se define aleatoriamente y se le toma el convex hull
    rng_poligon = np.random.default_rng()
    #rng_poligon = np.random.default_rng(75988)
    random_points_poligon = rng_poligon.uniform(-10, 10,(10, 2))   # random points in 2-D
    #random_points_poligon = np.array([[6.550035845261398,-0.23728769270522854],
    #    [-5.563036917117787,7.398356456338423],
    #    [-6.380355418675318,1.0519939534424587],
    #    [-6.47558087947086,-3.8744785255704457],
    #    [-0.06719563593481581,-9.313936397493801],
    #    [3.4096374189832837,-8.66040711097301]])

    poligon = ConvexHull(random_points_poligon)
    area_del_poligono=poligon.volume
    # La región a particionar está guardada en "poligono"
    poligono = poligon.points[poligon.vertices] # 2-d array de puntos que definen la región externa
    area_del_poligono=poligon.volume
    plt.plot(random_points_poligon[:,0], random_points_poligon[:,1], 'o')
    for simplex in poligon.simplices:
        plt.plot(poligon.points[simplex, 0], poligon.points[simplex, 1], 'k-')
    plt.plot(poligon.points[poligon.vertices,0], poligon.points[poligon.vertices,1], 'r--', lw=2)
    plt.plot(poligon.points[poligon.vertices[0],0], poligon.points[poligon.vertices[0],1], 'ro')
    plt.show() 
    df_poligono_add=pd.DataFrame(poligono, columns = ['x','y'])
    df_poligono_add['fig']=figura
    df_poligono=pd.concat([df_poligono,df_poligono_add], ignore_index = True)
    df_poligono.reset_index()
    
    df_poligono.to_csv('poligonos_{}_lados_conv_{}.csv'.format(number_of_regions, fecha), index=False)
    


    alcanzo_resultado=False

    repeticion=0

    while (alcanzo_resultado==False) and (repeticion < number_of_repetitions):
        
        starttime = timeit.default_timer()
        
        ##SITIOS ARBITRARIOS    

        # Aquí se escogen los puntos (sitios) donde se hacen los centros de las
        # regiones de Voronoi. Las coordenadas se guardarán en un array llamado "sitios"
        # Sitios randomizados
        rng_sitios = np.random.default_rng()
        #random_points_poligon = rng_sitios.uniform(-10, 10,(9, 2))
        # Aquí escogeremos numero_de_regiones puntos para producir el diagrama de Voronoi. Pero los escogeremos dentro de la region
        bbox = [poligon.min_bound, poligon.max_bound] #Bounding box
        #Hull path
        poligon_path = Path( poligon.points[poligon.vertices] )
        #Draw number_of_regions random points inside the convex hull
        rand_points = np.empty((number_of_regions, 2))
        #Choose number_of_regions random weights
        rand_weights= np.empty(number_of_regions)
        for i in range(number_of_regions):
            #Draw a random point in the bounding box of the convex hull
            rand_points[i] = np.array([rng_sitios.uniform(bbox[0][0], bbox[1][0]), rng_sitios.uniform(bbox[0][1], bbox[1][1])])
            rand_weights[i] = rng_sitios.uniform(bbox[0][0], bbox[1][0])  #weights are chosen arbitrarily on the same imits as box
            #We check if the random point is inside the convex hull, otherwise we draw it again            
            while poligon_path.contains_point(rand_points[i]) == False:
                rand_points[i] = np.array([rng_sitios.uniform(bbox[0][0], bbox[1][0]), rng_sitios.uniform(bbox[0][1], bbox[1][1])])
        #Sitios donde van los puntos que generan el diagrama de Voronoi
        sitios = rand_points
        pesos = rand_weights
        slenght=len(sitios)#largo del arreglo

        #---------------------------------------------------

        # Busca sitios que sean sus propios centros de masa
        #sites=best
        starttime = timeit.default_timer()
        coordenadas=sitios.copy()
        part = particion(poligono,coordenadas)
        regiones, areas, perimetros = part[0], part[1], part[2]
        centros = np.empty(np.shape(coordenadas))
        for i in range(len(regiones)):
            centros[i]=centroide(regiones[i])[0]
        coord = coordenadas    
        coordenadas = centros
        end_while_centros=20
        if repeticion > 0:
            end_while_centros = 5-repeticion
        t=0
        while (t < end_while_centros) and (np.linalg.norm(coord-centros) >10**-3):
            #print('t={}, dist_area ={}, dist_peri={}'.format(t,optimizador(areas,perimetros,1,0), optimizador(areas,perimetros,0,1)))
            print('t={}, dist_area ={:.8f}, dist_peri={:.8f}'.format(t,optimizador(areas,perimetros,1,0), optimizador(areas,perimetros,0,1)))
            #print('gradiente = {}'.format(gradiente(poligono,sites,0.1,1,1)))
            part = particion(poligono,coordenadas)
            regiones = part[0]
            areas = part[1]
            perimetros = part[2]
            centros = np.empty(np.shape(coordenadas))
            for i in range(len(regiones)):
                centros[i]=centroide(regiones[i])[0]
            coord = coordenadas    
            coordenadas = centros
            t=t+1
        print("Figura = {}, Repeticion ={}, while centros de masa terminado. t={}".format(figura,repeticion,t)) 
        #
        # -------------------------------------------------------------------------
        # 
          
        #ssites=site
        #sites=best
        ssites=coordenadas.copy()
        #ssites=sitios
        mu=10**-8
        step0=1
        step=step0
        t=0
        multiplicador=0  #valor=ff(poligono, ssites, multiplicador)
        valor=f(poligono, ssites)
        gradiente_area=grad_f_area(poligono, ssites,10**-8)
        gradiente_perimetro=grad_f_perimetro(poligono, ssites,10**-8)
        norma_area=np.linalg.norm(gradiente_area)
        norma_perimetro=np.linalg.norm(gradiente_perimetro)
        norma_grad=np.linalg.norm(gradiente_perimetro+gradiente_area)
        while (t < 100) and (valor > 10**-4) and (step*norma_grad > 10**-8):
            part = particion(poligono,ssites)
            regiones = part[0]
            areas = part[1]
            perimetros = part[2]
            error_total_normalizado=sum((areas/areas.mean()-1)**2)+sum((perimetros/perimetros.mean()-1)**2)
            valor=f(poligono, ssites)
            #gradiente = grad_f(poligono, ssites,10**-8)
            gradiente_area=grad_f_area(poligono, ssites,10**-8)
            gradiente_perimetro=grad_f_perimetro(poligono, ssites,10**-8)
            norma_area=np.linalg.norm(gradiente_area)
            norma_perimetro=np.linalg.norm(gradiente_perimetro)
            norma_grad=np.linalg.norm(gradiente_perimetro+gradiente_area)
            cosine_angle=sum(sum(gradiente_area*gradiente_perimetro))/(np.linalg.norm(gradiente_area)*np.linalg.norm(gradiente_perimetro))
            #print('t={}, d={:.6f} ,d_ar ={:.6f}, d_pe={:.6f}, |grad|={:.6f}, |g_ar|={:.6f}, |g_pe|={:.6f}, cos(ang)={:.6f}, step={:.4f}'.format(t,optimizador_sin_pesos(areas,perimetros,1,1), optimizador_sin_pesos(areas,perimetros,1,0), optimizador_sin_pesos(areas,perimetros,0,1),norma_grad,norma_area,norma_perimetro,cosine_angle, step))
            print('t={}, d={:.6f} ,|grad|={:.6f}, err_norm={}, cos(ang)={:.6f}, step={:.4f}'.format(t,optimizador_sin_pesos(areas,perimetros,1,1),norma_grad,error_total_normalizado,cosine_angle, step))
            #print('t={}, ff ={}, f={},  norma grad={}, step={}'.format(t,valor, f(poligono, ssites),norma,step))
            step=step0
            while f(poligono, ssites - step*(1*gradiente_area+1*gradiente_perimetro)) > valor - step**2*mu*(norma_area+norma_perimetro)**2 :
                step=step/2 
                if step < 10**-8:
                    break
            if np.abs(f(poligono, ssites - step*(1*gradiente_area+1*gradiente_perimetro)) - valor) < 10**-6:
                break
            ssites = ssites - step*(1*gradiente_area+1*gradiente_perimetro)    
            t=t+1    
        print("Figura = {}, Repeticion ={}, while gradiente. Valor={}, t={}".format(figura,repeticion,valor,t)) 
        error_gradiente=valor#print("Tiempo de ejecución :", timeit.default_timer() - starttime, "segundos")   
        error_voronoi=error_total_normalizado
        # 
        # ----------------------------------------------------------
        # 
        #   
        
        #sites=coordenadas.copy()
        #sites=sitios.copy()
        sites=ssites.copy()
        weights=np.zeros(len(sitios))
        #weights=pesos.copy()
        mu=10**-6
        step0=0.1
        step=step0
        t=0
        valor=f_wv(poligono, sites, weights)
        gradiente = grad_f_wv(poligono, sites,weights,10**-6)
        norma_sitios=np.linalg.norm(gradiente[0])
        norma_pesos=np.linalg.norm(gradiente[1])
        #diagramas = []
        #centros = []
        #diagramas.append(particion_wv(poligono,sites,weights))
        #centros.append(sites)
        while (t < 1) and (valor > 10**-6) and (step*(norma_sitios**2+norma_pesos**2)**(0.5) > 10**-3):
            info=particion_wv(poligono,sites,weights)
            valor=optimizador(info[1],info[2],1,1)
            #diagramas.append(info)
            #centros.append(sites)
            gradiente = grad_f_wv(poligono, sites,weights,10**-6)
            norma_sitios=np.linalg.norm(gradiente[0])
            norma_pesos=np.linalg.norm(gradiente[1])
            #print('t={}, d ={:.6f}, d_ar={:.6f}, d_pe={:.6f}, |gr_sitios|={:.6f}, |gr_pesos|={:.6f}, step={}'.format(t,valor,optimizador(info[1],info[2],1,0), optimizador(info[1],info[2],0,1),norma_sitios, norma_pesos,step))
            step=step0
            while f_wv(poligono, sites - step*gradiente[0], weights - step*gradiente[1]) > valor: # - step*mu*(norma_sitios**2+norma_pesos**2) :
                step=step/2 
                if step < 10**-8:
                    break
            if abs(f_wv(poligono, sites - step*gradiente[0], weights - step*gradiente[1]) - valor) < 10**-8:
                break   
            sites= sites-gradiente[0]*step
            weights = weights-gradiente[1]*step  
            t=t+1
        print("Figura = {}, Repeticion ={}, while gradiente pesos.Valor={}, t={}".format(figura,repeticion,valor,t)) 
        #tiempo=timeit.default_timer() - starttime,    
        #print("Tiempo de ejecución :", tiempo, "segundos")     


        #------------------------------------------------------------------------------------
        external=external_vertices_wv(poligono,sites,weights) 
        intermediate=intermediate_vertices_wv(poligono,sites,weights)     
        internal=internal_vertices_wv(poligono,sites,weights)
            
        mu=10**-6
        step0=0.1
        step=step0
        t=0
        kappa=10**-1 #peso en el punishment 
        parti=particion_vertices(external,intermediate,internal)
        valor=optimizador(parti[1],parti[2],1,1) + kappa*(sum(parti[1])-area_del_poligono)**2
        perim=parti[2]
        are=parti[1]
        error_total_normalizado=sum((are/are.mean()-1)**2)+sum((perim/perim.mean()-1)**2)
        error_convexidad=(sum(parti[1])-area_del_poligono)**2
        #diagramas = []
        #centros = []
        #diagramas.append(particion)
        #centros.append(sites)
        while (t < 2000) and ((error_total_normalizado > 10**-8) or (error_convexidad > 10**-8)):
            parti=particion_vertices(external,intermediate,internal)
            valor=optimizador(parti[1],parti[2],1,1) + kappa*(sum(parti[1])-area_del_poligono)**2
            #diagramas.append(parti)
            #centros.append(sites)
            gradiente_internal = grad_part_vert_internal(external,intermediate,internal,10**-7) + kappa*grad_part_vert_internal_extra(external,intermediate,internal,10**-7)
            norma_grad_internal=np.linalg.norm(gradiente_internal)
            gradiente_intermediate = grad_part_vert_intermediate(external,intermediate,internal,10**-7) + kappa*grad_part_vert_intermediate_extra(external,intermediate,internal,10**-7)
            norma_grad_intermediate=np.linalg.norm(gradiente_intermediate)
            error_convexidad=(sum(parti[1])-area_del_poligono)**2
            #norma_pesos=np.linalg.norm(gradiente[1])
            #print('t={}, er ={:.8f}, er_ar={:.8f}, er_pe={:.8f}, conv={:.10f}, |g_intern|={:.6f},|g_interm|={:.6f}, step={}'.format(t,valor,optimizador(parti[1],parti[2],1,0), optimizador(parti[1],parti[2],0,1),error_convexidad,norma_grad_internal,norma_grad_intermediate,step))
            print('t={}, fun ={:.8f}, err_norm={:.10f},  conv={:.10f}, |g_intern|={:.6f},|g_interm|={:.6f}, step={}'.format(t,valor, error_total_normalizado,error_convexidad,norma_grad_internal,norma_grad_intermediate,step))
            step=step0
            while step >10**-6:
                internal_new=[]
                internal_new.append(internal[0]-step*gradiente_internal)
                internal_new.append(internal[1])
                intermediate_new=[]
                intermediate_new.append(intermediate[0]-step*gradiente_intermediate)
                intermediate_new.append(intermediate[1])
                intermediate_new.append(intermediate[2])
                particion_new=particion_vertices(external,intermediate_new,internal_new)
                valor_new=optimizador(particion_new[1],particion_new[2],1,1) + kappa*(sum(particion_new[1])-area_del_poligono)**2
                if valor_new < valor - step*mu*(norma_grad_internal**2) :
                    break
                else:
                    step=step/2
            #if particion_new[4]==False:
                #print("Alguna región no es convexa.\n Convexidad por regiones = {}".format(particion_new[3]))
            #    break
            #out_of_bounds=False #se revisa que los puntos intermedios no se salgan de los lados
            #for i in range(np.shape(intermediate[0])[0]):
            #    a=np.dot(intermediate[0][i]-external[0][intermediate[2][i][0]],intermediate[0][i]-external[0][intermediate[2][i][1]])
            #    if a > 0:
            #        bound1=intermediate[1][i][0]
            #        bound2=intermediate[1][i][1]
            #        #print("intermediate vertex {}, between regions {} and {} is out of bounds".format(i,bound1,bound2))
            #        out_of_bounds=True
            #if out_of_bounds==True:
            #    break  
            perim=particion_vertices(external,intermediate,internal)[2]
            are=particion_vertices(external,intermediate,internal)[1]
            error_total_normalizado=sum((are/are.mean()-1)**2)+sum((perim/perim.mean()-1)**2)
            if (error_total_normalizado < 10**-8) and (error_convexidad < 10**-8):
                print('Terminó. err_norm= {}, erro_conv ={}'.format(error_total_normalizado,error_convexidad))   
                break
            #if (sum(parti[1]) > area_del_poligono +10**-8): 
                #print('Se dañó la convexidad. Area final= {}, Area inicial ={}'.format(sum(parti_[1]),area_del_poligono))   
                #break      
            internal=internal_new 
            intermediate=intermediate_new
            t=t+1

        
        perim=particion_vertices(external,intermediate,internal)[2]
        are=particion_vertices(external,intermediate,internal)[1]
        error_total=sum((are-are.mean())**2)+sum((perim-perim.mean())**2)
        error_total_normalizado=sum((are/are.mean()-1)**2)+sum((perim/perim.mean()-1)**2)

        tiempo=timeit.default_timer()-starttime

        nuevos_datos={'fig': [figura], 'rep': [repeticion], 'tiempo':[round(tiempo)], 't':[t], 'er_vor':[error_voronoi], 'er_conv': [error_convexidad], 'er_tot_nor': [error_total_normalizado]}
        df_error_add = pd.DataFrame.from_dict(nuevos_datos)
        df_error = pd.concat([df_error,df_error_add], ignore_index = True)
        df_error.reset_index()

        df_error.to_csv('errores_{}_lados_conv_{}.csv'.format(number_of_regions,fecha), index=False)

        if (error_total_normalizado) <= 10**-8 and (error_convexidad <= 10**-8):
            alcanzo_resultado=True
        print("repeticion {}, figura {}, alcanzo = {}. err_nor={}, t={}".format(repeticion,figura,alcanzo_resultado,error_total_normalizado, t))
        repeticion=repeticion+1
        #final del while de repeticion
    figura=figura+1
    #final del while de las figuras



graph_only_regiones_centroides(particion_vertices(external,intermediate,internal)[0])

###################
#Despues del todo el procedimiento (Centros de masa, gradiente voronoi, gradiente mover vertices)
graph_only_regiones_centroides(particion_vertices(external,intermediate,internal)[0])
#DEspues de gradiente Voronoi
graph_regiones_centroides(particion_wv(poligono,sites,weights)[0],sites)

particion_final=particion_vertices(external,intermediate,internal)
print("Áreas finales = {}".format(particion_final[1]))
print("Perímetros finales = {}".format(particion_final[2]))
