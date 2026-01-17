from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.video import router as video_processing_router
from app.routes.faces import router as face_animizer_router
from app.routes.download import router as download_router
import torch
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import onnxruntime as ort
from contextlib import asynccontextmanager
from app.config import VIDEO_PROCESSING_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = VIDEO_PROCESSING_PATH / 'emb_models' / 'w600k_r50_batch_f16.onnx'
        
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

    app.state.emb_session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider"])
    
    print("Model loaded!")

    yield 

    print("Application shutdown!")
    
app = FastAPI(lifespan=lifespan)

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


