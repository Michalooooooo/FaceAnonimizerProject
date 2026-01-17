import numpy as np
from norfair.tracker import TrackedObject

##################################################################################################
# DISTANCE FUNCTIONS TO USE AS Tracker.reid_function
##################################################################################################

def cosine(candidate: TrackedObject, track: TrackedObject):
    """
    Takes candidate and track which are non-normailzed embeddings and calculates cosine distance
    """
    
    candidate_emb = candidate.last_detection.embedding
    track_emb = calculate_centroid(track)

    candidate_emb = normalize(candidate_emb)
    track_emb = normalize(track_emb)
    
    distance = 1 - np.dot(candidate_emb, track_emb)
    return distance

def euclidean(candidate: TrackedObject, track: TrackedObject):
    """
    Takes candidate and track which are non-normailzed embeddings and calculates euclidean distance
    """

    candidate_emb = candidate.last_detection.embedding
    track_emb = calculate_centroid(track)
    
    return np.linalg.norm(candidate_emb-track_emb)

def euclidean_squared(candidate: TrackedObject, track: TrackedObject):
    """
    Takes candidate and track which are non-normailzed embeddings and calculates euclidean squared distance
    """

    candidate_emb = candidate.last_detection.embedding
    track_emb = calculate_centroid(track)
    
    return np.sum((candidate_emb-track_emb) ** 2)

##################################################################################################
# HELPER FUNCTIONS
##################################################################################################

def calculate_centroid(obj: TrackedObject, max_emb: int = 5):
    det_list = obj.past_detections[-max_emb:]
    
    emb_list = [det.embedding for det in det_list]

    return np.mean(emb_list, axis=0)

def normalize(embedding: np.ndarray):
    return embedding / np.linalg.norm(embedding)

##################################################################################################
