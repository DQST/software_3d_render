from dataclasses import dataclass, field
from tkinter import *
from typing import List
import time

from PIL import Image, ImageTk
import glm

from mesh import Mesh
from pipeline import pipeline, Camera, Light


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
        self.camera = Camera(glm.vec3(0, 2, 5), glm.vec3(0, 0, 0))
        self.light = Light(glm.vec3(1.2, 1.0, 5.0))
        self.angle = 0
        self.last_time = 0.0
        self.delta = 0.0

    def _update(self):
        current_frame = time.time()
        self.delta = current_frame - self.last_time
        self.last_time = current_frame
        print(f'delta = {self.delta}')
        angle = glm.radians(self.angle)
        print(f'angle = {angle}')
        light_x = self.light.position.x * glm.cos(angle) - self.light.position.z * glm.sin(angle)
        light_z = self.light.position.z * glm.cos(angle) + self.light.position.x * glm.sin(angle)
        self.light.position = glm.vec3(light_x, self.light.position.y, light_z)
        self.angle += 0.5 * self.delta

    def _swap_buffer(self, buffer: Image.Image):
        buffer = ImageTk.PhotoImage(buffer)
        self._label.configure(image=buffer)
        self._label.image = buffer

    def _render(self):
        self._update()
        bitmap = pipeline(self.camera, self.meshes, self.light, self.width, self.height)
        self._swap_buffer(bitmap)
        self._window.after(10, self._render)

    def run(self):
        self._render()
        self._window.mainloop()


obj = Mesh.from_obj_file('./models/head.obj')
window = Display(WIDTH, HEIGHT, 'Software 3D render')
window.meshes.extend([obj])
window.run()
