import os
import cv2
import numpy as np

real_folder = "dataset/deepfake/real"
fake_folder = "dataset/deepfake/fake"

data = []
labels = []

def load_images_from_folder(folder, label):
    for file in os.listdir(folder):
        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (128, 128))
            img = img / 255.0
            data.append(img)
            labels.append(label)

# Real = 0
load_images_from_folder(real_folder, 0)

# Fake = 1
load_images_from_folder(fake_folder, 1)

data = np.array(data)
labels = np.array(labels)

print("Data shape:", data.shape)
print("Labels shape:", labels.shape)
