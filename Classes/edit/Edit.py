#This is a superclass that defines the behavior of all of its subclasses

from Classes.info.Arguments import Arguments
from Classes.image.Image import Image

class Edit():
  def edit(self, args: Arguments) -> Image:
    pass
