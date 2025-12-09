import cv2
import numpy as np
import av
from typing import Optional, Dict, List
from app.services.video_processing.processing.FaceDetector import FaceDetector
from app.services.video_processing.processing.FaceEmbedder import FaceEmbedder
from app.services.video_processing.processing.FaceTracker import FaceTracker
from app.services.video_processing.processing.Archive import Archive
from norfair.tracker import TrackedObject
import base64
from PIL import Image
from io import BytesIO
import os
from app.config import BASE_DIR_PATH
import uuid
from urllib.parse import quote
from pprint import pprint

class VideoAnalyzer:
    def __init__(self, in_video_path: str, processing_params: Optional[Dict] = None):

        self._in_video_path     = in_video_path
        self._processing_params = processing_params or {}

        # PyAV params / config
        self._in_container      = None
        self._video_stream_in   = None
        self._audio_stream_in   = None

        # Processing variables
        self._itr = 0
        self.fd = FaceDetector(self._processing_params.get('yolo_model', 'yolo11n_reduced_dataset'))
        self.fe = FaceEmbedder(show_warnings=False)
        # print('Using: ', self._processing_params.get('norfair_params', 
        #         {'distance_function': 'cosine', 'distance_threshold': 0.3}))
        self.ft = FaceTracker(self._processing_params.get('norfair_params'))
        print('Params: \n')
        pprint(self._processing_params.get('norfair_params'))
        self._frame_id = 0

        # Archive
        self.archive = Archive()

        self.crops = {}

        n_params = self._processing_params.get(
            'norfair_params', None
        )
        if n_params is not None:
            is_reid = n_params.get('reid_distance_function', False)
        
        self._is_reid = True if is_reid else False


    def __enter__(self):
        
        self._in_container   = av.open(self._in_video_path)
        
        self._video_stream_in = next((s for s in self._in_container.streams if s.type == 'video'))
        self._audio_stream_in = next((s for s in self._in_container.streams if s.type == 'audio'), None)
            
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._in_container.close()
        self.crops.clear()

    def process_video(self):
        # Processing variables
        frames_list = []

        for packet in self._in_container.demux([self._video_stream_in, self._audio_stream_in]):

            if packet.stream == self._video_stream_in:
                for frame in packet.decode():

                    frame = frame.to_ndarray(format='bgr24')
                    if self._processing_params.get('rotation', False):
                        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                    self._itr += 1
                    frames_list.append(frame)

                    # Building batch of size passed in self._processing_params
                    if self._itr == self._processing_params.get('yolo_batch_size', 1):
                        
                        self._itr = 0

                        frames_batch = np.stack(frames_list, axis=0)
                        boxes_list, confidences, results = self.fd.detect_faces(frames_batch, self._processing_params.get('yolo_params', {}))
                        boxes_list = self._rescale_boxes(boxes_list, (frame.shape[:2]))
                        faces_embeddings = self.fe.create_embeddings(
                            results, 
                            norm=False)

                        for i, frame in enumerate(frames_batch):
                            self.ft.build_detections(boxes_list[i], confidences[i], faces_embeddings[i])
                            tracked_objects = self.ft.update()
                            self._update_crops(tracked_objects, frame)
                            frame_tr_objs = self._serialize_tracked_objects(tracked_objects)
                            self.archive.add_frame_data(self._frame_id, frame_tr_objs)
                            self._frame_id += 1

                        frames_list.clear()

        # Handling last part of frames (they do not achieve full batch_size)
        if frames_list:
            frames_batch = np.stack(frames_list, axis=0)
            boxes_list, confidences, results = self.fd.detect_faces(frames_batch, self._processing_params.get('yolo_params', {}))
            boxes_list = self._rescale_boxes(boxes_list, (frame.shape[:2]))
            faces_embeddings = self.fe.create_embeddings(
                            results, 
                            norm=False)

            for i, frame in enumerate(frames_batch):

                self.ft.build_detections(boxes_list[i], confidences[i], faces_embeddings[i])
                tracked_objects = self.ft.update()
                self._update_crops(tracked_objects, frame)
                frame_tr_objs = self._serialize_tracked_objects(tracked_objects)
                self.archive.add_frame_data(self._frame_id, frame_tr_objs)
                self._frame_id += 1

        print(f'Zarejestrowana liczba klatek w VideoAnalyzer: {self._frame_id}')

    def get_crops(self):
        """
        Takes:
        {
            id(INT):np.ndarray(dtype=np.uint8),
            ...
        }
        
        Returns: 
        {
            id(INT):base64(STRING),
            ...
        }
        """
        if not self.crops:
            raise IndexError('VideoAnalyzer.get_crops | Crops dict is empty! Run process_video first.')
        
        dct = {}
        crops = self.crops

        for key, crop in crops.items():
            pil_crop = Image.fromarray(crop)
            buffer = BytesIO()
            pil_crop.save(buffer, format='PNG')
            buffer.seek(0)
            crop_base64 = base64.b64encode(buffer.getvalue()).decode()
            dct[key] = crop_base64

        return dct

    def _serialize_tracked_objects(self, tracked_objects: List[TrackedObject]):
        
        """
        Based on input argument (tracked_objects), this function builds and returns List of Dicts
        containing data about single detection: 
        'face_id':  
        'x1':      
        'y1':      
        'x2':      
        'y2':      
        'embedding':

        Works only for single frame.
        """
        
        lst = []

        for tr in tracked_objects:
            points = tr.last_detection.data.get('bbox')
            top_l, _, _, bottom_r = points

            dct = {
                'face_id':  tr.global_id,
                'x1':       top_l[0],
                'y1':       top_l[1],
                'x2':       bottom_r[0],
                'y2':       bottom_r[1]
            }
            lst.append(dct)
        
        return lst
    
    def _update_crops(self, tracked_objects: List[TrackedObject], frame: np.ndarray):
        for obj in tracked_objects:
            # Tworzymy crop tylko jeśli global_id jeszcze nie istnieje w self.crops
            if obj.global_id in self.crops:
                continue  # już mamy crop, nie ruszamy

            # Spróbuj wziąć bieżącą detekcję
            det = getattr(obj, 'last_detection', None)
            if det is not None and det.data.get('bbox', None):
                points = det.data['bbox']
            else:
                # Fallback: przewidywana pozycja z trackera
                points = obj.estimate_as_bbox()  # musi zwrócić 4 punkty: top_l, top_r, bottom_l, bottom_r

            top_l, top_r, bottom_l, bottom_r = points

            # Wycinamy crop z ramki
            crop = frame[top_l[1]:bottom_r[1], top_l[0]:bottom_r[0]]

            # Zapisujemy crop dla global_id tylko raz
            self.crops[obj.global_id] = crop

    def _rescale_boxes(self, boxes_list, size):
        """
        Converts bounding boxes from YOLO 896x896 to the target image size (H, W)
        
        Args:
            boxes_list: list of np.array, each frame has shape (N, 4) in the format [x1, y1, x2, y2]
            size: tuple (H, W) - target image size
        
        Returns:
            list of np.array - rescaled boxes for each frame
        """

        H, W = size
        scale_x = W / 896
        scale_y = H / 896
        
        rescaled_list = []
        for frame_boxes in boxes_list:
            if frame_boxes.size == 0:
                rescaled_list.append(frame_boxes)
                continue
            frame_rescaled = frame_boxes.copy()
            frame_rescaled[:, [0, 2]] = frame_rescaled[:, [0, 2]] * scale_x  # x1, x2
            frame_rescaled[:, [1, 3]] = frame_rescaled[:, [1, 3]] * scale_y  # y1, y2
            rescaled_list.append(frame_rescaled)
            
        return rescaled_list

    def get_crops_as_static_files(self, video_id):
        out_folder_path = f'{str(BASE_DIR_PATH)}/static/{str(video_id)}/'
        os.makedirs(out_folder_path, exist_ok=True)
        url_base = f'http://localhost:8000/static/{str(video_id)}/'

        dct = {}
        crops = self.crops

        for key, crop in crops.items():
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            pil_crop = Image.fromarray(crop)
            img_name = f'{uuid.uuid4()}.png'
            pil_crop.save(os.path.join(out_folder_path, img_name), format='PNG')
            dct[int(key)] = url_base + quote(img_name)

        return dct
            
