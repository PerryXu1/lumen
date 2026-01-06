from typing import Literal
from ..component import Component
import numpy as np
from numpy.typing import NDArray

class QWP(Component):
    """2-port polarization retarder. Shifts phase between fast and slow axes by pi/2.

    ## Port Designations
    - Inputs: Port 1
    - Outputs: Port 2

    ## Port Mapping
    - Port 1 <-> Port 2

    ## Effect
    Shifts phase between fast and slow axes by pi/2 (90 deg). Used to convert between 
    linear and circular polarization.
        
    :param angle: The angle that the QWP is oriented relative to the horizontal state (radians)
    :type angle: float | Literal["horizontal", "vertical"]
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_num_outputs", "_ports", "_port_aliases",
                 "_port_ids", "_in_degree", "_out_degree" "angle")
    
    _COMPONENT_NAME = "QWP"

    def __init__(self, *, angle: float | Literal["horizontal", "vertical"]):
        if self.angle == "horizontal":
            self.angle = 0
        elif self.angle == "vertical":
            self.angle = np.pi / 2
        elif isinstance(self.angle, float):
            self.angle = angle
        super().__init__(self._COMPONENT_NAME, 1, 1)
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        J11 = np.cos(self.angle) ** 2 + 1j * np.sin(self.angle) ** 2
        J_off_diagonal = (1 - 1j) * np.sin(self.angle) * np.cos(self.angle)
        J22 = np.sin(self.angle) ** 2 + 1j * np.cos(self.angle) ** 2
        
        return np.exp(-1j * np.pi / 4) * np.array([
            [0, 0, J11, J_off_diagonal],
            [0, 0, J_off_diagonal, J22],
            [J11, J_off_diagonal, 0, 0],
            [J_off_diagonal, J22, 0, 0]
        ], dtype=complex)
