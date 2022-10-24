# python file to generate three.js code for a bunch of spheres...

##colors
#import colorsys 
from  matplotlib import colors as mcolors

#print(mcolors.to_hex([ 0.47, 0.0, 1.0 ]))
#print(mcolors.to_hex([ 0.7, 0.321, 0.3, 0.5 ], keep_alpha=True))
#print(mcolors.to_rgb("#aabbcc"))
#print(mcolors.to_rgb("#ddee9f"))
#mcolors.hsv_to_rgb([ 0.47, 0.0, 1.0 ])

def HSVtoRGB(h, s, v): 
    #(r, g, b) =
    return mcolors.hsv_to_rgb((h, s, v) )
    #return (int(255*r), int(255*g), int(255*b)) 
    
    
def getDistinctColors(n): 
    huePartition = 1.0 / (n + 1) 
    return (HSVtoRGB(huePartition * value, 1.0, 1.0)
            for value in range(0, n))

# for color in getDistinctColors(4):
#     print(mcolors.to_hex(color))

######################################


## three.js code
def threejsSpheresObject(radius=4, scale=1, objectname="mySpheres"):
    text=f"""
var scale = {scale};
var radius = {radius}*scale,
    segments = 24,
    rings = 16;
var {objectname} = new THREE.Object3D();
var sphereGeometry = new THREE.SphereGeometry( radius, segments, rings );
"""
    return text

def threejsSphere(x,y,z, color="0xccff00", parentobject='mySpheres', spherename="mySphere"):
    """generates threejs code for a sphere"""
    text=f"""
    var sphereMaterial = new THREE.MeshLambertMaterial( {{ color: {color}  }} );
    var {spherename} = new THREE.Mesh( sphereGeometry, sphereMaterial );
    {spherename}.position.x= { x }*scale;
    {spherename}.position.y= { y }*scale;
    {spherename}.position.z= { z }*scale ;
    {parentobject}.add( {spherename} );
    """
    return text


def threejsSpheresText(spheres, objectname="mySpheres", radius='None'):
    """take a list of spheres given by a tuple (x,y,z, maybe color),"""
    text=threejsSpheresObject(objectname=objectname)
    for k, sphere in enumerate(spheres):
        name=f'{objectname}{k:0>4}'
        text+=threejsSphere(sphere[0],sphere[1],sphere[2],
                            spherename=name)
    return text+f'\n  scene.add({objectname});'


def chipfiringVisual(matrix, colorlist, spaces=20, scale=1, objectname="mySpheres"):

    mytext=f"""
    var scale = {scale};
    segments = 24,
    rings = 16;
    
    var {objectname} = new THREE.Object3D();
"""
    
    for n in range(len(colorlist)):
        if colorlist[n]:
            radius= 10 #(1000*n)**(1/3)+0.1
            mytext+=f"""
    var sphereGeometry{n} = new THREE.SphereGeometry( {radius}, segments, rings );
    var sphereMaterial{n} = new THREE.MeshLambertMaterial( {{ color: {colorlist[n]}  }} );
    var sphere{n} = new THREE.Mesh( sphereGeometry{n}, sphereMaterial{n} );

    """
    xcenter=(len(matrix)-1)/2
    ycenter=(len(matrix[0])-1)/2
    zcenter=(len(matrix[0][0])-1)/2
    
    for k in range(len(matrix)):
        for j in range(len(matrix[0])):
            for i in range(len(matrix[0][0])):
                if colorlist[matrix[k][j][i]]:
                    mytext+= f"""
                    var sphere{i}_{j}_{k}=sphere{matrix[k][j][i]}.clone()
                    sphere{i}_{j}_{k}.position.set( {spaces*(i-xcenter)}, {spaces*(j-ycenter)}, {spaces*(k-zcenter)} )
                    mySpheres.add(sphere{i}_{j}_{k})
                    """
    return mytext+f'\n  scene.add({objectname});'






