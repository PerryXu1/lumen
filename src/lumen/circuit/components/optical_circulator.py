from ..component import Component
import numpy as np
from numpy.typing import NDArray

class OpticalCirculator(Component):
    """Non-reciprocal 3-Port Circulator.

    ## Port Mapping (Unidirectional)
    - Port 1 -> Port 2
    - Port 2 -> Port 3
    - Port 3 -> Port 1

    ## Effect
    Routes signals in a one-way loop: Port 1 -> Port 2 -> Port 3 -> Port 1.
    
    Preserves polarization state across ports.
    
    :param insertion_loss: Power lost during transmission [dB]
    :type insertion_loss: float
    :param isolation_leakage: Power that leaks in the wrong direction (E.g. Port 2 -> Port 1) [dB]
    :type isolation_leakage: float
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_num_outputs", "_ports", "_port_aliases",
                 "_port_ids", "_in_degree", "_out_degree", "insertion_loss", "isolation_leakage")
    
    _COMPONENT_NAME = "OC"

    def __init__(self, *, insertion_loss: float, isolation_leakage: float):
        super().__init__(self._COMPONENT_NAME, 1, 1)
        self.insertion_loss = insertion_loss
        self.isolation_leakage = isolation_leakage
        
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        tau = 10 ** (-self.insertion_loss / 20)
        epsilon = 10 ** (-self.isolation_leakage / 20)
        
        return np.array([
            [0, 0, epsilon, 0, tau, 0],
            [0, 0, 0, epsilon, 0, tau],
            [tau, 0, 0, 0, epsilon, 0],
            [0, tau, 0, 0, 0, epsilon],
            [epsilon, 0, tau, 0, 0, 0],
            [0, epsilon, 0, tau, 0, 0]
        ], dtype=float)