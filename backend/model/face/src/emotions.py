import numpy as np
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.preprocessing.image import img_to_array


class EmotionDetector:
    def __init__(
        self, model_path="model.h5", cascade_path="haarcascade_frontalface_default.xml"
    ):
        self.model = self.load_model(model_path)
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.emotion_dict = {
            0: "Angry",
            1: "Disgusted",
            2: "Fearful",
            3: "Happy",
            4: "Neutral",
            5: "Sad",
            6: "Surprised",
            "No Face": "No Face",
        }

    def load_model(self, model_path):
        model = Sequential(
            [
                Conv2D(
                    32, kernel_size=(3, 3), activation="relu", input_shape=(48, 48, 1)
                ),
                Conv2D(64, kernel_size=(3, 3), activation="relu"),
                MaxPooling2D(pool_size=(2, 2)),
                Dropout(0.25),
                Conv2D(128, kernel_size=(3, 3), activation="relu"),
                MaxPooling2D(pool_size=(2, 2)),
                Conv2D(128, kernel_size=(3, 3), activation="relu"),
                MaxPooling2D(pool_size=(2, 2)),
                Dropout(0.25),
                Flatten(),
                Dense(1024, activation="relu"),
                Dropout(0.5),
                Dense(7, activation="softmax"),
            ]
        )
        model.load_weights(model_path)
        return model

    def detect_emotions(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        emotion_counts = {emotion: 0 for emotion in self.emotion_dict.values()}
        processed_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed_frames += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5
            )

            if len(faces) == 0:
                emotion_counts["No Face"] += 1

            for x, y, w, h in faces:
                roi_gray = gray[y : y + h, x : x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                roi_gray = roi_gray.astype("float") / 255.0
                roi_gray = img_to_array(roi_gray)
                roi_gray = np.expand_dims(roi_gray, axis=0)
                roi_gray = np.expand_dims(roi_gray, axis=-1)

                prediction = self.model.predict(roi_gray)[0]
                max_index = np.argmax(prediction)
                emotion = self.emotion_dict[max_index]
                emotion_counts[emotion] += 1

            print(f"Processing: {processed_frames / total_frames * 100:.1f}%", end="\r")

        cap.release()

        # Convert duration to seconds based on fps
        for emotion, count in emotion_counts.items():
            duration_seconds = count / fps
            emotion_counts[emotion] = duration_seconds

        return emotion_counts

    def detect_emotions_to_json(self, video_path):
        emotion_counts = self.detect_emotions(video_path)
        print(emotion_counts)
        return emotion_counts


