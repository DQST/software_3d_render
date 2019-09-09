import numpy as np


def identity_matrix() -> np.ndarray:
    return np.identity(4, dtype=np.float64)


def scale_matrix(x: float, y: float, z: float) -> np.ndarray:
    matrix = identity_matrix()
    matrix[np.diag_indices_from(matrix)] = [x, y, z, 1]
    return matrix


def translate_matrix(x: float, y: float, z: float) -> np.ndarray:
    matrix = identity_matrix()
    matrix[:3, 3] = [x, y, z]
    return np.array(matrix, dtype=np.float64)


def x_rotation_matrix(angle: float) -> np.ndarray:
    matrix = identity_matrix()
    matrix[1, 1:3] = [np.cos(angle),   -np.sin(angle)]
    matrix[2, 1:3] = [np.sin(angle),    np.cos(angle)]
    return matrix


def y_rotation_matrix(angle: float) -> np.ndarray:
    matrix = identity_matrix()
    matrix[0, :3] = [np.cos(angle), 0, np.sin(angle)]
    matrix[2, :3] = [-np.sin(angle), 0, np.cos(angle)]
    return matrix


def z_rotation_matrix(angle: float) -> np.ndarray:
    matrix = identity_matrix()
    matrix[0, :2] = [np.cos(angle),    -np.sin(angle)]
    matrix[1, :2] = [np.sin(angle),     np.cos(angle)]
    return matrix
