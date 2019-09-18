from dataclasses import dataclass, field
from tkinter import *
from typing import List

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

    def _swap_buffer(self, buffer: Image.Image):
        buffer = ImageTk.PhotoImage(buffer)
        self._label.configure(image=buffer)
        self._label.image = buffer

    def _update(self):
        bitmap = pipeline(self.camera, self.meshes, Light(glm.vec3(1.2, 1.0, 5.0)), self.width, self.height)
        self._swap_buffer(bitmap)
        self._window.after(1, self._update)

    def run(self):
        self._update()
        self._window.mainloop()


obj = Mesh.from_obj_file('./models/head.obj')
window = Display(WIDTH, HEIGHT, 'Software 3D render')
window.meshes.extend([obj])
window.run()
