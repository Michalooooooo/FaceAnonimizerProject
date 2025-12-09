import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("/home/michal/dev/FaceAnimizerBackend/app/services/video_processing/emb_models/w600k_r50_batch.onnx")

# Przykładowy batch 4 obrazów
x = np.random.randn(4,3,112,112).astype(np.float32)
outputs = session.run(None, {session.get_inputs()[0].name: x})
print(outputs[0]) 