from ...models.light import CoherentLight
from ..component import Component
import numpy as np
from numpy.typing import NDArray

class PolarizationBeamSplitter(Component):
    """Conceptual representation of a polarization beam splitter (PBS) within the photonics circuit.
    Represented with a 4 port (2 input, 2 output) component to maintain unitarity. H light goes through
    to Output Port 1 while V light goes cross to Output Port 2.
    
    Beam Splitting
    ============
    If only a single input port is connected, the component acts as a beam splitter.
    
    H light is outputted at Output Port 1 while V light is outputted at Output Port 2
    
    Beam Combining
    ============
    If both input ports are connected, the component acts as a beam combiner.
    
    If H light is inputted at Input Port 1 and V light is inputted at Input Port 2, the
    new polarization state is outputted at Output Port 1
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_input_ports", "_input_port_aliases",
                "_input_port_ids", "_num_outputs", "_output_ports", "_output_port_aliases",
                "_output_port_ids", "_in_degree", "_out_degree")
    
    _COMPONENT_NAME = "PBS"

    def __init__(self):
        super().__init__(self._COMPONENT_NAME, 2, 2)
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        return np.array([
                        [   0,   0,   0,   0,   1,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0, -1j],
                        [   0,   0,   0,   0,   0,   0,   1,   0],
                        [   0,   0,   0,   0,   0, -1j,   0,   0],
                        [   1,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0, -1j,   0,   0,   0,   0],
                        [   0,   0,   1,   0,   0,   0,   0,   0],
                        [   0, -1j,   0,   0,   0,   0,   0,   0]
                        ])