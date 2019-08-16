from dataclasses import dataclass, field
from tkinter import *
from typing import List

from PIL import Image, ImageTk, ImageDraw
from pyrr import Matrix44, Vector3

from mesh import Mesh

WIDTH = 1024
HEIGHT = 768


@dataclass
class Display:
    width: int
    height: int
    title: str
    meshes: List['Mesh'] = field(default_factory=list, init=False)

    def __post_init__(self):
        self._window = Tk()
        self._window.resizable(False, False)
        self._window.title(self.title)
        self._window.geometry(f'{self.width}x{self.height}')
        self._label = Label(self._window)
        self._label.pack()
        self._projection = Matrix44.perspective_projection(90, self.width / self.height, 0.1, 1000.0)
        self.angle = 0.0

    def _swap_buffer(self, buffer: Image.Image):
        buffer = ImageTk.PhotoImage(buffer)
        self._label.configure(image=buffer)
        self._label.image = buffer

    def _update(self):
        bitmap = Image.new('RGBA', (self.width, self.height), color='black')
        draw = ImageDraw.Draw(bitmap)
        fill = (255, 255, 255, 255)
        width = 0
        for mesh in self.meshes:
            translate = Matrix44.from_translation(mesh.position)
            # rotation = Matrix44.from_z_rotation(np.deg2rad(self.angle)) * Matrix44.from_x_rotation(np.deg2rad(self.angle))
            for v0, v1, v2 in mesh.triangles:
                v0 = self._projection * translate * v0
                v1 = self._projection * translate * v1
                v2 = self._projection * translate * v2

                # first step

                v0.x += 1.0
                v0.y += 1.0
                v1.x += 1.0
                v1.y += 1.0
                v2.x += 1.0
                v2.y += 1.0

                # next step

                v0.x *= 0.5 * float(self.width)
                v0.y *= 0.5 * float(self.height)
                v1.x *= 0.5 * float(self.width)
                v1.y *= 0.5 * float(self.height)
                v2.x *= 0.5 * float(self.width)
                v2.y *= 0.5 * float(self.height)

                draw.line([*v0.xy, *v1.xy], fill=fill, width=width)
                draw.line([*v1.xy, *v2.xy], fill=fill, width=width)
                draw.line([*v2.xy, *v0.xy], fill=fill, width=width)

        self.angle += 1

        self._swap_buffer(bitmap)
        self._window.after(1, self._update)

    def run(self):
        self._update()
        self._window.mainloop()


# triangle = Mesh('triangle',
#                 [
#                     Vector3([0.0, 1.0, 0.0]),
#                     Vector3([1.0, 0.0, 0.0]),
#                     Vector3([-0.5, 0.5, 0.0]),
#                 ],
#                 [0, 1, 2],
#                 position=Vector3([0., 0., 3.]))
african_head = Mesh.load_from_obj_file('./african_head.obj', 'head')
african_head.position = Vector3([0, 0, 3])
window = Display(WIDTH, HEIGHT, 'Software 3D render')
window.meshes.extend([african_head])
window.run()
