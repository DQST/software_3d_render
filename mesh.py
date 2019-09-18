import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Iterator

import glm
from help import group_by


@dataclass
class Face:
    """Face class"""
    p0: glm.vec3
    p1: glm.vec3
    p2: glm.vec3
    normal: glm.vec3 = field(init=False, default=None)

    def __post_init__(self):
        self.normal = glm.normalize(glm.cross(self.p1 - self.p0, self.p2 - self.p0))


@dataclass
class Mesh:
    """Mesh class for models"""
    name: str
    vertexes: List[glm.vec3]
    indexes: List[int]
    position: glm.vec3 = glm.vec3(0., 0., 0.)
    rotation: glm.vec3 = glm.vec3(0., 0., 0.)
    scale: glm.vec3 = glm.vec3(1., 1., 1.)
    color: glm.vec3 = glm.vec3(1.0, 0.5, 0.31)

    @property
    def faces(self) -> Iterator[Face]:
        for p0, p1, p2 in group_by(self.indexes, 3):
            yield Face(self.vertexes[p0], self.vertexes[p1], self.vertexes[p2])

    @classmethod
    def from_obj_file(cls, path: str, name: Optional[str] = None) -> 'Mesh':
        """Create Mesh instance from obj file."""
        path_lib = pathlib.Path(path)
        if not path_lib.exists():
            raise ValueError(f'File "{path_lib.name}" not exists.')

        vertexes = []
        indexes = []
        with open(path) as file:
            for line in file:
                if not line.startswith(('v', 'f')):
                    continue
                name, *args = line.split()
                if name == 'v':
                    args = [float(i) for i in args]
                    vertexes.append(glm.vec3(*args))
                elif name == 'f':
                    indexes.extend(int(i.split('/')[0]) - 1 for i in args)
        return cls(name or file.name, vertexes, indexes)
