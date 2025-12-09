import torch
import numpy as np
import cv2
from ultralytics import YOLO
from app.services.video_processing.processing.model_registry import MODEL_REGISTRY
from typing import Dict, Optional

class FaceDetector:
    def __init__(self, model: str):
        try:
            model_path = MODEL_REGISTRY.get(model, None)
            # print(f'TUTAJ JEST PRINT MODEL_PATH!!!!!!!!!!! {model_path}')
            self.model = YOLO(model_path)
        except Exception as e:
            print(f'Exception in FaceDetector class | {e}')
        
        self._itr_ctr = 0

    def detect_faces(self, frames_batch: np.ndarray, yolo_params: Dict = {}):
        # Data validation
        if frames_batch.ndim not in [3, 4]:
            raise ValueError(f'Error in class FaceDetector | detect_faces: frames_batch has inproper amount of dims ({frames_batch.ndim})')

        if frames_batch.shape[frames_batch.ndim - 1] != 3:
            raise ValueError(f'Error in class FaceDetector | detect_faces: frames_batch has inproper shape ({frames_batch.shape}) \
                             expected shape is (H, W, C), or (B, H, W, C) C=3')
        
        if frames_batch.dtype != np.uint8:
            raise TypeError(f'Error in class FaceDetector | detect_faces: frames_batch has inproper type ({frames_batch.dtype}) \
                            should be np.uint8')

        if frames_batch.ndim == 4:
            lst = []
            for frame in frames_batch:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (896, 896), interpolation=cv2.INTER_LINEAR)
                lst.append(frame)
            
            frames_batch = np.stack(lst, axis=0)
            frames_batch = np.transpose(frames_batch, (0, 3, 1, 2))

        elif frames_batch.ndim == 3:
            frames_batch = cv2.cvtColor(frames_batch, cv2.COLOR_BGR2RGB)
            frames_batch = cv2.resize(frames_batch, (896, 896), interpolation=cv2.INTER_LINEAR)
            frames_batch = np.transpose(frames_batch, (2, 0, 1))
            frames_batch = np.expand_dims(frames_batch, 0)
        else:
            raise ValueError('Error in class FaceDetector | detect_faces: sth wrong with frames_batch')

        frames_batch = torch.from_numpy(frames_batch)
        input_batch = frames_batch.to(torch.float32) / 255
        
        results = self.model(input_batch, **yolo_params)

        results_list = []
        conf_list = []
        crops_list = []

        for i in range(0, frames_batch.shape[0]):
            res = results[i].boxes.xyxy
            conf = results[i].boxes.conf
            results_list.append(res.cpu().numpy())
            conf_list.append(conf.cpu().numpy())

        # Cutting full roi from image tensor
        for frame, xyxy in zip(frames_batch, results_list):
            lst = []
            xyxy = xyxy.tolist()

            for result in xyxy:
                x1, y1, x2, y2 = map(int, result)
                roi = frame[:, y1:y2, x1:x2]
                # Transforming roi to (H, W, C)
                roi = roi.cpu().numpy()
                roi = np.transpose(roi, (1, 2, 0))
                lst.append(roi)
            crops_list.append(lst)
            # print(f'Liczba detekcji na klatke: {len(lst)}')


        return results_list, conf_list, crops_list
