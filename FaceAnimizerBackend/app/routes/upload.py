from fastapi import APIRouter, UploadFile, File
import shutil
from app.config import BASE_DIR_PATH, TEMP_VIDEOS_PATH
import uuid
from typing import Dict
import os

router = APIRouter()

@router.post('/upload-video')
async def upload_video(file: UploadFile = File(...)):
    _id = str(uuid.uuid4())

    os.makedirs(f'{str(TEMP_VIDEOS_PATH)}/{_id}')

    unique_name = f"{_id}.mp4"
    save_path = f'{str(TEMP_VIDEOS_PATH)}/{_id}/{unique_name}'

    with open(save_path, mode='wb') as f:
        shutil.copyfileobj(file.file, f)

    return {'id':_id}
    
