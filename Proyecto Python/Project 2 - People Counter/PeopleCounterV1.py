import cv2

# Cargar el clasificador de Haar para la detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la cámara
cap = cv2.VideoCapture(0)

# Configurar el ancho y alto de la ventana de captura
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Contar el número de personas
count = 0

while True:
    # Capturar un fotograma de la cámara
    ret, frame = cap.read()

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detección de rostros en la imagen en escala de grises
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Dibujar un rectángulo alrededor de cada rostro detectado y contar el número de rostros
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

    # Mostrar el número de personas en la pantalla
    cv2.putText(frame, 'Personas: {}'.format(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar la imagen en una ventana
    cv2.imshow('frame', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
