import cv2

# Real image
real_path = "dataset/deepfake/real/00016.jpg"
real_img = cv2.imread(real_path)

# Fake image
fake_path = "dataset/deepfake/fake/0B3N3K1GS4.jpg"
fake_img = cv2.imread(fake_path)

if real_img is not None:
    cv2.imshow("Real Image", real_img)

if fake_img is not None:
    cv2.imshow("Fake Image", fake_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
