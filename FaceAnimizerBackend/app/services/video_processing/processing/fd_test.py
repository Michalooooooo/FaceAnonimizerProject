from app.services.video_processing.processing.VideoAnalyzer import VideoAnalyzer
import sys, traceback
import numpy as np
from app.services.video_processing.processing.distance_functions import cosine_distance_reid
import time

in_video_path = '/home/michal/dev/vscode/MyUtils/data_processing/inputs/filmik.mp4'

processing_params = {
    'norfair_params': {
        'distance_function': 'cosine',
        'distance_threshold': 0.3,
        'hit_counter_max':100,
        'initialization_delay':2,
        'reid_distance_function':cosine_distance_reid,
        # 'reid_distance_threshold':0.2

    },
    'yolo_model':'yolo11n_reduced_dataset',
    'yolo_batch_size':32,
    'yolo_params': {
        'verbose': True,
        'half':True,
        'conf':0.75,
        'iou':0.75,
        'device':'cuda'
    },
    'rotation':True
}

with VideoAnalyzer(in_video_path, processing_params) as va:
    try:
        start = time.time()
        va.process_video()
        dct = va.get_crops()
        step1 = time.time()
        va.archive.import_to_json('/home/michal/dev/vscode/MyUtils/data_processing/outputs/output1.json')
        finish = time.time()
        print(f'Ilosc wykrytych twarzy (patrząc po id trackera): {len(va.crops)}')
    except AssertionError:
        print("AssertionError caught in fd_test.py!")
        traceback.print_exc()   # pokaże dokładny stack trace
        sys.exit(1)



import matplotlib.pyplot as plt
import cv2

for a in dct.values():
    a = cv2.resize(a, (80,80), interpolation=cv2.INTER_LINEAR)
    plt.imshow(a)
    plt.show()

#print('Niby zrobione')
print(f'Czas przetwarzania: {step1 - start}')
print(f'Czas zapisu do JSON: {finish - step1}')

# from FaceEmbedder import FaceEmbedder
# from distance_functions import cosine_distance_reid
# import cv2
# import numpy as np

# fe = FaceEmbedder()

# im1 = cv2.imread('/home/michal/dev/vscode/MyUtils/data_processing/outputs/output_img_1.jpg')
# im2 = cv2.imread('/home/michal/dev/vscode/MyUtils/data_processing/outputs/output_img_2.jpg')

# im_list = [im1, im2]

# im1 = cv2.resize(im1, (112, 112), interpolation=cv2.INTER_LINEAR)
# im2 = cv2.resize(im2, (112, 112), interpolation=cv2.INTER_LINEAR)

# e1 = fe.create_embeddings(im1)
# e2 = fe.create_embeddings(im2)
# print(1 - np.dot(e1[0][0], e2[0][0]))

