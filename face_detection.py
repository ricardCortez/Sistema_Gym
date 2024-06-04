from threading import Thread
from tqdm import tqdm
import cv2
import os
import time
import requests
import numpy as np


def process_image_data(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def capture_faces(image_data, codigo_unico, current_count):
    img = process_image_data(image_data)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Ajustar estos parámetros para optimizar la detección
    scale_factor = 1.1  # Disminuye este valor para aumentar la sensibilidad a rostros más pequeños
    min_neighbors = 5  # Aumenta este valor para reducir falsos positivos
    min_size = (50, 50)  # Tamaño mínimo del rostro a detectar
    max_size = (200, 200)  # Tamaño máximo del rostro a detectar

    faces = face_classifier.detectMultiScale(gray, scale_factor, min_neighbors, minSize=min_size, maxSize=max_size)
    path = f"/Sistema_gym/faces/{codigo_unico}"
    os.makedirs(path, exist_ok=True)

    count = current_count
    for (x, y, w, h) in faces:
        center_x, center_y = x + w // 2, y + h // 2
        margin = max(w, h) // 2
        x_new = max(center_x - margin, 0)
        y_new = max(center_y - margin, 0)
        w_new = min(2 * margin, gray.shape[1] - x_new)
        h_new = min(2 * margin, gray.shape[0] - y_new)
        face_image = gray[y_new:y_new + h_new, x_new:x_new + w_new]
        face_image = cv2.resize(face_image, (200, 200))
        cv2.imwrite(f"{path}/{count}.jpg", face_image)
        print(f"Imagen {count} guardada.")
        count += 1

    print(f"{count - current_count} imágenes capturadas en esta iteración, total capturadas: {count}")
    return count


def train_model():
    data_path = '/Sistema_gym/faces/'  # Asegúrate de que este directorio existe en tu proyecto
    model_directory = '/Sistema_gym/modelLBPHFace/'  # Carpeta para guardar el modelo entrenado
    model_path = os.path.join(os.getcwd(), model_directory)  # Ruta completa

    os.makedirs(model_path, exist_ok=True)  # Crea el directorio si no existe

    people_list = os.listdir(data_path)
    labels = []
    faces_data = []
    label = 0

    print("Comenzando el entrenamiento del modelo...")
    total_images = sum(len(os.listdir(os.path.join(data_path, person))) for person in people_list)
    progress_bar = tqdm(total=total_images, desc="Entrenando", unit="img")

    for personName in people_list:
        person_path = os.path.join(data_path, personName)
        for imageName in os.listdir(person_path):
            image = cv2.imread(os.path.join(person_path, imageName), cv2.IMREAD_GRAYSCALE)
            faces_data.append(image)
            labels.append(label)
            progress_bar.update(1)
        label += 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces_data, np.array(labels))
    face_recognizer.write(os.path.join(model_path, 'modelo_LBPHFace.xml'))  # Guarda el modelo en la ruta especificada
    progress_bar.close()
    print("Modelo entrenado y almacenado con éxito en:", model_path)


def send_validation_signal():
    try:
        response = requests.post('http://localhost:5000/api/face_validated')
        if response.status_code == 200:
            print("Señal de validación enviada correctamente.")
        else:
            print(f"Error al enviar la señal de validación: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la señal de validación: {e}")


def recognize_faces():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('/Sistema_gym/modelLBPHFace/modelo_LBPHFace.xml')
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Reconocimiento de Rostros", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Reconocimiento de Rostros", 640, 480)

    recognition_threshold = 50  # Umbral de confianza para considerar el reconocimiento positivo
    continuous_recognition_duration = 3  # Duración en segundos para validar reconocimiento

    start_time = None  # Iniciar el tiempo de seguimiento cuando se reconoce un rostro

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        recognized = False  # Flag para controlar si se ha reconocido algún rostro

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150))
            label, confidence = face_recognizer.predict(face)
            confidence = 100 - confidence

            if confidence > recognition_threshold:
                if start_time is None:
                    start_time = time.time()  # Marcar el inicio del reconocimiento continuo
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Confianza: {confidence:.2f}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)
                recognized = True
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "No reconocido", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if recognized and start_time and (time.time() - start_time) >= continuous_recognition_duration:
            print("Usuario validado exitosamente.")
            send_validation_signal()  # Enviar señal de validación
            break  # Salir del bucle y cerrar la ventana
        elif not recognized:
            start_time = None  # Reiniciar el contador si no hay rostros reconocidos o no cumplen el umbral

        cv2.imshow("Reconocimiento de Rostros", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# def async_capture_faces(image_data, face_id, start_count, num_samples=300):
#     thread = Thread(target=capture_faces, args=(image_data, face_id, start_count, num_samples))
#     thread.start()
#     return thread


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
