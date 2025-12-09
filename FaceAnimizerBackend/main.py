from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.video import router as video_processing_router
from app.routes.faces import router as face_animizer_router
from app.routes.download import router as download_router
import torch
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(upload_router)
app.include_router(video_processing_router)
app.include_router(face_animizer_router)
app.include_router(download_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend Vite
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST itd.
    allow_headers=["*"],   # wszystkie nagłówki
)

@app.get("/")
def root():
    return {"message": "Cuda dziala" if torch.cuda.is_available() else 'Cuda nie dziala'}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
