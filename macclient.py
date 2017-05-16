import requests
import cv2
import time

host = "127.0.0.1:8888"
# This script will detect faces via your webcam.
# Tested with OpenCV3

def monitor():
    cap = cv2.VideoCapture(0)

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier("facelib/haarcascade_frontalface_default.xml")
    haveCap = True
    count = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))
        if len(faces) > 0 and haveCap:
            # haveCap = False
            sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
            (x, y, w, h) = faces[0]
            if w < 150 or h < 150:
                continue
            crop_img = frame[y:y+h,x:x+w]
            cv2.imwrite("test.jpg", crop_img)
            send("test.jpg")
            count = count + 1
            time.sleep(1);

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


        # Display the resulting frame
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def send(filename):
    url = "http://" + host + "/upload"
    files = {'file1': ('file1', open(filename, 'rb'), 'image/jpg', {'Expires': '0'})}
    r = requests.post(url, files=files)
    print r.text

if __name__ == "__main__":
    monitor()