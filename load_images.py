import os
import cv2

real_folder = "dataset/deepfake/real"
fake_folder = "dataset/deepfake/fake"

# Real images
print("Loading REAL images:")
for file in os.listdir(real_folder):
    img_path = os.path.join(real_folder, file)
    img = cv2.imread(img_path)
    if img is not None:
        print(f"Loaded: {file}")

# Fake images
print("\nLoading FAKE images:")
for file in os.listdir(fake_folder):
    img_path = os.path.join(fake_folder, file)
    img = cv2.imread(img_path)
    if img is not None:
        print(f"Loaded: {file}")
