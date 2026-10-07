import os
import cv2

files = os.listdir("images")

for i in range(3):
       img = cv2.imread("images/" + files[i])
       small = cv2.resize(img, (60, 60))
       cv2.imwrite("images/small_" + str(i + 1) + ".jpg", small)

print("done")