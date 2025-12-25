from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from lumen.models.light import Light


@dataclass(frozen=True, slots=True)
class DisplaySettings:
    width: int
    height: int
    background_color: str

    def __post_init__(self):
        if self.width <= 0:
            raise ValueError("Parameter 'width' must be positive.")
        if self.height <= 0:
            raise ValueError("Parameter 'height' must be positive.")


class Display(ABC):
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10
    DEFAULT_BACKGROUND_COLOR = "#E6E6E6"

    __slots__ = "light", "settings"

    def __init__(self, light: Light, settings: Optional[DisplaySettings] = None):
        self.light = light
        self.settings = settings if settings is not None else DisplaySettings(
            width=self.DEFAULT_WIDTH,
            height=self.DEFAULT_HEIGHT,
            background_color=self.DEFAULT_BACKGROUND_COLOR,
        )

    @abstractmethod
    def display(self):
        """A way to display the light data"""
        pass

    def create_fig(self) -> Figure:
        return plt.figure(
            figsize=(self.settings.width, self.settings.height),
            facecolor=self.settings.background_color,
            constrained_layout=True
        )
