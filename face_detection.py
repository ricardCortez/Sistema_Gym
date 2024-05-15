import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN

class FaceDetector:
    def __init__(self):
        # Inicializa el detector MTCNN y el reconocedor de rostros LBPH
        self.detector = MTCNN()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def detect_faces(self, img):
        """Detecta rostros en una imagen usando MTCNN."""
        return self.detector.detect_faces(img)

    def train_recognizer(self, images, labels):
        """Entrena el reconocedor de rostros con las imágenes y etiquetas proporcionadas."""
        self.recognizer.train(images, np.array(labels))
        self.recognizer.save('trained_model.xml')  # Guarda el modelo entrenado

    def recognize_face(self, face_img):
        """Reconoce el rostro en la imagen proporcionada."""
        label, confidence = self.recognizer.predict(face_img)
        return label, confidence

    def process_image(self, img_bytes):
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        faces = self.detect_faces(img)
        results = []
        for face in faces:
            x, y, width, height = face['box']
            face_img = img[y:y + height, x:x + width]
            label, confidence = self.recognize_face(face_img)
            # Asegúrate de que 'label' y 'confidence' no estén causando el problema
            results.append({'label': label, 'confidence': confidence, 'box': (x, y, width, height)})

        return results

