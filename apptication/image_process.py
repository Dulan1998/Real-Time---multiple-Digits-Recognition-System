import cv2
import numpy as np
import  math
from keras.models import load_model

# Loading trained digits model
model = load_model('../1model_training/mnist.h5')
def predict_digit(img):
    test_image = img.reshape(-1, 28, 28, 1)
    value = np.argmax(model.predict(test_image))
    x=0
    if value == 0:
        x = 'zero'
    elif value == 1:
        x = 'one'
    elif value == 2:
        x = 'two'
    elif value == 3:
        x = 'three'
    elif value == 4:
        x = 'four'
    elif value == 5:
        x = 'five'
    elif value == 6:
        x = 'six'
    elif value == 7:
        x = 'seven'
    elif value == 8:
        x = 'eight'
    elif value == 9:
        x = 'nine'
    else:
        x = 'out of range'
    return x
#pitting label
def put_label(t_img, label, x, y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    l_x = int(x) - 10
    l_y = int(y) + 10
    cv2.putText(t_img, str(label), (l_x,l_y), font, 1.5, (200, 70, 70), 4, cv2.LINE_AA)
    return t_img
# refining each digit
def image_refiner(gray):
    org_size = 22
    img_size = 28
    rows, cols = gray.shape

    if rows > cols:
        factor = org_size/rows
        rows = org_size
        cols = int(round(cols*factor))
    else:
        factor = org_size/cols
        cols = org_size
        rows = int(round(rows*factor))
    gray = cv2.resize(gray, (cols, rows))
    #get padding
    colsPadding = (int(math.ceil((img_size - cols) / 2.0)), int(math.floor((img_size - cols) / 2.0)))
    rowsPadding = (int(math.ceil((img_size - rows) / 2.0)), int(math.floor((img_size - rows) / 2.0)))

    # apply padding
    gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')
    return gray
def get_output_image(path):
    img = cv2.imread(path, 2)
    img_org = cv2.imread(path)

    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for j, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        if(hierarchy[0][j][3] != -1 and w > 10  and h > 10):
            # putting boundary on each digit
            cv2.rectangle(img_org, (x, y), (x + w, y + h),(0,255,255), 2)

            # cropping each image and process
            roi = img[y:y+h, x:x+w]
            roi = cv2.bitwise_not(roi)
            roi = image_refiner(roi)
            #getting predictiction of cropped image
            pred = predict_digit(roi)
            print(pred)

            #placing label on each digit
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            img_org = put_label(img_org,pred, x, y)
    return img_org