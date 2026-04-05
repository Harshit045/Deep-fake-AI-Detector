import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load models
model = load_model("deepfake_cnn_model.h5")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load image
img_path = "Snapchat-2123404253.jpg"
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=7,
    minSize=(100, 100)
)

if len(faces) == 0:
    print("No face detected.")
else:
    for (x, y, w, h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)

        prediction = model.predict(face)[0][0]
        print("Raw prediction:", prediction)

        if prediction > 0.65:
            result = "Fake Image"
        elif prediction < 0.35:
            result = "Pure / Real Image"
        else:
            result = "Suspicious (Needs Human Verification)"

        print("Result:", result)

        # Show detection
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(img, result, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("AI Deepfake Detection System", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
