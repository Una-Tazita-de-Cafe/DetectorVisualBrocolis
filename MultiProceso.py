import threading
from Vision import Vision_1
from Vision2 import Vision_2
#import Vision2
# Variable compartida para indicar el estado actual del ciclo

# Función para el primer hilo

stop_event = threading.Event()
def run_vision_1():
    vision_1 = Vision_1(2,"cam2",7)
    vision_1.main([14, 30])

# Función para el segundo hilo
def run_vision_2():
    vision_1 = Vision_1(0,"cam1",8)
    vision_1.main([14, 30])
# Crear dos hilos

h1 = threading.Thread(target=run_vision_1)
h2 = threading.Thread(target=run_vision_2)


# Iniciar los hilos

h1.start()
h2.start()

# Esperar a que ambos hilos terminen (esto puede no ocurrir ya que son ciclos infinitos)

try:
    h1.join()
    h2.join()
except KeyboardInterrupt:
    # Manejar la interrupción del teclado para detener los hilos
    print("Deteniendo hilos...")
    stop_event.set()
    h1.join()
    h2.join()
    print("Hilos detenidos")

print("Ambos hilos se han detenido")