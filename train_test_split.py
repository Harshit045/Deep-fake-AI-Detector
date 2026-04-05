import numpy as np
from sklearn.model_selection import train_test_split
import os
import cv2

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

load_images_from_folder(real_folder, 0)
load_images_from_folder(fake_folder, 1)

data = np.array(data)
labels = np.array(labels)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=42
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)
