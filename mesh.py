from dataclasses import dataclass
from typing import Iterable, Optional

import numpy as np
from pyrr import Vector3


@dataclass
class Mesh:
    name: str
    vertexes: Iterable[Vector3]
    indexes: Iterable[int]
    position: Vector3 = Vector3([0., 0., 0.])
    rotation: Vector3 = Vector3([0., 0., 0.])
    scale: Vector3 = Vector3([1., 1., 1.])

    @property
    def triangles(self):
        r = []
        for i, e in enumerate(self.indexes, 1):
            r.append(self.vertexes[e-1])
            if i % 3 == 0:
                yield r
                r = []

    @classmethod
    def load_from_obj_file(cls, path: str, name: Optional[str] = None):
        vertexes = []
        indexes = []
        with open(path) as file:
            for line in file:
                if not line.startswith(('v', 'f')):
                    continue
                name, *args = line.split()
                if name == 'v':
                    vertexes.append(Vector3(args, dtype=np.float64))
                elif name == 'f':
                    indexes.extend(int(i.split('/')[0]) for i in args)
        return cls(name or file.name, vertexes, indexes)
