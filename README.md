# Face image quality check

A small Python script that goes through a folder of face images, checks each one for quality problems and sorts them into valid and rejected folders. Also, it saves a CSV report with the result for every image.

I made it to practice working with image data and to see how much of the checking can be automated.

## What it checks

| Status | Meaning |
|---|---|
| too_small | image width or height is below 100 px |
| blurry | Laplacian variance is below 50 |
| no_face | no face detected |
| multiple_faces | more than one face detected |
| ok | image passed all checks |

Face detection uses OpenCV's Haar cascade classifier.

## Files

* `check_images.py` is the main script
* `make_img_small.py` makes a few very small copies of images, I used it to create test examples
* `report.csv` is the report 

## How to run

```
pip install opencv-python==4.14.0.94 pandas
python check_images.py
```

Put the images in a folder called `images` next to the script. The results are saved in `output/valid`, `output/rejected/<reason>` and `report.csv`.


## Data

I tested it on 91 images: 80 random images from the LFW (Labeled Faces in the Wild) dataset and 11 bad examples that I added on purpose (blurry, very small, group photos and photos without people).
The images are not in this repository because they show real people.

## Results

| Status | Images | Checked by hand |
|---|---|---|
| ok | 67 | |
| blurry | 10 | 9 correct, 1 looked fine |
| multiple_faces | 8 | 6 correct, 2 had only one face |
| no_face | 3 | all correct |
| too_small | 3 | all correct |

I opened every rejected image to see if the script was right. It was wrong in 3 out of 24 cases.

## What I noticed

* The detector can still find a face in a 60x60 image, so image size needs to be checked separately.
* The sharpness score is calculated for the whole image. In one example, the face was blurry but the score was still high because the rest of the image was sharp.
* The detector sometimes detects a second face in the background even when there isn't one.
* I chose the 100 px and 50 thresholds based on the results from this sample, so they would likely need to be adjusted for a different dataset.

## Possible improvements

* calculate the sharpness score only on the face area
* try a newer face detector
* support more image formats