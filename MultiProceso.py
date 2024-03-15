import threading
from Vision import Vision_1
from Vision2 import Vision_2
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
#import Vision2
# Variable compartida para indicar el estado actual del ciclo

# Función para el primer hilo
"""Elementos para el servidor"""
from flask import Flask, Response
from flask_cors import CORS



app=Flask(__name__)
class MultiPoceso:
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.vision_1 = Vision_1(2,"cam1",7)
        #self.vision_2 = Vision_2(2,"cam2",6)
        
    def run_vision_1(self):
        #vision_1 = Vision_1(0,"cam2",7)
        self.vision_1.main([14, 30],{17,20})
    def run_vision_2(self):
        #vision_1 = Vision_1(0,"cam2",7)
        self.vision_2.main([14, 30],{17,20})
    def inicio(self):
        h1=threading.Thread(target=self.run_vision_1)
        #h2=threading.Thread(target=self.run_vision_2)
        h1.start()
        #h2.start()
        try:
            h1.join()
         #   h2.join()
            print("valiendo verga")
        except KeyboardInterrupt:
            # Manejar la interrupción del teclado para detener los hilos
            print("Deteniendo hilos...")
            self.stop_event.set()
            h1.join()
          #  h2.join()
            print("Hilos detenidos")
        except Exception as e:
            print(f"Excepción en inicio: {e}")
        print("Ambos hilos se han detenido")
    
    def Trigger(self,elemento,accion):
        try:
            modbusClient = ModbusClient('192.168.0.115', 5020)
            modbusClient.connect()
            modbusClient.write_coil(elemento, accion) #cambiar despues por el Trigger para cortar el brocoli
            modbusClient.close() 
        except:
            print("la Raspberry no esta conectado o esta en otra red")
            

# Función para el segundo hilo

# Crear dos hilos

#h1 = threading.Thread(target=run_vision_1)
#h2 = threading.Thread(target=run_vision_2)


obj=MultiPoceso()

@app.route("/seguridad")
def seguridad():
    return {"SeguridadCamara1":obj.vision_1.seguridad,
            "SeguridadCamara2":obj.vision_1.seguridad}
@app.route("/prueba")
def prueba():
   obj.vision_1.seguridad=not obj.vision_1.seguridad
   return f"{obj.vision_1.seguridad}"

@app.route("/encendido/on/<trigger>")
def encendio_componentes(trigger):
    obj.Trigger(trigger, 1)
    return "<p>jalo</p>"

@app.route("/encendido/off/<trigger>")
def apagado_componentes(trigger):
    obj.Trigger(trigger, 0)
    return "<p>jalo</p>"

@app.route("/inicio")
def inicio():
    obj.vision_1.ciclo=True
    #obj.vision_2.ciclo=True
    obj.inicio()

@app.route("/fin")
def fin():
    obj.vision_1.ciclo=False
    #obj.vision_2.ciclo=False
    return "<p>se termino</p>"

@app.route("/continuar")
def continuar():
    obj.vision_1.seguridad=True
    obj.Trigger(3,0)
    return "<p>se termino</p>"


@app.route("/stream")
def stream():
    return Response(obj.vision_1.conversion_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream2")
def stream2():
    return Response(obj.vision_2.conversion_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ =="__main__":
    app.run(port=8000, debug=False)
# Iniciar los hilos

#h1.start()
 #h2.start()

# Esperar a que ambos hilos terminen (esto puede no ocurrir ya que son ciclos infinitos)

"""try:
    h1.join()
 #   h2.join()
except KeyboardInterrupt:
    # Manejar la interrupción del teclado para detener los hilos
    print("Deteniendo hilos...")
    stop_event.set()
    h1.join()
  #  h2.join()
    print("Hilos detenidos")

print("Ambos hilos se han detenido")"""