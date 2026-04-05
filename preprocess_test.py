import cv2

img_path = "dataset/deepfake/real/00016.jpg"

img = cv2.imread(img_path)
img_resized = cv2.resize(img, (128, 128))
img_normalized = img_resized / 255.0

print("Image shape:", img_normalized.shape)

cv2.imshow("Original Image", img)
cv2.imshow("Resized Image", img_resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
