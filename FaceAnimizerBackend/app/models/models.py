from pydantic import BaseModel
from typing import Optional, List

from typing import Optional
from pydantic import BaseModel, Field

class NorfairParams(BaseModel):
    distance_function: str = 'mean_euclidean'
    distance_threshold: float = 30
    hit_counter_max: Optional[int] = 10
    initialization_delay: Optional[int] = 2
    pointwise_hit_counter_max: Optional[int] = 0
    detection_threshold: Optional[float] = 0.4
    past_detections_length: Optional[int] = 5

    # te pola mają się pojawić tylko jeśli front je wyśle
    reid_distance_function: Optional[str] = Field(default=None)
    reid_distance_threshold: Optional[float] = Field(default=None)
    reid_hit_counter_max: Optional[int] = Field(default=None)


class YOLOParams(BaseModel):
    conf:       float   = 0.4
    iou:        float   = 0.4
    half:       bool    = True
    device:     str     = 'cuda'
    verbose:    bool    = False

class ProcessingParams(BaseModel):
    norfair_params: NorfairParams
    yolo_model: str                 = 'yolo11s_reduced_dataset'
    yolo_batch_size: int            = 32
    yolo_params: YOLOParams
    rotation: bool                  = False

class AnonimizeRequest(BaseModel):
    faces_list: List[int]
    rotate: bool 
