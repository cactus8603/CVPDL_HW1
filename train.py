import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

imgs = ['./data/IMG_2274_jpeg_jpg.rf.2f319e949748145fb22dcb52bb325a0c.jpg']

results = model(imgs)

results.save()