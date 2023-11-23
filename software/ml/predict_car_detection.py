from ultralytics import YOLO
import cv2
import numpy

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
        for p in keypoints.xy[0]:
            x = int(p[0])
            y = int(p[1])
            cv2.circle(img, (x, y), 1, visible_color, -1)

    for box in numpy_boxes:
        xtl = int(box.xyxy[0][0])
        ytl = int(box.xyxy[0][1])
        xbr = int(box.xyxy[0][2])
        ybr = int(box.xyxy[0][3])
        cv2.rectangle(img, (xtl, ytl), (xbr, ybr), [255,0,0], 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)