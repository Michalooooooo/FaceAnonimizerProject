import cv2
from app.services.video_processing.processing.distance_functions import cosine
from app.services.video_processing.processing.FaceEmbedder import FaceEmbedder
import numpy as np

im1 = cv2.imread('/home/michal/dev/FaceAnimizerBackend/static/189c2de2-83ac-41da-8af5-8f6e054dedd4/4ce4e360-1e97-4279-a166-47903e6c71ac.png')
im2 = cv2.imread('/home/michal/dev/FaceAnimizerBackend/static/189c2de2-83ac-41da-8af5-8f6e054dedd4/80eb97ce-4985-469d-8f41-ebd83cb27d6c.png')

fe = FaceEmbedder(show_warnings=False)

im1 = cv2.resize(im1, (112,112), interpolation=cv2.INTER_LINEAR)
im2 = cv2.resize(im2, (112,112), interpolation=cv2.INTER_LINEAR)

im1 = np.transpose(im1, (2, 0, 1))
im2 = np.transpose(im2, (2, 0, 1))

im1_emb = fe.create_embeddings(im1)[0].flatten()
im2_emb = fe.create_embeddings(im2)[0].flatten()

def normalize(embedding: np.ndarray):
    return embedding / np.linalg.norm(embedding)

im1_emb = normalize(im1_emb)
im2_emb = normalize(im2_emb)

distance = 1 - np.dot(im1_emb, im2_emb)

print(distance)
