# from typing import Dict
# from app.models.models import ProcessingParams
# from app.services.video_processing.processing.distance_functions import \
# cosine_distance_reid, euclidean_distance_reid,euclidean_distance_squared_reid
# from pprint import pprint

# CALLABLES = {
#     'cosine_distance_reid':             cosine_distance_reid,
#     'euclidean_distance_reid':          euclidean_distance_reid,
#     'euclidean_distance_squared_reid':  euclidean_distance_squared_reid
# }

# def convert_params(model: ProcessingParams):
#     params = model.model_dump()
#     norfair_params = params.get('norfair_params', None)
    
#     val = norfair_params.get('reid_distance_function', False)

#     if val:
#         try:
#             norfair_params['reid_distance_function'] = CALLABLES.get(val)
#         except Exception as e:
#             print(f'app.models.convert_params.convert_params | {e}')

#     params['norfair_params'] = norfair_params

#     pprint(params)

#     return params