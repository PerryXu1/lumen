from ...models.light import CoherentLight
from ..component import Component
import numpy as np
from numpy.typing import NDArray

class PhaseShifter(Component):
    """Conceptual representation of a phase shifter within the photonics circuit. Models how
    light changes as it travels through a medium of certain length and optical properties. Has
    2 ports (1 input, 1 output).
    
    :param nH: Refractive index for the horizontal mode
    :type nH: float
    :param nV: Refractive index for the vertical mode
    :type nV: float
    :param length: Length of the phase shifter
    :type length: float
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_input_ports", "_input_port_aliases",
                "_input_port_ids", "_num_outputs", "_output_ports", "_output_port_aliases",
                "_output_port_ids", "_in_degree", "_out_degree", "nH", "nV", "length")
    
    _COMPONENT_NAME = "PS"

    def __init__(self, nH: float, nV: float, length: float):
        super().__init__(self._COMPONENT_NAME, 1, 1)
        self.nH = nH
        self.nV = nV
        self.length = length
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        phase_H = (2 * np.pi * self.nH * self.length) / wavelength
        phase_V = (2 * np.pi * self.nV * self.length) / wavelength
        
        return np.array([
            [                     0,                     0, np.exp(-1j * phase_H),                     0],
            [                     0,                     0,                     0, np.exp(-1j * phase_V)],
            [ np.exp(-1j * phase_H),                     0,                     0,                     0],
            [                     0, np.exp(-1j * phase_V),                     0,                     0]
        ])