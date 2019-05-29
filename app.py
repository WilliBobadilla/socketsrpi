"""
autor: Williams Bobadilla 
colaboracion de: Bryan Giger 
fecha de creacion: 17 de mayo del 2019 
Descripcion: Server escrito en flask para el uso de botones normalmente abierto, 
para un sistema de encuesta, al presionar uno de los tres botones disponibles, 
para las tres opciones marcada en la pagina como a b c, la pagina se actualiza 
con la respuesta enviada desde el server al cliente mediante sockets, con una interrupcion 
activada mediante uno de los botones presionados. Usamos socketIo para tal fin, y del 
lado del cliente jquery para recibir y realizar las acciones correspondientes, en este
caso lo que realiza es que al presionar el boton, del lado del ciente se ve la cuenta 
de la cantidad de veces que se presiono el boton.


"""



from flask import Flask, render_template, session,request, jsonify,current_app,copy_current_request_context
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
import requests  
import RPi.GPIO as gpio   #libreria utilizada para la rpi


#definimos los puertos de entrada salida 
entrada1=21   #variables que definen las entradas
entrada2=22 

gpio.setmode(gpio.BCM) # Ponemos la placa en modo BCM
gpio.setup(entrada1, gpio.IN)    # GPIO numero 21 como entrada
gpio.setup(entrada2, gpio.IN)    # GPIO numero 22 como entrada


pulsaciones=1    #variable global usada para contar la cantidad de veces que se pulso el boton entrada1

app = Flask(__name__)  #instanciamos la clase Flask y creamos el objeto app
cors=CORS(app)         #creamos otro objeto llamado cors y heredamos los atributos y metodos de app
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)   #creamos un objeto socketio y heredamos los atributos y metodos de app


@socketio.on('connect',namespace='/') #evento que detecta un cliente conectado al server 
def cliente_connectado():
    pass

def manejo(boton):
    global pulsaciones
    pulsaciones+=1  #aumentamos en uno cada vez que entramos aca 
    with app.test_request_context('/'):
        print(pulsaciones)        #imprimimos la cantidad de veces que pulsamos el boton 
        socketio.emit('my response',{"data":pulsaciones},namespace="/")   #emitimos un mensaje con la cantidad de pulsaiones 


gpio.add_event_detect(entrada1, gpio.RISING, callback=manejo, bouncetime=200)  #detecta un flanco positivo o de subida 


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':  
    socketio.run(app)             #inicializamos el sevidor

