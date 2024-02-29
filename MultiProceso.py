import threading
from Vision import Vision_1
from Vision2 import Vision_2
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
        self.vision_1 = Vision_1(0,"cam1",7)
        self.vision_2 = Vision_2(1,"cam2",6)
        
    def run_vision_1(self):
        #vision_1 = Vision_1(0,"cam2",7)
        self.vision_1.main([14, 30],{17,20})
    def run_vision_2(self):
        #vision_1 = Vision_1(0,"cam2",7)
        self.vision_2.main([14, 30],{17,20})
    def inicio(self):
        h1=threading.Thread(target=self.run_vision_1)
        h2=threading.Thread(target=self.run_vision_2)
        h1.start()
        h2.start()
        try:
            h1.join()
            h2.join()
        except KeyboardInterrupt:
            # Manejar la interrupción del teclado para detener los hilos
            print("Deteniendo hilos...")
            self.stop_event.set()
            h1.join()
            h2.join()
            print("Hilos detenidos")
        print("Ambos hilos se han detenido")

# Función para el segundo hilo

# Crear dos hilos

#h1 = threading.Thread(target=run_vision_1)
#h2 = threading.Thread(target=run_vision_2)


obj=MultiPoceso()

@app.route("/inicio")
def inicio():
    obj.inicio()
@app.route("/stream")
def stream():
    return Response(obj.vision_1.conversion_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route("/stream2")
def stream2():
    return Response(obj.vision_2.conversion_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ =="__main__":
    app.run(host='0.0.0.0', debug=False)
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