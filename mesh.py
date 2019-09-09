import pathlib
from dataclasses import dataclass
from typing import Optional, List

from gmath import vec3
from help import group_by


@dataclass
class Face:
    p0: vec3
    p1: vec3
    p2: vec3

    @property
    def normal(self) -> vec3:
        normal = (self.p1 - self.p0).cross(self.p2 - self.p0)
        return normal.normalize()


@dataclass
class Mesh:
    """Mesh class for models"""
    name: str
    vertexes: List[vec3]
    indexes: List[int]
    position: vec3 = vec3(0., 0., 0.)
    rotation: vec3 = vec3(0., 0., 0.)
    scale: vec3 = vec3(1., 1., 1.)

    @property
    def faces(self):
        for p0, p1, p2 in group_by(self.indexes, 3):
            yield Face(self.vertexes[p0 - 1], self.vertexes[p1 - 1], self.vertexes[p2 - 1])

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
                    vertexes.append(vec3(*args))
                elif name == 'f':
                    indexes.extend(int(i.split('/')[0]) for i in args)
        return cls(name or file.name, vertexes, indexes)
