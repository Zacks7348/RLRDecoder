import json
from dataclasses import dataclass
from typing import List
from copy import deepcopy

from .header_properties import HeaderProperties
from .net_cache import NetCache

@dataclass
class Replay:
    header_size: int = None
    header_crc: int = None
    engine_version: int = None
    licensee_version: int = None
    network_version: int = None
    game_type: str = None
    header_properties: HeaderProperties = None
    body_size: int = None
    body_crc: int = None
    levels: list = None
    keyframes: list = None
    network_size: int = None
    debug_logs: List[dict] = None
    tickmarks: List[dict] = None
    packages: List[str] = None
    objects: List[str] = None
    names: list = None
    class_map: dict = None
    net_caches: List[NetCache] = None

    def to_json(self, path: str, **kwargs) -> None:
        """
        Output this replay object to JSON
        """
        
        output = deepcopy(self.__dict__)
        output['header_properties'] = self.header_properties.data
        tmp = []
        for cache in self.net_caches:
            cache_data = deepcopy(cache.__dict__)
            cache_data.pop('parent')
            cache_data.pop('children')
            tmp.append(cache_data)
        output['net_caches'] = tmp
        with open(path, 'w') as f:
            json.dump(output, f, **kwargs)

def replay_from_json(path: str) -> Replay:
    """
    Create a Replay object from a JSON file

    Only works with JSON files generated from a Replay object

    Attributes
    ----------
    path : str
        The path to the JSON file

    Returns
    -------
    :class:`Replay`
        The :class:`Replay` object created
    """

    with open(path, 'r') as f:
        data = json.load(f)
        data['header_properties'] = HeaderProperties(data['header_properties'])
        cache_list = []
        cache_lookup = {}
        for cache_data in data['net_caches']:
            cache = NetCache(**cache_data)
            cache_lookup[cache.cache_id] = cache
            cache_list.append(cache)
        for cache in cache_list:
            cache.parent = cache_lookup.get(cache.parent_id)
            cache.children = []
            if cache.children_ids is None:
                cache.children_ids = []
            else:
                for child_id in cache.children_ids:
                    cache.children.append(cache_lookup.get(child_id))
        data['net_caches'] = cache_list
        return Replay(**data)
