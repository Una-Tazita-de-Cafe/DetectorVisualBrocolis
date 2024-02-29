
"""libreias que se utilizan para el correcto funcionamiento del programa para detectar brocolis"""
import torch
import numpy as np
import cv2
import time
from datetime import datetime
import math
from Analizador import AnalizadorDiametro
from Conexion import Conexion
from easymodbus.modbusClient import ModbusClient
from threading import Thread, Event
import pyrealsense2
from realsense_depth import *
from ConexionDB import *
import DatosConexion 

"""Elementos para el servidor"""
from flask import Flask, Response
from flask_cors import CORS

#app=Flask(__name__)
class Vision_1:
    """Constructor (define la camara que se va a utilizar, estable la conexion para la base de datos y define los parametros para grabar )"""
    def __init__(self, puerto_camara=0,names="cam1", puerto_piston=6):
        self.names_Ca=names
        self.serial_number={0:"241122305779",2:"234322304889",1:"215122252177"}      
        self.ConexionBaseDatos=Creacion(Datos)
        self.puerto_camara=puerto_camara
        self.puerto_pston=puerto_piston
        self.trasmision_api=""
        
    """Función utilizada para reconectar camara cuando esta es cambiada o desconectada"""
    def conexionCamara(self):
        camara = cv2.VideoCapture(self.puerto_camara)
        camara, h, w = self.CamaraSettings(camara)
        ret, frame = camara.read()
        return ret, frame, camara

    """Funcion utilizada para configuración inicial de camara (parametros criticos)"""
    def CamaraSettings(self,camara) :
        camara.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        camara.set(cv2.CAP_PROP_FOCUS, 100000)
        camara.set(cv2.CAP_PROP_FPS, 60)
        camara.set(cv2.CAP_PROP_FRAME_WIDTH, 800)#840
        camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)#400
        w = camara.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = camara.get(cv2.CAP_PROP_FRAME_HEIGHT)
        h = int(h)
        w = int(w)
        return camara, h, w

    """Función utilizada para establecer los ajustes de Configuración de YoloV5"""

    def AjustesYoloV5(self,model, names) :
       
        SettingsFlag = True
        
        #Configuracion de paramatros para
        """
        #print("Ajustes de Parametros... Si no sabe lo que esta realizando por favor escriba 'no'")
        #Ajustes = input("Desea Ajustar parametros a YoloV5(si/no): ")
       
        Respuesta = Ajustes.casefold()

        while 1 :
            if Respuesta == "si" :
                print("Ajustes".center(50, "*"))
                model.conf = float(input("Confidence Threshold(0-1): "))
                model.iou = float(input("NMS IoU threshold (0-1): "))
                model.classes = tuple(map(int, input(f"Clases Seleccionadas (0-{len(names)}): ").split(",")))

                model.agnostic = bool(input("NMS class-agnostic: "))  # NMS class-agnostic
                model.multi_label = bool(input("NMS multiple labels per box: "))  # NMS multiple labels per box
                model.max_det = int(
                    input("Maximum number of detections per image: "))  # maximum number of detections per image
                model.amp = bool(
                    input("Automatic Mixed Precision (AMP) inference: "))  # Automatic Mixed Precision (AMP) inference
                model.to("cuda")
                print("\n")
                break

            if Respuesta == "no" :
                print("Ajustes".center(50, "*"))
                print("Ajustes Predeterminados Seleccionados...\n")
                model.conf = 0.5  # confidence threshold (0-1)
                model.iou = 0.5  # NMS IoU threshold (0-1)
                model.classes = 0, 50
                model.agnostic = False  # NMS class-agnostic
                model.multi_label = False  # NMS multiple labels per box
                model.max_det = 100  # maximum number of detections per image
                model.amp = False  # Automatic Mixed Precision (AMP) inference
                model.to("cuda")
                print("\n")
                break
            Ajustes = input("Escribir \'si\' o \'no\': ")
            Respuesta = Ajustes.casefold()
         """
        """----------------------------------------------------------"""
        print("Ajustes".center(50, "*"))
        print("Ajustes Predeterminados Seleccionados...\n")
        model.conf = 0.5  # confidence threshold (0-1)
        model.iou = 0.5  # NMS IoU threshold (0-1)
        model.classes =  0,46,47,49,50,51
        model.agnostic = False  # NMS class-agnostic
        model.multi_label = False  # NMS multiple labels per box
        model.max_det = 100  # maximum number of detections per image
        model.amp = False  # Automatic Mixed Precision (AMP) inference
        model.to("cuda")
        print("\n")        

    """Funcion de prueba para poder visualizar que todos los procesos de la raspberry se enciendan"""
    def InicializacionForzadaProcesos(self):
        for i in range(1,10):  
         self.Trigger(i,0)
         print(i)
     
    """Funcion encargada de mandar la seña de corte siempre que se cumpla la condicion de la distancia que ha recorido el implemento"""
    def CorteConPila(self,velocidad, pilaD, distancia) :
        if pilaD[len(pilaD)-1]!=0: 
           #señal =(Distancia a al que detecto el brocoli)+(Distancia a la que esta el centro de la cuchilla y el centro de LA Camara)-((latencia del piston)*Velovidad del implementos)  
            senal_distancia_activacion=(pilaD[1]+0.47-(0.015*velocidad))
            ### El 0.22 es un valor para evitar falsos positivos de activacion
            if senal_distancia_activacion<distancia and distancia>(pilaD[1]+0.22):
                print("cortar brocoli")
                #solo cuando este conectado para evitar que se tarde el programa en funcionar
                #self.Trigger(self.puerto_piston,1)
                #self.Trigger(self.puerto_piston,0)
                pilaD.pop(1)
                return pilaD
        return pilaD
    
    
    """ Funcion que controla los trigger de la comunicacion de la RaspBerry mediante el protocolo de Modbus"""
    def Trigger(self,elemento,accion):
        try:
            modbusClient = ModbusClient('192.168.100.10', 502)
            modbusClient.connect()
            modbusClient.write_single_coil(elemento, accion) #cambiar despues por el Trigger para cortar el brocoli
            modbusClient.close() 
        except:
            print("la Raspberry no esta conectado o esta en otra red")
            
            
    """Primera funcion para poder determinar la velcidad a la que va el implemento"""
    def VelocidadPrueba(self,puntosXY, tiempo, distancia) :
        dist = 0
        veloc = 0
        temp = 0
        dist = math.sqrt((puntosXY[1][0] - puntosXY[0][0]) ** 2 + (puntosXY[1][1] - puntosXY[0][1]) ** 2)
        temp = distancia * 0.25 / 100
        veloc = dist * temp / tiempo
        if veloc >= 1 :
            print("distancia:", dist * temp, "cm")
            print("Velocidad del objeto", veloc, "cm/s")
            return veloc
        return 0
    
    
    """Funcion que arroga el tamaño aproximado de bede de tener el brocoli en funcion a la cantidad de pixeles que hay"""
    def TamanoBrocoli(self,diamtro_pixeles, distancia) :
        tam = 0
        dista1 = diamtro_pixeles[1] - diamtro_pixeles[0]
        dista2 = diamtro_pixeles[3] - diamtro_pixeles[2]
        tamPix = distancia * 0.25 / 100
        tam = tamPix * dista1
        tam2 = tamPix * dista2
        return tam, tam2

    """Funcion que nos dice a que distancia promedio que hay del borcoli y la camara tomando en cuenta los puntos centrales del brocoli """
    def distancia_promedio_del_brocoliCamara(self,tam, mean, depth) :
        vec = []
        contj = tam
        while contj >= -tam :
            conti = tam
            while conti >= -tam :
                vec.append(depth[mean[0] + conti, mean[1] + contj])
                conti -= 1
            contj -= 1
        return vec
    
    
    """Funcion que calcula la velocidad en funcion de la aceleracion del acelerometro"""
    def Velocidad(self,ruido, accel, accelA, sumaAnte, tiempo) :
        tiempo = tiempo - time.time()
        suma = (sumaAnte + accel + accelA - 2 * ruido) * (tiempo / 2)
        vel = abs((suma - sumaAnte) / tiempo)
        return vel, accel, suma, time.time()
    
    
    """Funcion utilizada para calcular el ruido que nos proporciona el acelerometo  para asi consegui una señal mas limpia"""
    def ruido(self) :
        dc = DepthCamera(self.serial_number[self.puerto_camara])
        tiempo = time.time()
        ruido = []
        while (time.time() - tiempo) <= 2 :
            ret2, depth_frame, color_frame, accel = dc.get_frame()
            ruido.append(accel[1])
        ruido = sum(ruido) / len(ruido)
        return ruido
    
    
    """Funcion utilizada para guarda de manera temporal """
    def busqueda(self) :
        cont = 1
        try :
            while True :
                ar = open(f'Documentos\corte_{cont}.txt')
                cont += 1
                ar.close()
        except Exception :
            pass
        return cont


    """Programa Principal"""
    def main(self,BroccoliAcceptedSizes,rango) :

        print("Confirmacion Tamaño de Brocolis: ", BroccoliAcceptedSizes)
        print("Laseres Encendidos")
        print("Iniciando Programa".center(50, "*"))
        print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")
        
        CameraOpen_StartingTime = time.time()
        
        """Llamada al metodo para la camara acceder a los datos de profundida de la camara"""
        dc = DepthCamera(self.serial_number[self.puerto_camara])  
        camara = cv2.VideoCapture(self.puerto_camara)
        camara, h, w = self.CamaraSettings(camara)
        
        print("Ancho: ", w, "Alto: ", h)

        # Variables y Constantes iniciadas
        BroccoliSizeMin, BroccoliSizeMax = BroccoliAcceptedSizes
        Rangominimo,RangoMaximo=rango

        x1 = x2 = y1 = y2 = xmean = ymean = None
        showImageFlag = False
        NumberOfSlots = 20
        bAnt = NumberOfSlots * [0]
        bAct = NumberOfSlots * [0]
        AnalysisPictureFlag = 0
        BroccolisCounter = 0
        BroccolisCut=0
        tiempos = []
        endVideo = False
        h2 = int(h / 2)
        w2 = int(w / 2)
        intentosReconexion = 0
        intentosDeReconexionAceptados = 5
        CamaraOpenTimeFlag = True
        pila_distancia_recorrida = [0]
        distance = []
        tamano_RealX = 0
        tamano_RealY = 0
        accel_ant = sumaA = vel = 0
        tiempo = 0
        cont = self.busqueda()
        distancia = 0
       # Archivo = open(f'Documentos\corte_{cont}.txt', "w")
        calibresBrocolis={
            "menor":"Menor14",
            14:"Cant_14",
            15:"Cant_15",
            16:"Cant_16",
            17:"Cant_17",
            18:"Cant_18",
            19:"Cant_19",
            20:"Cant_20",
            21:"Cant_21",
            22:"Cant_22",
            23:"Cant_23",
            24:"Cant_24",
            25:"Cant_25",
            26:"Cant_26",
            27:"Cant_27",
            28:"Cant_28",
            29:"Cant_29",
            30:"Cant_30",
            "mayor":"Mayor30",
            }
        # Setup Modelo YOLOV5
        names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                 'frisbee',
                 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                 'surfboard',
                 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                 'cell phone',
                 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                 'teddy bear',
                 'hair drier', 'toothbrush']

        model = torch.hub.load(r'yolov5-master', 'custom', 'yolov5m6.pt', source='local')
        self.AjustesYoloV5(model, names)
        # Escritor de Video
        tiempo = time.time()
        vec = []
        while (time.time() - tiempo) <= 5 :
            accel = dc.accel_data()
            vec.append(accel[1])
        fondo = sum(vec) / len(vec)
        
        tiempo = 0
        #Archivo.write(f'{datetime.now().strftime("%d/%b/%Y")}  {datetime.now().strftime("%H:%M %p")}\n')
        #Archivo.write('*********************************************************************************\n')
        Videoresult = cv2.VideoWriter(r'Cam1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (int(w), int(h)))
        if camara.isOpened() :
            if CamaraOpenTimeFlag :  # sirve para poder mostrar el tiempo que tardado en la configuracion de todas sus parates
                CameraOpen_EndingTime = time.time()
                print("Tiempo de Inicio: ", CameraOpen_EndingTime - CameraOpen_StartingTime)
                CamaraOpenTimeFlag = False
            while 1:

                distancia = distancia + vel * (time.time() - tiempo)
                TimePerFrame_StartingPoint = time.time()
               

                """octencion de vector rgb, profundida y datos del acelerometo"""
                
                ret, depth_frame, frame, accel = dc.get_frame()
                
                """**************Velocidad********************"""
                
                vel, accel_ant, sumaA, tiempo = self.Velocidad(fondo, accel[1], accel_ant, sumaA, tiempo)
                
                """******************Validacion de la coneccion de la camara*************************"""
                while ret == False :
                    if intentosReconexion < intentosDeReconexionAceptados :
                        intentosReconexion += 1
                        print(f"Intentando Reconexion...\nIntento #{intentosReconexion}/5")
                        ret, frame, camara = self.ConexionCamara()
                        if ret == True :
                            print("Conexion Restablecida")
                            intentosReconexion = 0
                        time.sleep(5)
                    else :
                        print("Numero de Intentos Excedidos, Cerrando Programa...")
                        endVideo = True
                        break
                if endVideo == True :
                    break
                
                
                # Lector de FPS
                fps = camara.get(cv2.CAP_PROP_FPS)
                # print(fps)
                
                # Correccion de imagen
                frame = cv2.flip(frame, 1)
                # Ingreso del frame al modelo para analizar
                results = model(frame, size=640)
                # Obtencion de nombre y posicion del objeto detectado
                labels = cord = results.xyxyn[0][:, :-1]
                classes = labels.tolist()
                infoPandas = results.pandas().xyxy[0]
                # Numero de objetos detectados en el video
                objetosEnVideo = len(cord)
                #print(classes[0])
                # Muestra los BBs en el frame actual
                Bb = np.squeeze(results.render())
                # ***Ajustes de Lineas Visuales de los Bigotes de Gato***

                if showImageFlag == True :
                    frame[0 :200, 0 :200] = lastImageTaken

                # Muestra de Numero de objetos detectados en el Frame
                # cv2.putText(frame, f'No. de Objetos: {objetosEnVideo}', (w-340, h-28), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 255, 124), 2)
    
                """Datos de visualisacion"""
                cv2.putText(frame, f"Brocolis Cortados:{BroccolisCut}", (w - 280, h - 38), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 230, 124), 2)
                cv2.putText(frame, f"Brocolis Contados:{BroccolisCounter}", (w - 280, h - 68), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 124), 2)
                cv2.putText(frame, f'Fecha: {datetime.now().strftime("%d/%b/%Y")}', (10, h - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 124), 2)
                cv2.putText(frame, f'Hora: {datetime.now().strftime("%H:%M %p")}', (10, h - 68), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 124), 2)
                
                cv2.line(frame, (int(2 * w / 3), h), (int(2 * w / 3), 0), (255, 0, 0), 1)
                cv2.line(frame, (int(w / 3), h), (int(w / 3), 0), (255, 0, 0), 1)
                cv2.line(frame, (0, int(h / 2)), (w, h2), (0, 0, 220), 1)
                cv2.line(frame, (w2, h), (w2, 0), (0, 0, 220), 1)
                
                
                for j in range(0, objetosEnVideo) :
                    
                    # ***Obtencion de datos del BoundingBox***
                    x1 = int(cord[j][0] * w)
                    y1 = int(cord[j][1] * h)
                    x2 = int(cord[j][2] * w)
                    y2 = int(cord[j][3] * h)
                    xmean = int((x1 + x2) / 2)
                    ymean = int((y1 + y2) / 2)
                    pixeles=x2-x1
                    
                    if y2 < 480 and x2 < 848 :
                        distance = self.distancia_promedio_del_brocoliCamara(5, (ymean, xmean), depth_frame)
                        promedio = 0
                        cont = 0
                        # sacar el promedio de la distancia
                        for i in range(0, len(distance)) :
                            if distance[i] != 0 :
                                cont += 1
                                promedio += distance[i]
                        if cont == 0 :
                            tamano_RealX = tamano_RealY = 0
                        else :
                            promedio = int((promedio / cont) / 10)
                            tamano_RealX, tamano_RealY = self.TamanoBrocoli(([x1, x2, y1, y2]), promedio)
                        cv2.putText(frame, "{}cm".format(promedio), (x2, y2 - 20), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 2)
                        cv2.putText(frame, "tam:{:.2f}".format(tamano_RealX), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 255), 1)
                        distance.clear()
                    tamano_RealX=round(tamano_RealX)
                    if tamano_RealX >= BroccoliSizeMin and tamano_RealX <= BroccoliSizeMax :
                        cv2.ellipse(frame, (xmean, ymean), (int((x2 - x1) / 2), int((y2 - y1) / 2)), 0, 0, 360,(60, 255, 51), 2)
                        ban = True
                    else :
                        cv2.ellipse(frame, (xmean, ymean), (int((x2 - x1) / 2), int((y2 - y1) / 2)), 0, 0, 360,(0, 0, 255), 2)
                        ban = False
                    tamano_RealX=round(tamano_RealX)
                    cv2.circle(frame, (xmean, ymean), 3, (0, 0, 255), -1)
                    cv2.circle(frame, (x2, ymean), 3, (0, 0, 255), -1)
                    cv2.circle(frame, (xmean, y1), 3, (0, 0, 255), -1)
                    cv2.circle(frame, (x1, ymean), 3, (0, 0, 255), -1)
                    cv2.circle(frame, (xmean, y2), 3, (0, 0, 255), -1)
                    if ymean < h2 and ymean < h2 + 50 :
                        if x1 > (w / 3) and x2 < (2 * w / 3 - 1) :
                            bAct[j] = 1
                    else :
                        bAct[j] = 0
                  
                suma = sum(bAct) - sum(bAnt)
               
                if suma > 0:
                    dateOfDetection = datetime.now()
                    AnalysisPictureFlag = 1
                    BroccolisCounter += 1
                    idBroc = BroccolisCounter
                    #Archivo.write(f"Brocoli: {BroccolisCounter}  tamaño x:{bro[j][0]:.2f}  tamaño Y: {bro[j][1]:.2f}\n")
                    #Archivo.write(f"Brocoli: {BroccolisCounter}  tamaño x:{tamano_RealX}")
                    if ban:
                        self.ConexionBaseDatos.Incremento(calibresBrocolis[tamano_RealX], 7)
                        self.ConexionBaseDatos.Incremento("CantidadCortada", 7)
                        if (tamano_RealX<=Rangominimo and tamano_RealX<=RangoMaximo):
                            pila_distancia_recorrida.append(distancia)
                            BroccolisCut+=1
                    else:
                        if tamano_RealX<BroccoliSizeMin:
                            self.ConexionBaseDatos.Incremento(calibresBrocolis["menor"], 7)
                            self.ConexionBaseDatos.Incremento("CantidadPorDebajo", 7)
                        else:
                            self.ConexionBaseDatos.Incremento(calibresBrocolis["mayor"], 7) 
                            self.ConexionBaseDatos.Incremento("CantidadPorEncima", 7)
                    self.ConexionBaseDatos.Incremento("CantidadObservada", 7)
                bAnt = bAct.copy()
                pila_distancia_recorrida = self.CorteConPila(vel, pila_distancia_recorrida, distancia)
            
                cv2.namedWindow(f"{self.names_Ca}", cv2.WINDOW_NORMAL)
                cv2.imshow(f"{self.names_Ca}", frame)
                self.trasmision_api=frame
                Videoresult.write(frame)
                

                # ***Datos de Medidas de Dispersion***
                if cv2.waitKey(1) == ord("s") :
                    print("Tiempos de Procesamiento".center(50, "*"))
                    print("Valor MAX: ", max(tiempos))
                    print("Valor MIN: ", min(tiempos))
                    print("Rango: ", max(tiempos) - min(tiempos))
                    print("Promedio: ", np.mean(tiempos))
                    print("Desviacion Standar: ", np.std(tiempos))
                    print("Varianza: ", np.var(tiempos))
                    break
                
                timeProcessing = time.time() - TimePerFrame_StartingPoint

                tiempos.append(timeProcessing)
            #Archivo.close()
            camara.release()
            Videoresult.release()
            #dc.release()
            cv2.destroyAllWindows()
        else :
            print("Conectar Cámara para arranque")

    """Metodo de trasmision a la api"""
    def conversion_frame(self):
        while 1:
            ret, buffer = cv2.imencode('.jpg', self.trasmision_api)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

obj=Vision_1()

"""@app.route("/inicio")
def inicio():
    #Esta condicional inicializa el main() con los parametros de trabajo(rango de tamaño de cabezas) definido manualmente en codigo o recuperado de la base de datos     
    obj.main([14,30])
@app.route("/stream")
def stream():
    return Response(obj.conversion_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ =="__main__":
    app.run(host='0.0.0.0', debug=False)"""