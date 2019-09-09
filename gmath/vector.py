from typing import Optional, Union

import numpy as np


class BaseVec(np.ndarray):
    def __new__(cls, items):
        return np.asarray(items, dtype=np.float).view(cls)

    def cross(self, other: 'BaseVec') -> 'BaseVec':
        return BaseVec(np.cross(self, other))

    @property
    def length(self):
        return np.sqrt((self ** 2).sum())

    def normalize(self) -> 'BaseVec':
        return BaseVec(self / self.length)


class Vec3(BaseVec):
    def __new__(cls, x: Union[float, 'Vec4'], y: Optional[float] = None, z: Optional[float] = None):
        if isinstance(x, np.ndarray):
            x, y, z = x[:3]
        return super(Vec3, cls).__new__(cls, [x, y, z])


class Vec4(BaseVec):
    def __new__(cls, x: Union[float, Vec3], y: Optional[float] = None, z: Optional[float] = None, w: float = 1.0):
        if isinstance(x, np.ndarray):
            x, y, z = x
        return super(Vec4, cls).__new__(cls, [x, y, z, w])


vec3 = Vec3
vec4 = Vec4
