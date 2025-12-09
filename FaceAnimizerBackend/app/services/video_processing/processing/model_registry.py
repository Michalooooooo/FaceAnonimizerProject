from app.config import VIDEO_PROCESSING_PATH


MODEL_REGISTRY = {
    'yolo11s_reduced_dataset':  str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo11s_reduced_dataset.pt'),
    'yolo11n_FDDB':             str(VIDEO_PROCESSING_PATH/'yolo_models'/'yolo11n_FDDB.pt')
}
