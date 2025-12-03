import cv2
import serial
import time
import os


arduino = serial.Serial('COM4', 9600)
time.sleep(2)  


cascade_path = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(cascade_path)


def procesar_imagen(ruta_imagen: str):
    if not os.path.exists(ruta_imagen):
        print(f"ERROR: La imagen '{ruta_imagen}' no existe en la carpeta.")
        return

    img = cv2.imread(ruta_imagen)
    if img is None:
        print(f"ERROR: No se pudo leer la imagen '{ruta_imagen}'.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(faces) > 0:
        print(f"[{ruta_imagen}] → ROSTRO DETECTADO → Acceso correcto")
        arduino.write(b'1')
        mensaje = "Acceso correcto"
        color_rect = (0, 255, 0) 
    else:
        print(f"[{ruta_imagen}] → SIN ROSTRO → Acceso denegado")
        arduino.write(b'0')
        mensaje = "Acceso denegado"
        color_rect = (0, 0, 255)  

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), color_rect, 2)

    cv2.putText(
        img,
        mensaje,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color_rect,
        2,
        cv2.LINE_AA
    )

    cv2.imshow(f"Resultado - {ruta_imagen}", img)
    print("Presiona una tecla en la ventana de la imagen para continuar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


print("=== SISTEMA DE RECONOCIMIENTO CON IMÁGENES DE PRUEBA ===")
print("Coloca tus imágenes en la MISMA carpeta que este archivo (index.py).")
print("Ejemplos: rostro1.jpg, norostro1.jpg, etc.")
print("Escribe 'salir' para terminar.\n")

while True:
    nombre = input("Nombre del archivo de imagen (ej: rostro1.jpg) o 'salir': ").strip()

    if nombre.lower() == "salir":
        print("Finalizando programa...")
        break

    procesar_imagen(nombre)

arduino.close()