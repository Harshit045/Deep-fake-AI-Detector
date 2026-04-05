from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from PIL.ExifTags import TAGS
import os
import io

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

# ---------------- LOAD MODEL ----------------
if os.path.exists("deepfake_cnn_model.h5"):
    model = load_model("deepfake_cnn_model.h5", compile=False)
else:
    model = None
    print("WARNING: deepfake_cnn_model.h5 not found! Please place the file in this directory.")

# Use OpenCV's built-in path to ensure the cascade XML always loads properly
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# ---------- AI Artifact Detection ----------
def detect_ai_artifacts(image):
    """
    Returns (ai_score, is_filtered, is_ai_gen).
    Uses Advanced Forensics: Error Level Analysis (ELA) & Sensor Noise.
    """
    score = 0.0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 1. Sensor Noise Analysis (Median Blur diff)
    # Real cameras produce high-frequency noise. AI/Filters destroy this.
    blurred = cv2.medianBlur(gray, 3)
    noise_diff = cv2.absdiff(gray, blurred)
    noise_mean = np.mean(noise_diff)
    print(f"Debug - Sensor Noise Mean: {noise_mean:.2f}")

    is_filtered = False
    is_ai_gen = False

    if noise_mean < 1.5:  
        score += 0.35
        is_filtered = True
    elif noise_mean < 2.2:
        score += 0.1

    # 2. Error Level Analysis (ELA) Simulator
    # Identifies digital generation & synthetic patterns.
    _, encoded_img = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    compressed_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    ela_diff = cv2.absdiff(image, compressed_img)
    ela_mean = np.mean(ela_diff)
    print(f"Debug - ELA Mean: {ela_mean:.2f}")

    if ela_mean > 8.0:
        score += 0.3
        is_ai_gen = True

    # 3. Edge / Over-sharpening Check (Common in Midjourney/ChatGPT)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"Debug - Laplacian Variance: {laplacian_var:.2f}")
    if laplacian_var > 1500: # Increased threshold for high-res DSLR images
        score += 0.3
        is_ai_gen = True
    elif laplacian_var < 50:
        score += 0.25
        is_filtered = True

    # 4. Impossible Sharpness (AI Signature)
    # AI generates hyper-sharp edges but lacks microscopic sensor noise
    if laplacian_var > 800 and noise_mean < 1.0: # Relaxed for real high-res images
        score += 0.4
        is_ai_gen = True
        print("Debug - AI Signature: High Sharpness + Zero Noise detected")

    # 5. Color Saturation (AI often generates hyper-vibrant images)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation_mean = np.mean(hsv[:, :, 1])
    print(f"Debug - Saturation Mean: {saturation_mean:.2f}")
    if saturation_mean > 135:
        score += 0.15

    return min(score, 1.0), is_filtered, is_ai_gen


# ---------- Metadata Check ----------
def check_metadata(file_bytes):
    try:
        img = Image.open(io.BytesIO(file_bytes))
        exif = img.getexif() if hasattr(img, 'getexif') else (img._getexif() if hasattr(img, '_getexif') else None)

        if not exif:
            return "UNKNOWN"

        has_camera_make = False
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag in ["Make", "Model"]:
                has_camera_make = True
            elif tag == "Software":
                v = str(value).lower()

                if any(x in v for x in ["ai", "stable", "diffusion", "midjourney", "dall"]):
                    return "AI"

        return "CAMERA" if has_camera_make else "UNKNOWN"

    except:
        return "UNKNOWN"


@app.route("/")
def home():
    return app.send_static_file('index.html')


# ---------- MAIN API ----------
@app.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_bytes = file.read()

    np_img = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ai_score, is_filtered, is_ai_gen = detect_ai_artifacts(img)
    metadata = check_metadata(file_bytes)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        if metadata == "AI" or ai_score >= 0.65 or is_ai_gen:
            return jsonify({
                "deepfake_score": 0.0,
                "ai_score": round(ai_score, 3),
                "metadata": metadata,
                "final_verdict": "AI_GENERATED",
                "reason": "Image forensic patterns indicate AI generation (No face in image)."
            })
        elif ai_score <= 0.25 and metadata == "CAMERA":
            return jsonify({
                "deepfake_score": 0.0,
                "ai_score": round(ai_score, 3),
                "metadata": metadata,
                "final_verdict": "REAL_CAMERA",
                "reason": "Natural sensor noise and normal compression detected (No face in image)."
            })
            
        return jsonify({
            "deepfake_score": 0.0,
            "ai_score": round(ai_score, 3),
            "metadata": metadata,
            "final_verdict": "SUSPICIOUS",
            "reason": "No face detected. Image lacks clear AI signs but may be edited or filtered."
        })

    x, y, w, h = faces[0]

    face = img[y:y+h, x:x+w]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = face / 255.0
    face = np.expand_dims(face, axis=0)

    # ---------- MODEL PREDICTION ----------
    if model is None:
        return jsonify({"error": "Deepfake model not found on server. Please place deepfake_cnn_model.h5 in the backend directory."}), 500

    deepfake_score = float(model.predict(face, verbose=0)[0][0])

    print("Deepfake score:", deepfake_score)
    print("AI artifact score:", ai_score)

    reason = "Analysis complete."
    verdict = "SUSPICIOUS" # Default to suspicious

    # ---------- FINAL DECISION ----------
    if metadata == "AI":
        verdict = "AI_GENERATED"
        reason = "Image metadata explicitly states it was generated by AI software."
        
    elif ai_score >= 0.6 or is_ai_gen:
        verdict = "AI_GENERATED"
        reason = "Forensic analysis shows zero sensor noise or hyper-sharp edges typical of AI generation."
        
    elif deepfake_score > 0.85 and ai_score > 0.35:
        verdict = "DEEPFAKE"
        reason = "CNN detected a manipulated face AND forensic artifacts match Deepfake patterns."
        
    elif is_filtered and deepfake_score > 0.25:
        verdict = "EDITED_OR_FILTERED"
        reason = "Low sensor noise detected. Image likely has beauty filters, skin smoothing, or digital edits."

    elif deepfake_score > 0.85 and ai_score <= 0.3:
        verdict = "SUSPICIOUS"
        reason = "Face model flagged as fake, but physics look REAL. Could be a CNN mistake on a high-quality photo."

    # This is the key change: A more robust "REAL" check
    elif deepfake_score < 0.4 and ai_score < 0.3 and not is_ai_gen:
        verdict = "REAL_CAMERA"
        reason = "Low deepfake score and no strong AI indicators found. Image appears authentic."

    elif is_filtered:
        verdict = "EDITED_OR_FILTERED"
        reason = "Image shows signs of filtering or smoothing, but is not a clear deepfake."

    else:
        verdict = "SUSPICIOUS"
        reason = "Scores are ambiguous. Minor edits or filters might be present."

    return jsonify({
        "deepfake_score": round(deepfake_score, 3),
        "ai_score": round(ai_score, 3),
        "metadata": metadata,
        "final_verdict": verdict,
        "reason": reason
    })


if __name__ == "__main__":
    # Set debug=False and host='0.0.0.0' for external access during deployment
    app.run(debug=False, host='0.0.0.0')