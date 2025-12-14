from abc import abstractmethod, ABC
# TODO: remove this import
import numpy as np

from lumen.dataclasses.light import Light

class Display(ABC):

    def __init__(self, light: Light):
        self.light = light
        # TODO: remove the super().__init__() line
        super().__init__()

    # TODO: self has to be the first parameter for this
    @abstractmethod
    def display():
        """A way to display the light data"""
        # TODO: do pass or ... instead of return
        return