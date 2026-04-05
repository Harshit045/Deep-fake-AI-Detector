import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from PIL.ExifTags import TAGS
import os

# -------------------------
# Load Models
# -------------------------
model = load_model("deepfake_cnn_model.h5")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# -------------------------
# AI Generated Detection (Simple Heuristics)
# -------------------------
def detect_ai_artifacts(image):
    """
    Returns ai_score between 0 and 1
    0 = looks like real camera
    1 = strongly AI generated
    """
    ai_score = 0.0
    h, w, _ = image.shape

    # Very smooth image → AI tendency
    blur = cv2.GaussianBlur(image, (21,21), 0)
    diff = cv2.absdiff(image, blur)
    score = np.mean(diff)
    if score < 10:
        ai_score += 0.3

    # Too perfect symmetry check
    left = image[:, :w//2]
    right = cv2.flip(image[:, w//2:], 1)
    if left.shape == right.shape:
        symmetry = np.mean(cv2.absdiff(left, right))
        if symmetry < 15:
            ai_score += 0.3

    # Too uniform lighting
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    std = np.std(gray)
    if std < 25:
        ai_score += 0.2

    return min(ai_score, 1.0)


# -------------------------
# Metadata Check
# -------------------------
def check_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return "UNKNOWN"

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "Software":
                val = str(value).lower()
                if any(x in val for x in ["stable", "diffusion", "midjourney", "dall", "ai"]):
                    return "AI"
        return "CAMERA"
    except:
        return "UNKNOWN"


# -------------------------
# Load Image
# -------------------------
img_path = "0L1IDFAHRA.jpg"   # yahan apni test image ka naam daal
img = cv2.imread(img_path)

if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -------------------------
# Face Detection (Strict)
# -------------------------
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=7,
    minSize=(100, 100)
)

if len(faces) == 0:
    print("No face detected")
    print("Result: SUSPICIOUS")
    exit()

# Sirf first face use karenge
(x, y, w, h) = faces[0]
face = img[y:y+h, x:x+w]
face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
face = cv2.resize(face, (224, 224))
face = face / 255.0
face = np.expand_dims(face, axis=0)

# -------------------------
# Deepfake Prediction
# -------------------------
deepfake_score = model.predict(face)[0][0]
print("Deepfake score:", deepfake_score)

# -------------------------
# AI Generated Detection
# -------------------------
ai_score = detect_ai_artifacts(img)
print("AI Artifact score:", ai_score)

# -------------------------
# Metadata
# -------------------------
meta_result = check_metadata(img_path)
print("Metadata:", meta_result)

# -------------------------
# Final Decision Logic
# -------------------------
if deepfake_score > 0.65:
    final_result = "DEEPFAKE"
elif ai_score > 0.65 or meta_result == "AI":
    final_result = "AI_GENERATED"
elif deepfake_score < 0.35 and ai_score < 0.35 and meta_result == "CAMERA":
    final_result = "REAL_CAMERA"
else:
    final_result = "SUSPICIOUS"

print("\n==============================")
print("FINAL FORENSIC RESULT:", final_result)
print("==============================")

# -------------------------
# Display Result
# -------------------------
cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
cv2.putText(img, final_result, (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

cv2.imshow("Digital Image Forensic System", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
