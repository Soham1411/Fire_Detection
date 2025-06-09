from ultralytics import YOLO

model = YOLO(r"C:\Users\SOHAM MONDAL\Desktop\Yolov10Firedetectionmodel\runs\content\runs\detect\train\weights\best.pt")
model.predict(source=0, imgsz=640, conf=0.6, show=True)