from dataclasses import dataclass
from typing import NoReturn, Sequence, Tuple

import glm
from PIL import Image, ImageDraw

from mesh import Mesh, Face


Point2D = Tuple[int, int]


@dataclass
class Camera:
    position: glm.vec3
    target: glm.vec3
    up: glm.vec3 = glm.vec3(0.0, 1.0, 0.0)


@dataclass
class Light:
    position: glm.vec3
    color: glm.vec3 = glm.vec3(1.0, 1.0, 1.0)

    def get_diffuse_color(self, face: Face, model: glm.mat4) -> glm.vec3:
        normal = glm.mat3(glm.transpose(glm.inverse(model))) * face.normal
        frag_pos = glm.vec3(model * glm.vec4(face.p0, 1.0))
        light_dir = glm.normalize(self.position - frag_pos)
        diff = glm.clamp(glm.dot(normal, light_dir), 0.0, 1.0)
        return diff * self.color


def get_model_matrix(mesh: Mesh) -> glm.mat4:
    # TODO adding rotation!
    scale_matrix = glm.scale(glm.mat4(), mesh.scale)
    translate_matrix = glm.translate(glm.mat4(), mesh.position) * scale_matrix
    return translate_matrix


def true_round(i: float) -> int:
    if i % 1 >= 0.5:
        i += 0.5
    return int(i)


def world_to_screen(vertex: glm.vec4, width: float, height: float) -> Point2D:
    ndc_space_pos = vertex.xyz / vertex.w
    x = ndc_space_pos.x * width + width / 2
    y = -ndc_space_pos.y * height + height / 2
    return true_round(x), true_round(y)


def is_clipped(vec: glm.vec4) -> bool:
    for i in glm.vec3(vec):
        if i > 1 or i < -1:
            return True
    return False


def draw_face(bitmap: Image.Image, face: Face, mvp: glm.mat4, width: float, height: float, fill: tuple) -> NoReturn:
    # TODO adding culling invisible vertex
    draw = ImageDraw.Draw(bitmap)
    p0: glm.vec4 = mvp * glm.vec4(face.p0, 1.0)
    p1: glm.vec4 = mvp * glm.vec4(face.p1, 1.0)
    p2: glm.vec4 = mvp * glm.vec4(face.p2, 1.0)

    p0: Point2D = world_to_screen(p0, width, height)
    p1: Point2D = world_to_screen(p1, width, height)
    p2: Point2D = world_to_screen(p2, width, height)

    draw.line((p0, p1), fill=fill)
    draw.line((p1, p2), fill=fill)
    draw.line((p2, p0), fill=fill)
    draw.polygon((p0, p1, p2), fill=fill)


def pipeline(camera: Camera, meshes: Sequence[Mesh], light: Light, width: int, height: int) -> Image.Image:
    # TODO adding true backface culling and Z-buffer!
    bitmap = Image.new('RGBA', (width, height), color='black')
    for mesh in meshes:
        projection_matrix = glm.perspective(glm.radians(90.0), width/height, 0.1, 1000.0)
        view_matrix = glm.lookAt(camera.position, camera.target, camera.up)
        model_matrix = get_model_matrix(mesh)
        mvp = projection_matrix * view_matrix * model_matrix
        for face in mesh.faces:
            dot = glm.dot(face.p0 - camera.position, face.normal)
            if dot >= 0:
                continue
            diffuse = light.get_diffuse_color(face, model_matrix)
            ambient_strength = 0.1
            ambient = ambient_strength * light.color
            result = glm.vec4((ambient + diffuse) * mesh.color, 1.0)
            draw_face(bitmap, face, mvp, width, height, fill=tuple(map(int, result * 255)))
    return bitmap