def chipfiringVisual2(matrix,  spaces=100, scale=1, objectname="mySpheres"):

    mytext=f""
    
    xcenter=(len(matrix)-1)/2
    ycenter=(len(matrix[0])-1)/2
    zcenter=(len(matrix[0][0])-1)/2
    
    for k in range(len(matrix)):
        for j in range(len(matrix[0])):
            for i in range(len(matrix[0][0])):
                mytext+= f"""
                var sphere{i}_{j}_{k}=sphere{matrix[k][j][i]}.clone()
                sphere{i}_{j}_{k}.position.set( {spaces*(i-xcenter)}, {spaces*(j-ycenter)}, {spaces*(k-zcenter)} )
                mySpheres{matrix[k][j][i]}.add(sphere{i}_{j}_{k})
                    """
    return mytext+f'\n  scene.add({objectname});'







                
if __name__ == '__main__':

    spheres=[(0,0,0), (0,0,10)]
    print(threejsSpheresText(spheres))




    #print(threejsSphere(1,2,3,'0x7fd4ff'))
    #print(threejsSpheresObject(23))
    
    """
  var radius = 30,
      segments = 24,
      rings = 16;
  var phi=1.618;
      

  var sphere0 = new THREE.Mesh(
      new THREE.SphereGeometry(16, segments, rings), material);
      
      // add the sphere to the scene
  scene.add(sphere0);

      

      

  var icospheres = new THREE.Object3D();
  var sphereGeometry = new THREE.SphereGeometry( radius, segments, rings );
   
//wroten in python file icos.py   
var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7fd4ff} );
var sphere0 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere0.position.x=0*radius ;
sphere0.position.y= 1*radius ;
sphere0.position.z= 1.5*radius ;
icospheres.add( sphere0 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7f2aff} );
var sphere1 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere1.position.x=0*radius ;
sphere1.position.y= -1*radius ;
sphere1.position.z= 1.5*radius ;
icospheres.add( sphere1 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7fd400} );
var sphere2 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere2.position.x=0*radius ;
sphere2.position.y= 1*radius ;
sphere2.position.z= -1.5*radius ;
icospheres.add( sphere2 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7f2a00} );
var sphere3 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere3.position.x=0*radius ;
sphere3.position.y= -1*radius ;
sphere3.position.z= -1.5*radius ;
icospheres.add( sphere3 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0xd4ff7f} );
var sphere4 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere4.position.x=1*radius ;
sphere4.position.y= 1.5*radius ;
sphere4.position.z= 0*radius ;
icospheres.add( sphere4 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x2aff7f} );
var sphere5 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere5.position.x=-1*radius ;
sphere5.position.y= 1.5*radius ;
sphere5.position.z= 0*radius ;
icospheres.add( sphere5 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0xd4007f} );
var sphere6 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere6.position.x=1*radius ;
sphere6.position.y= -1.5*radius ;
sphere6.position.z= 0*radius ;
icospheres.add( sphere6 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x2a007f} );
var sphere7 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere7.position.x=-1*radius ;
sphere7.position.y= -1.5*radius ;
sphere7.position.z= 0*radius ;
icospheres.add( sphere7 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0xff7fd4} );
var sphere8 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere8.position.x=1.5*radius ;
sphere8.position.y= 0*radius ;
sphere8.position.z= 1*radius ;
icospheres.add( sphere8 );

var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7fd4} );
var sphere9 = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere9.position.x=-1.5*radius ;
sphere9.position.y= 0*radius ;
sphere9.position.z= 1*radius ;
icospheres.add( sphere9 );

  var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0xff7f2a} );
  var sphere10 = new THREE.Mesh( sphereGeometry, sphereMaterial );
  sphere10.position.x=1.5*radius ;
  sphere10.position.y= 0*radius ;
  sphere10.position.z= -1*radius ;
  icospheres.add( sphere10 );

  var sphereMaterial = new THREE.MeshLambertMaterial( { color: 0x7f2a} );
  var sphere11 = new THREE.Mesh( sphereGeometry, sphereMaterial );
  sphere11.position.x=-1.5*radius ;
  sphere11.position.y= 0*radius ;
  sphere11.position.z= -1*radius ;
  icospheres.add( sphere11 );




      
      

      scene.add(icospheres);
      
      
"""
