import cv2
import numpy as np
from typing import List
from app.config import TEMP_VIDEOS_PATH
import av
import json
import traceback
import os
import shutil

class FaceAnonimizer:
    def __init__(self, _id: str, faces_list: List[int], rotation: bool = False):
        self._id = _id
        self._faces_list = faces_list
        self._frame_id = 0
        self._dir_path = f'{TEMP_VIDEOS_PATH}/{self._id}'
        self._rotation = rotation

        self._json_dict = {}
        self._in_video_path = f'{self._dir_path}/{self._id}.mp4'
        self._out_video_path = f'{self._dir_path}/{self._id}_processed.mp4'

    def __enter__(self):
        self._input_av = av.open(self._in_video_path)
        self._output_av = av.open(self._out_video_path, mode='w', format='mp4')
        self._input_video_stream = None
        self._input_audio_stream = None
        self._input_video_stream = next((s for s in self._input_av.streams if s.type == 'video'), None)
        self._input_audio_stream = next((s for s in self._input_av.streams if s.type == 'audio'), None)

        self._output_audio_stream = None
        if self._input_audio_stream is not None:
            self._output_audio_stream = self._output_av.add_stream_from_template(template=self._input_audio_stream)

        self._output_video_stream = self._output_av.add_stream(
            codec_name='libx264',
            rate=round(self._input_video_stream.average_rate) if self._input_video_stream.average_rate else 30
        )
        if self._rotation:
            self._output_video_stream.width = self._input_video_stream.height
            self._output_video_stream.height = self._input_video_stream.width
        else:
            self._output_video_stream.width = self._input_video_stream.width
            self._output_video_stream.height = self._input_video_stream.height
        self._output_video_stream.pix_fmt = 'yuv420p'

        json_path = f'{self._dir_path}/{self._id}.json'

        with open(json_path, "r") as f:
            self._json_dict = json.load(f)

        self._json_dict = {int(k): v for k, v in self._json_dict.items()}

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._input_av.close()
        self._output_av.close()

    def anonimize_video(self):

        for packet in self._input_av.demux([self._input_video_stream, self._input_audio_stream]):

            if packet.stream == self._input_video_stream:
                for frame in packet.decode():
                    img = frame.to_ndarray(format='bgr24')
                    if self._rotation:
                        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

                    processed_img = self._blur_faces_on_frame(img)
                    self._frame_id += 1

                    new_frame = av.VideoFrame.from_ndarray(processed_img, format='bgr24')
                    new_frame = new_frame.reformat(format='yuv420p', width=frame.width, height=frame.height)

                    for out_packet in self._output_video_stream.encode(new_frame):
                        self._output_av.mux(out_packet)

            elif packet.stream == self._input_audio_stream and self._input_audio_stream is not None:
                if packet.dts is None:
                    continue
                packet.stream = self._output_audio_stream
                self._output_av.mux(packet)

        for out_packet in self._output_video_stream.encode():
            self._output_av.mux(out_packet)

    def _blur_faces_on_frame(self, frame: np.ndarray):
        frame_data = self._json_dict.get(self._frame_id, [])

        for fd in frame_data:
            if fd.get('face_id') in self._faces_list:
                # Blurring
                x1 = fd.get('x1')
                y1 = fd.get('y1')
                x2 = fd.get('x2')
                y2 = fd.get('y2')

                roi = frame[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(roi, (65, 65), 0)

                frame[y1:y2, x1:x2] = blurred
        
        return frame

    def _draw_face_ids_on_frame(self, frame: np.ndarray):
        frame_data = self._json_dict.get(self._frame_id, [])

        for fd in frame_data:
            if fd.get('face_id') in self._faces_list:
                x1 = fd.get('x1')
                y1 = fd.get('y1')
                x2 = fd.get('x2')
                y2 = fd.get('y2')

                text = str(fd.get('face_id'))

                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_thickness = 2
                color = (0, 255, 0)

                (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

                center_x = x1 + (x2 - x1) // 2
                center_y = y1 + (y2 - y1) // 2

                text_x = center_x - text_width // 2
                text_y = center_y + text_height // 2

                cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)

        return frame

