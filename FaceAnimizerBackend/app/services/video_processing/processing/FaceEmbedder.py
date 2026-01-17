import mediapipe as mp
import numpy as np
import cv2
from typing import List, Union
import time

class FaceEmbedder:
    def __init__(self, session, show_warnings: bool = True):
       
        self._session = session
        self._input_name = self._session.get_inputs()[0].name
        self._output_name = self._session.get_outputs()[0].name

        # Creating face alignation model instance and session
        mp_face = mp.solutions.face_mesh
        self.face_mesh = mp_face.FaceMesh(static_image_mode=True, max_num_faces=1)

        self.show_warnings = show_warnings

    def create_embeddings(self, crop: Union[List[List[np.ndarray]], np.ndarray], norm: bool = True):
        
        crop_structure = [len(frame) for frame in crop]
        batch_size = 64
        out = []


        if isinstance(crop, list) and not any(crop):
            return crop         

        if isinstance(crop, list):
            
            crops = []
            for frame in crop:
                for single_crop in frame:
                    single_crop = cv2.resize(single_crop, (112, 112), interpolation=cv2.INTER_LINEAR)
                    crops.append(single_crop)
            
            crop = np.stack(crops, axis=0)
            del crops
        elif isinstance(crop, np.ndarray):
            crop = np.expand_dims(crop, axis=0)
        else:
            raise ValueError('FaceEmbedder.create_embeddings | wrong input')
        
        # If amount of dimensions is less than 3 / greater than 4 -> ERROR
        if 5 <= crop.ndim < 3:
            raise ValueError(f'FaceEmbedder.create_embeddings | crop has inproper amount of dimensions ({crop.ndim})')

        # If shape of crop is e.g. (16, 112, 112, 3) it is transformed to (16, 3, 112, 112)
        if crop.shape[1] != 3:
            if self.show_warnings:
                print(f'WARNING: create_embeddings | Expected crop shape is (B, C, 112, 112) got: {crop.shape}. Fixing ...') 
            
            crop = np.transpose(crop, (0, 3, 1, 2))
                
        crop = crop.astype(np.float32)

        crop_list = [crop[i:i+batch_size] for i in range(0, len(crop), batch_size)]

        for c in crop_list:
            emb = self._session.run([self._output_name], {self._input_name: c})
            out.append(emb[0])
        
        combined = np.concatenate(out, axis=0)
        
        split_embs = np.split(combined, np.cumsum(crop_structure)[:-1])
        
        return split_embs

    def align_face_crop(self, face_crop: np.ndarray, remove_padding: bool = True, rgb: bool = True):
        
        '''
        Makes crop square and aligns eyes horizontally.

        Returns either rgb or bgr aligned face (depends on rgb argument)
        '''
        
        org_height, org_width = face_crop.shape[:2]

        square_crop = self._make_square_crop(face_crop)
        h, w = square_crop.shape[:2]

        rgb_crop = cv2.cvtColor(square_crop, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb_crop)

        if not results.multi_face_landmarks:
            return square_crop, None 

        face = results.multi_face_landmarks[0]

        left_eye = face.landmark[33]
        right_eye = face.landmark[263]

        left_eye_coord = (int(left_eye.x * w), int(left_eye.y * h))
        right_eye_coord = (int(right_eye.x * w), int(right_eye.y * h))

        dx = right_eye_coord[0] - left_eye_coord[0]
        dy = right_eye_coord[1] - left_eye_coord[1]
        angle = np.degrees(np.arctan2(dy, dx))

        eyes_center = ((left_eye_coord[0] + right_eye_coord[0]) // 2,
                    (left_eye_coord[1] + right_eye_coord[1]) // 2)

        M = cv2.getRotationMatrix2D(eyes_center, angle, 1)
        aligned_crop = cv2.warpAffine(square_crop, M, (w, h))

        if remove_padding:
            aligned_crop = self._remove_square_padding(aligned_crop, org_height, org_width)

        if rgb:
            aligned_crop = cv2.cvtColor(aligned_crop, cv2.COLOR_BGR2RGB)

        return aligned_crop

    def _make_square_crop(self, face_crop):

        '''
        Adds padding to shorter dimension in order to make the crop a square.
        '''

        h, w = face_crop.shape[:2]
        size = max(h, w)

        pad_h = (size - h) // 2
        pad_w = (size - w) // 2

        square_crop = cv2.copyMakeBorder(
            face_crop,
            top=pad_h,
            bottom=pad_h,
            left=pad_w,
            right=pad_w,
            borderType=cv2.BORDER_REPLICATE
        )

        return square_crop

    def _remove_square_padding(self, aligned_square_crop, original_h, original_w):

        '''
        Cuts the square crop to original size.
        '''

        size_h, size_w = aligned_square_crop.shape[:2]

        center_y = size_h // 2
        center_x = size_w // 2

        y1 = center_y - original_h // 2
        y2 = y1 + original_h
        x1 = center_x - original_w // 2
        x2 = x1 + original_w

        cropped = aligned_square_crop[y1:y2, x1:x2]

        return cropped