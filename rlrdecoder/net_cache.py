from dataclasses import dataclass
from typing import List


@dataclass
class NetCache:
    is_root: bool = False
    object_index: int = None
    parent_id: int = None
    parent: 'NetCache' = None
    cache_id: int = None
    properties: list = None
    children_ids: List[int] = None
    children: List['NetCache'] = None

    def __str__(self):
        return f'NetCache(is_root={self.is_root}, object_index={self.object_index}, ' \
                f'parent_id={self.parent_id}, cache_id={self.cache_id}, ' \
                f'properties={self.properties}, children_ids={self.children_ids})'
