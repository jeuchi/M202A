from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
model.train(data='config.yaml', epochs=300, batch=128, imgsz=1080)