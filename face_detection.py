from threading import Thread
from tqdm import tqdm
import cv2
import os
import numpy as np


def capture_faces(face_id, num_samples=300):
    try:
        # Inicializa la cámara
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Error: La cámara no pudo ser activada.")

        # Crea el clasificador de rostros
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Crea el directorio para guardar las imágenes capturadas
        path = f"faces/{face_id}"
        os.makedirs(path, exist_ok=True)

        # Contador de rostros capturados
        count = 0
        cv2.namedWindow("Captura de Rostros", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Captura de Rostros", 640, 480)

        # Proceso de captura de rostros
        while count < num_samples:
            ret, frame = cap.read()
            if not ret:
                break

            # Aplica filtro Gaussiano para reducción de ruido
            frame_blurred = cv2.GaussianBlur(frame, (5, 5), 0)

            # Convierte a escala de grises para la detección de rostros y ecualización
            gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            # Detecta los rostros en la imagen
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_image = gray[y:y + h, x:x + w]
                face_image = cv2.resize(face_image, (150, 150))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imwrite(f"{path}/{count}.jpg", face_image)
                count += 1

            # Muestra el estado de la captura en la ventana
            cv2.putText(frame, f"Presione 'q' para salir. Imagenes Capturadas: {count}/{num_samples}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Captura de Rostros", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_samples:
                break

        # Cierra los recursos utilizados
        cap.release()
        cv2.destroyAllWindows()
        print(f"{count} imágenes capturadas y almacenadas en {path}")
        print("Rostro(s) capturado(s) con éxito.")

    except Exception as e:
        # Maneja cualquier excepción que ocurra durante la captura
        print(f"Se ha producido un error durante la captura de rostros: {str(e)}")
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()


def train_model():
    dataPath = 'faces/'
    peopleList = os.listdir(dataPath)
    labels = []
    facesData = []
    label = 0

    print("Comenzando el entrenamiento del modelo...")
    total_images = sum(len(os.listdir(os.path.join(dataPath, person))) for person in peopleList)
    progress_bar = tqdm(total=total_images, desc="Entrenando", unit="img")

    for personName in peopleList:
        personPath = os.path.join(dataPath, personName)
        for imageName in os.listdir(personPath):
            image = cv2.imread(os.path.join(personPath, imageName), cv2.IMREAD_GRAYSCALE)
            facesData.append(image)
            labels.append(label)
            progress_bar.update(1)  # Actualizar la barra de progreso por cada imagen procesada
        label += 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(facesData, np.array(labels))
    face_recognizer.write('modelo_LBPHFace.xml')
    progress_bar.close()  # Cerrar la barra de progreso al completar
    print("Modelo entrenado y almacenado con éxito.")


def recognize_faces():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modelo_LBPHFace.xml')
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Reconocimiento de Rostros", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Reconocimiento de Rostros", 640, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (150, 150))
            label, confidence = face_recognizer.predict(face)
            confidence = 100 - confidence

            if confidence < 50:  # Asumimos que menos del 50% de confianza es no reconocido
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "No reconocido", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Confianza: {confidence:.2f}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Reconocimiento de Rostros", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def async_capture_faces(face_id, num_samples=300):
    """Función para iniciar la captura de rostros en un hilo separado."""
    thread = Thread(target=capture_faces, args=(face_id, num_samples))
    thread.start()
    return thread


def async_train_model():
    """Función para iniciar el entrenamiento del modelo en un hilo separado."""
    thread = Thread(target=train_model)
    thread.start()
    return thread


def async_recognize_faces():
    """Función para iniciar el reconocimiento de rostros en un hilo separado."""
    thread = Thread(target=recognize_faces)
    thread.start()
    return thread


# Esto evitará que se ejecute código al importar
if __name__ == '__main__':
    capture_faces('example_id')
    train_model()
    recognize_faces()