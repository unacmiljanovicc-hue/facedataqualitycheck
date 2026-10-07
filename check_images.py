import os
import shutil
import cv2
import pandas as pd
#face detector from opencv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#limits that i picked after looking at image scores
min_size = 100
blur_limit = 50

files = os.listdir("images")
#deletes output from the last run
shutil.rmtree("output", ignore_errors=True)
rows = []

for f in files:
    img = cv2.imread("images/" + f)
    if img is None: #skips files that are not images
        rows.append([f, "unreadable", 0, 0, 0, 0])
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    height, width = gray.shape
    #calculates blur score, lower number means blurry
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    if width < min_size or height < min_size:
        status = "too_small"
    elif blur < blur_limit:
        status = "blurry"
    elif len(faces) == 0:
        status = "no_face"
    elif len(faces) > 1:
        status = "multiple_faces"
    else:
        status = "ok"

    #copying image to the right folder
    if status == "ok":
        folder = "output/valid"
    else:
        folder = "output/rejected/" + status
    os.makedirs(folder, exist_ok=True)
    shutil.copy("images/" + f, folder + "/" + f)

    rows.append([f, status, len(faces), width, height, round(blur)])

#saving the report
report = pd.DataFrame(rows, columns=["file", "status", "faces", "width", "height", "blur_score"])
report.to_csv("report.csv", index=False)

print(report["status"].value_counts())
print("total:", len(report))