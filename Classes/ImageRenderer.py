import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import Classes.Renderer as Renderer

class ImageRenderer(Renderer):
    def __init__(self, image: np.ndarray = []) -> None:
        super().__init__(image)
        
    def render_image(self) -> None:
        