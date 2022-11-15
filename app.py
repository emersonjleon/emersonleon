import os

from flask import Flask, redirect, render_template, request, url_for

import pickle
from datetime import datetime, date

from visual import threejsSpheresText, chipfiringVisual, chipfiringVisual2
from threedfiring import chipfiring3d

#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())

app = Flask(__name__)

def pickleLoad(filename):
    pickleobject = []
    with (open(filename, "rb")) as openfile:
        while True:
            try:
                pickleobject.append(pickle.load(openfile))
            except EOFError:
                break
    return pickleobject[-1]


#sesiones=pickleLoad('sesiones.pkl')


#####    

def guardarSesionActual(name='*unsaved '):
    global historias
    #### Crear a class Sesion!
    nuevasesion={}
    nuevasesion['fecha'] = datetime.now()
    if name == '*unsaved ':
        name+=str(nuevasesion['fecha'])
    else:
        nuevasesion['nombre'] = name
    sesiones.append(nuevasesion)

    # write the python object (dict) to pickle file
    f = open("sesiones.pkl","wb")
    pickle.dump(sesiones,f)
    f.close()



    

# @app.route("/sesiones", methods=("GET", "POST"))
# def editar_sesiones():
#     global historias

#     if request.method == "POST":
#         myaction = request.form["myaction"]
#         ##################
#         if myaction == "guardarSesionActual":  #nueva sesion
#             sesionname = request.form["sesionname"]
#             guardarSesionActual(sesionname)

#             return render_template("sesiones.html", historias=historias, sesiones=sesiones)
#         ###############
#         elif myaction == "borrarhistorias":  #caution
#             pass
#             return render_template("sesiones.html", historias=historias, sesiones=sesiones)
#         ##############
#         elif myaction == "borrarsesionguardada":  
#             borrarsesion = request.form["deletesesion"]
#             for i in range(len(sesiones)):
#                 if sesiones[i]['nombre']==borrarsesion:
#                     deleted=sesiones.pop(i)
#                     nota=f'Se eliminó la sesión {borrarsesion}'
#                     f = open("sesiones.pkl","wb")
#                     pickle.dump(sesiones,f)
#                     f.close()
#                     break
#                 else:
                
#                     nota='No se encontró ninguna sesión con ese nombre'
#             return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)
#         #######################
#         elif myaction == "cargarsesion":  
#             cargarsesion = request.form["cargarsesion"]
#             for i in range(len(sesiones)):
#                 if sesiones[i]['nombre']==cargarsesion:
#                     historias=sesiones[i]['historias']
#                     nota= f'se cargó la sesión { sesiones[i]["nombre"] }'
#                     break
#                 else:
#                     nota='No se encontró ninguna sesión con ese nombre'
#             return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)


#     return render_template("sesiones.html", historias=historias, sesiones=sesiones)







###################
###Generate index page
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
@app.route("/home", methods=("GET", "POST"))
def homeapp():
    return render_template("home.html")


@app.route("/math", methods=("GET", "POST"))
def mathpage():
    return render_template("math.html")

@app.route("/visual", methods=("GET", "POST"))
def visualpage():
    return render_template("visualization.html")



@app.route("/index")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return render_template("index.html", links=links)


@app.route("/blog")
def blog():
    return render_template("blog.html")



@app.route("/visual", methods=("GET", "POST"))
def visual():
    spheres=[]
    for x in range(-10,10,1):
        for y in range(-10,10,1):
            spheres.append((10*x,10*y,0))
    
    spheresText=threejsSpheresText(spheres)
    return render_template("visual.html", width=600, height=400,
                           spheresText=spheresText)







@app.route("/sandpile/<string:chipnumber>", methods=("GET", "POST"))
def sandpile(chipnumber):
    colorlist=["",
               "0x6699ff",
               "0xdddd00",
               "0x883388",
               "0x550000",
               "0x000033"]
    spheresText=chipfiringVisual(chipfiring3d(int(chipnumber),size=25),colorlist, spaces=25)    
    return render_template("visual.html", width=1000, height=700,
                           spheresText=spheresText)




def parseChipstring(chipstring):
    "example chipstring: '10000chips-ballsize30--cubematrix25'  "
    # "example chipstring: '10000chips-size30--display12345'  "
    chipposition = chipstring.find("chip")
    chips=int(chipstring[0:chipposition])
    epos = chipstring.find("size")
    figure=chipstring[chipposition+6:epos]
    linespos = chipstring.find("--")	             
    ballsize=int(chipstring[epos+4:linespos])
    xposition = chipstring.find("x")
    cubematrix=int(chipstring[xposition+1:])
    # displaynumbers= [str(number) in list(displaystr) for number in range(6)]
    return chips, ballsize,cubematrix,figure

@app.route("/chipfiring", methods=("GET", "POST"))
def chipfiringredirect():
    if request.method == "POST":
        chips = request.form["chips"]
        ballsize = request.form["ballsize"]
        matrixsize = request.form["matrixsize"]
        figure = request.form["figure"]
        # if is_cube==True:
        #     figure='cube'
        # else:
        #     figure='ball'
    else:
        chips=5000
        ballsize=50
        matrixsize=35
        figure='ball'
    chipstring=f"{chips}chips-{figure}size{ballsize}--cubematrix{matrixsize}"
    return redirect(url_for('chipfiringvisualize', chipstring=chipstring))
        
@app.route("/chipfiring/<string:chipstring>", methods=("GET", "POST"))
def chipfiringvisualize(chipstring):
    chips, ballsize, cubematrix, figure= parseChipstring(chipstring)
    spheresText=chipfiringVisual2( chipfiring3d(int(chips),size=cubematrix) )    
    return render_template("chipfiringvisualize.html", mySpheresCode=spheresText, 
                           size=ballsize, chips=chips, matrixsize=cubematrix,
                           figure=figure)





#########################
if __name__ == '__main__':
    app.run()
