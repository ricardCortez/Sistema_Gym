from threading import Thread

from flask_socketio import emit, SocketIO
from tqdm import tqdm
import cv2
import os
import numpy as np


def process_image_data(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def capture_faces(image_data, face_id, current_count, total_samples=300):
    img = process_image_data(image_data)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Ajustar estos parámetros para optimizar la detección
    scaleFactor = 1.1  # Disminuye este valor para aumentar la sensibilidad a rostros más pequeños
    minNeighbors = 5  # Aumenta este valor para reducir falsos positivos
    minSize = (30, 30)  # Tamaño mínimo del rostro a detectar
    maxSize = (200, 200)  # Tamaño máximo del rostro a detectar

    faces = face_classifier.detectMultiScale(gray, scaleFactor, minNeighbors, minSize=minSize, maxSize=maxSize)

    path = f"/Sistema_gym/faces/{face_id}"
    os.makedirs(path, exist_ok=True)

    count = current_count
    for (x, y, w, h) in faces:
        face_image = gray[y:y + h, x:x + w]
        face_image = cv2.resize(face_image, (150, 150))
        cv2.imwrite(f"{path}/{count}.jpg", face_image)
        count += 1
    print(f"{count} imágenes capturadas y almacenadas en {path}")
    return count


def train_model():
    dataPath = '/Sistema_gym/faces/'  # Asegúrate de que este directorio existe en tu proyecto
    modelDirectory = '/Sistema_gym/modelLBPHFace/'  # Carpeta para guardar el modelo entrenado
    modelPath = os.path.join(os.getcwd(), modelDirectory)  # Ruta completa

    os.makedirs(modelPath, exist_ok=True)  # Crea el directorio si no existe

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
            progress_bar.update(1)
        label += 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(facesData, np.array(labels))
    face_recognizer.write(os.path.join(modelPath, 'modelo_LBPHFace.xml'))  # Guarda el modelo en la ruta especificada
    progress_bar.close()
    print("Modelo entrenado y almacenado con éxito en:", modelPath)


def recognize_faces():
    # Definir la ruta completa al modelo
    model_path = '/Sistema_gym/modelLBPHFace/modelo_LBPHFace.xml'  # Asegúrate de que esta ruta sea accesible y correcta

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
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

            if confidence < 50:
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

def async_capture_faces(image_data, face_id, start_count, num_samples=300):
    thread = Thread(target=capture_faces, args=(image_data, face_id, start_count, num_samples))
    thread.start()
    return thread


def async_train_model():
    thread = Thread(target=train_model)
    thread.start()
    return thread


def async_recognize_faces():
    thread = Thread(target=recognize_faces)
    thread.start()
    return thread


if __name__ == '__main__':
    capture_faces('example_id', 0, 300)
    train_model()
    recognize_faces()