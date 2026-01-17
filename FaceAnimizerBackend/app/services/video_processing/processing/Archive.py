from dataclasses import dataclass, field
from typing import Dict, List
import json

@dataclass
class Archive:
    _archive: Dict = field(init=False)

    def __post_init__(self):
        self._archive = {}
    
    def add_frame_data(self, frame_id: int, frame_data: List[Dict]):
        
        """
        Adds frame to archive. Expects arguments:
        - frame_num: number / id of frame (int)
        - frame_data: list of Dicts containing data about single detection
        """
        
        self._archive[frame_id] = frame_data

    def delete_frame_data(self, frame_id: int):

        """
        Deletes frame from archive. Expets argument:
        - frame_id: id of fram that is supposed to be removed (int)

        Raises an ValueError if there is no frame with passed frame_id.
        """

        for frame_info in self._archive:
            if frame_info['frame_id'] == frame_id:
                self._archive.remove(frame_info)
                return
        
        raise ValueError('Error in class Archive | delete_frame | no frame with passed frame_id found \
                         in archive!')

    def get_frame_data(self, frame_id: int):

        """
        Returns frame information from archive. Expets argument:
        - frame_id: id of fram that is supposed to be returned (int)

        Raises an ValueError if there is no frame with passed frame_id.
        """

        for frame_info in self._archive:
            if frame_info['frame_id'] == frame_id:
                return frame_info

        raise ValueError('Error in class Archive | get_frame_info | no frame with passed frame_id found \
                         in archive!')   
    
    def import_to_json(self, output_path: str):
        data_str_keys = {str(k):v for k, v in self._archive.items()}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_str_keys, f, indent=4, ensure_ascii=False)