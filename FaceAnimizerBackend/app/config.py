from pathlib import Path

BASE_DIR_PATH = Path(__file__).resolve().parent.parent

VIDEO_PROCESSING_PATH = BASE_DIR_PATH / 'app' / 'services' / 'video_processing' 

TEMP_VIDEOS_PATH = BASE_DIR_PATH / 'app' / 'temp_videos'
