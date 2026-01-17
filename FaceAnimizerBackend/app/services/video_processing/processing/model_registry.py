from app.config import VIDEO_PROCESSING_PATH

MODEL_REGISTRY = {
    'yolo11n_100epch':             str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo11n_FDDB.pt'),
    'yolo10n':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo10n.pt'),
    'yolo10s':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo10s.pt'),
    'yolo11n':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo11n.pt'),
    'yolo11s':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo11s.pt'),
    'yolo12n':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo12n.pt'),
    'yolo12s':                  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo12s.pt'),
}
