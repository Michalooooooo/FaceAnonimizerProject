from enum import Enum

class DetectionModels(Enum):
    NONE = 0
    YOLOv11 = 1
    YOLOv12 = 2
    FASTERRCNN = 3

class EmbeddingsModels(Enum):
    NONE = 0
    FACENET = 1
    ARCNET = 2

class FaceMeshModels(Enum):
    NONE = 0
    MEDIA_PIPE = 1
    DLIB = 2