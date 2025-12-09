from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.config import TEMP_VIDEOS_PATH

router = APIRouter()

@router.get("/download/{video_id}")
async def get_video(video_id: str):
    
    video_path = f'{TEMP_VIDEOS_PATH}/{video_id}/{video_id}_processed.mp4'
    print(video_path)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )
