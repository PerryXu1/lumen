from typing import Literal
from ..component import Component
import numpy as np
from numpy.typing import NDArray

class HWP(Component):
    """2-port polarization retarder. Shifts phase between fast and slow axes by pi.

    ## Port Designations
    - Inputs: Port 1
    - Outputs: Port 2

    ## Port Mapping
    - Port 1 <-> Port 2

    ## Effect
    Shifts phase between fast and slow axes by pi (180 deg). Used to rotate linear polarization.

        
    :param angle: The angle that the QWP is oriented relative to the horizontal state (radians)
    :type angle: float
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_num_outputs", "_ports", "_port_aliases",
                 "_port_ids", "_in_degree", "_out_degree", "angle")
    
    _COMPONENT_NAME = "QWP"

    def __init__(self, *, angle: float):
        self.angle = angle
        super().__init__(self._COMPONENT_NAME, 1, 1)
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        cos = np.cos(2*self.angle)
        sin = np.sin(2*self.angle)
        
        return np.array([
            [    0,    0,  cos,  sin],
            [    0,    0,  sin, -cos],
            [  cos,  sin,    0,    0],
            [  sin, -cos,    0,    0]
        ], dtype=float)
