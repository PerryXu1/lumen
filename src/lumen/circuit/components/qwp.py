from typing import Literal
from ...models.light import CoherentLight
from ..component import Component
import numpy as np
from numpy.typing import NDArray

class QWP(Component):
    """Conceptual representation of a quarter-wave plate (QWP) within the
    photonics circuit. Has two ports (1 input, 1 output)
        
    :param fast_axis: Specification of whether the QWP's fast axis is aligned
        with the vertical or horizontal state of the light
    :type fast_axis: literal - either the string 'vertical' or the string 'horizontal'
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_input_ports", "_input_port_aliases",
                "_input_port_ids", "_num_outputs", "_output_ports", "_output_port_aliases",
                "_output_port_ids", "_in_degree", "_out_degree", "fast_axis")
    
    _COMPONENT_NAME = "QWP"

    def __init__(self, fast_axis: Literal["vertical", "horizontal"]):
        self.fast_axis = fast_axis
        super().__init__(self._COMPONENT_NAME, 1, 1)
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        if self.fast_axis == "vertical":
            return np.array([[   0,   0, -1j,   0],
                             [   0,   0,   0,   1],
                             [ -1j,   0,   0,   0],
                             [   0,   1,   0,   0]])
        if self.fast_axis == "horizontal":
            return np.array([[   0,   0,   1,   0],
                             [   0,   0,   0, -1j],
                             [   1,   0,   0,   0],
                             [   0, -1j,   0,   0]])