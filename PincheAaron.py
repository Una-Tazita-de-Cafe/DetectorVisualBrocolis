from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
class Conexion:
    
    def Trigger(self, activacion):
        try:
            """
            modbusClient = ModbusClient('10.42.0.1', 5020)
            modbusClient.connect()
            modbusClient.write_single_coil(activacion, 0)
          
            modbusClient.close()
            modbusClient = ModbusClient('10.42.0.1', 5020)
            modbusClient.connect()
            modbusClient.write_single_coil(activacion, 1)
          
            modbusClient.close()
            
            """
            client = ModbusClient("192.168.0.115", 5020)
            client.write_coil(6, 0) #gpio 16
            client.write_coil(7, 1) #gpio 26
            client.write_coil(6, 1) #gpio 16
            client.write_coil(7, 0) #gpio 26
            client.close() 
        except:
            print("aduino no detectado")
    def Activacion(self):
        print("************Escribe*************")
        while 1:
            dispositivo=int(input("Trigger a modificar \n"))
            self.Trigger(dispositivo)
            respuesta=input("seguir testeando no (n) \n")
            if respuesta=="n":
                break
    def Prueba_Latencia(self):
        for i in range(0,1200):
            self.Trigger(6)
            time.sleep(0.5)
            
if __name__=="__main__":
    obj=Conexion() 
    obj.Prueba_Latencia()