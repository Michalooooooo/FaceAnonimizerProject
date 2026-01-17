import numpy as np
from norfair.tracker import Tracker, Detection
from typing import Dict
from app.services.video_processing.processing.distance_functions import cosine, euclidean, euclidean_squared

class FaceTracker:
    def __init__(self, norfair_params: Dict):
        new_params = self._convert_params(norfair_params)
        self.tracker = Tracker(**new_params)
        self.detections = []
        self.tracks = {}
    
    def clear_tracker(self):
        del self.tracker
        del self.detections
        del self.tracks

    def build_detections(self, boxes: np.ndarray, confidences: np.ndarray, embeddings: np.ndarray):

        for box, conf, emb in zip(boxes, confidences, embeddings):
                        
            det_obj = Detection(
                points=self._calculate_center_point(box),
                embedding=emb,
                scores=np.array([conf]),
                data={'bbox':self._convert_points(box)}
            )
            self.detections.append(det_obj)

    def update(self):

        tracked_objects = self.tracker.update(self.detections)  

        self.detections.clear()
        return tracked_objects

    def _convert_points(self, box: np.ndarray):
        box = box.tolist()
        x1, y1, x2, y2 = map(int, box)

        points = [
            [x1, y1],
            [x2, y1],
            [x1, y2],
            [x2, y2]
        ]

        return points

    def _calculate_center_point(self, box: np.ndarray):
        box = box.tolist()
        x1, y1, x2, y2 = map(int, box)

        x = min(x1, x2) + abs((x2 - x1) // 2)
        y = min(y1, y2) + abs((y2 - y1) // 2)

        return np.array([[x, y]]).astype(np.float32)
    
    def _convert_params(self, params: Dict):
        """
        Returns a copy of the params dictionary where the 'reid_distance_function' key
        is replaced with a reference to the actual function instead of a string.
        """
        new_params = params.copy()
        fun_name = params.get('reid_distance_function')
        
        if isinstance(fun_name, str):
            match fun_name:
                case 'cosine':
                    new_params['reid_distance_function'] = cosine
                case 'euclidean':
                    new_params['reid_distance_function'] = euclidean
                case 'euclidean_squared':
                    new_params['reid_distance_function'] = euclidean_squared
                case _:
                    raise ValueError('Error in FaceTracker._convert_params. Such distance function is not supported!')
            
        
        return new_params