from ultralytics import YOLO
import cv2
import numpy
from constants import LABEL_MAPPING

# Load a COCO-pretrained YOLOv8n model
#model = YOLO('yolov8n.pt')
model = YOLO(r"C:\Users\jeuch\Documents\GitHub\traffic-watch\runs\pose\train3\weights\last.pt")

for i in range (15,24):
    for j in range(0, 10):
        image_path = f"C:\\Users\\jeuch\\Documents\\GitHub\\traffic-watch\\data\\recordings\\off_road\\%s\\videos\\%s.png" % (i,j)
        img = cv2.imread(image_path)
        results = model(image_path)

        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            numpy_boxes = boxes.numpy()

            for box in numpy_boxes:
                #if box.cls[0] == 2:
                xtl = int(box.xyxy[0][0])
                ytl = int(box.xyxy[0][1])
                xbr = int(box.xyxy[0][2])
                ybr = int(box.xyxy[0][3])
                cv2.rectangle(img, (xtl, ytl), (xbr, ybr), [255,0,0], 1)

            cv2.imshow('img', img)
            cv2.waitKey(0)

if False:
    model_path = r"C:\Users\jeuch\Documents\GitHub\traffic-watch\runs\pose\train2\weights\last.pt"
    image_path = f"C:\\Users\\jeuch\\Documents\\GitHub\\traffic-watch\\data\\test\\\\3.png"

    model = YOLO(model_path)
    img = cv2.imread(image_path)

    #for i in range (0, 23):
    #    model(f"C:\\Users\\jeuch\\Documents\\GitHub\\traffic-watch\data\\recordings\\1\\videos\\{i}.png",save=True)

    #exit(1)

    visible_color = [0,255,0]
    invisible_color = [0,0, 255]

    results = model(image_path,save=False)

    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        numpy_boxes = boxes.numpy()
        numpy_keypoints = keypoints.numpy()

        for keypoints in numpy_keypoints:
            for index, p in enumerate(keypoints.xy[0], start=1):
                x = int(p[0])
                y = int(p[1])
                cv2.circle(img, (x, y), 1, [255,100,255] if index == LABEL_MAPPING['passenger_side_mirror'] else visible_color, -1)

        for box in numpy_boxes:
            xtl = int(box.xyxy[0][0])
            ytl = int(box.xyxy[0][1])
            xbr = int(box.xyxy[0][2])
            ybr = int(box.xyxy[0][3])
            cv2.rectangle(img, (xtl, ytl), (xbr, ybr), [255,0,0], 1)

        cv2.imshow('img', img)
        cv2.waitKey(0)
