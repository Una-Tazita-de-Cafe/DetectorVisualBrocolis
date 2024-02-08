import cv2

# Abre la primera cámara (cámara 0)
cap1 = cv2.VideoCapture(0)

# Abre la segunda cámara (cámara 1)
cap2 = cv2.VideoCapture(2)

while True:
    # Lee un cuadro de la primera cámara
    ret1, frame1 = cap1.read()
    
    # Lee un cuadro de la segunda cámara
    ret2, frame2 = cap2.read()
    
    # Si la lectura es exitosa, muestra las imágenes
    if ret1:
        cv2.imshow('Cámara 1', frame1)
        cv2.imshow('Cámara 2', frame2)

    # Presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra las ventanas
cap1.release()
cap2.release()
cv2.destroyAllWindows()