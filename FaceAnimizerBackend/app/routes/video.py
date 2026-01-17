from fastapi import APIRouter
from app.services.video_processing.processing.VideoAnalyzer import VideoAnalyzer
import  traceback
import time
from app.config import TEMP_VIDEOS_PATH
from app.models.models import ProcessingParams
from pprint import pprint
from fastapi import Request

router = APIRouter()

@router.post('/analyze-video/{video_id}')
def analyze_video(request: Request, video_id, processing_params: ProcessingParams):
    in_video_path = f'{str(TEMP_VIDEOS_PATH)}/{str(video_id)}/{str(video_id)}.mp4'

    processing_params = processing_params.model_dump()

    pprint(processing_params)
    with VideoAnalyzer(in_video_path, request.app.state.emb_session, processing_params) as va:
        
        try:
            va.process_video()
            dct = va.get_crops_as_static_files(video_id)
            pprint(dct)
            va.archive.import_to_json(TEMP_VIDEOS_PATH / str(video_id) / f'{str(video_id)}.json')
        except Exception as e:
            print('Exception in video.py in function analyze_video | ', e)
            traceback.print_exc()  

    return {
        'faces': dct
    }


