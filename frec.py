#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
import time

from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
path = './yangz'

# For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.face.createLBPHFaceRecognizer()


def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.tst')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

# Path to the Yale Dataset

# Call the get_images_and_labels function and get the face images and the
# corresponding labels


def train_model(path):
    images, labels = get_images_and_labels(path)
    recognizer.train(images, np.array(labels))
    recognizer.save("./cur.xml")
# Perform the tranining
# recognizer.train(images, np.array(labels))
#
recognizer.load("./rec.xml")
# Append the images with the extension .sad into image_paths


def recognize(image_path):
    size_cof = 4800
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    width, height = predict_image_pil.size
    ret = []
    sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        if w > width / size_cof and h > height / size_cof:
            nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
            ret.append((nbr_predicted, conf))
    return ret


# image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.tst')]
# for image_path in image_paths:
#     print image_path
#     ret = recognize(image_path)
#     for predict_lable, conf in ret:
#         print predict_lable, conf
