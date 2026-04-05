import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("deepfake_cnn_model.h5")  # ya .h5

img_path = "56353.jpg"   # yahan koi bhi new image daalna
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (224, 224))
img = img / 255.0
img = np.expand_dims(img, axis=0)

prediction = model.predict(img)[0][0]

if prediction > 0.65:
    print("Fake Image")
elif prediction < 0.35:
    print("Real Image")
else:
    print("Suspicious / Needs Human Verification")

print("Confidence:", prediction)
