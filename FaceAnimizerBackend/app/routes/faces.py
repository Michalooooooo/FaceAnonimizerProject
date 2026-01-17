from fastapi import APIRouter
from app.services.video_processing.processing.FaceAnonimizer import FaceAnonimizer
from app.models.models import AnonimizeRequest
import traceback
from typing import List, Dict
import traceback

router = APIRouter()

@router.post('/anonimize-video/{video_id}')
async def anonimize_video(video_id: str, request: AnonimizeRequest):
    faces_list = request.faces_list
    rotate = request.rotate
    print('Otrzymano rotate rowne: ', rotate)

    if faces_list is None:
        raise ValueError('Faces list is None!')

    with FaceAnonimizer(video_id, faces_list, rotate) as fa:
        try:
            fa.anonimize_video()
        except Exception as e:
            print('Exception in faces.py in function analyze_video | ', e)
            traceback.print_exc() 

    return {'status': 'ok'}
