# import onnx
# from onnx import helper
# import onnxruntime as ort
# import numpy as np

# # --- 1. Załaduj model ---
# model_path = "/home/michal/dev/FaceAnimizerBackend/app/services/video_processing/emb_models/w600k_r50.onnx"
# model = onnx.load(model_path)

# # --- 2. Zmień wejście na dynamiczny batch ---
# for input in model.graph.input:
#     dims = input.type.tensor_type.shape.dim
#     dims[0].dim_param = "batch_size"  # zamiast dim_value=1

# # --- 3. Zmień wyjście na dynamiczny batch ---
# for output in model.graph.output:
#     dims = output.type.tensor_type.shape.dim
#     dims[0].dim_param = "batch_size"  # zamiast dim_value=1

# # --- 4. Zapisz nowy model ---
# batch_model_path = "/home/michal/dev/FaceAnimizerBackend/app/services/video_processing/emb_models/w600k_r50_batch.onnx"
# onnx.save(model, batch_model_path)
# print(f"Model zapisany jako {batch_model_path}")
from onnxconverter_common import float16
import onnx

p1 = '/home/michal/dev/FaceAnimizerBackend/app/services/video_processing/emb_models/w600k_r50_batch.onnx'
p2 = '/home/michal/dev/FaceAnimizerBackend/app/services/video_processing/emb_models/w600k_r50_batch_f16.onnx'

model_fp16 = float16.convert_float_to_float16(onnx.load(p1), keep_io_types=True)
onnx.save(model_fp16, p2)
print("✅ Zapisano model FP16 jako w600kr50_batch_fp16.onnx")