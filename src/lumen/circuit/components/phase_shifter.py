from ..component import Component
import numpy as np
from numpy.typing import NDArray

class PhaseShifter(Component):
    """2-port (1 input, 1 output) waveguide segment that applies a phase delay to the signal.
    Can be used to model a propagation segment (waveguide/fibre).

    ## Port Designations
    - Inputs: Port 1
    - Outputs: Port 2

    ## Port Mapping
    - Port 1 <-> Port 2

    ## Effect
    Applies exp(i * phi) to the field, where phi = (2 * pi * n_eff * L) / lambda.
    Horizontal and Vertical modes may have different refractive indices (nH, nV),
    resulting in different phase shifts for each polarization.
    
    :param nH: Refractive index for the horizontal mode (unitless)
    :type nH: float
    :param nV: Refractive index for the vertical mode (unitless)
    :type nV: float
    :param length: Length of the phase shifter (metres)
    :type length: float
    :param power_ratio_H: Power ratio representing transmission loss in the horizontal mode (dB/m)
    :type power_ratio_H: float
    :param power_ratio_V: Power ratio representing transmission loss in the vertical mode (dB/m)
    :type power_ratio_V: float
    """
    
    __slots__ = ("id", "name", "_num_inputs", "_num_outputs", "_ports", "_port_aliases",
                 "_port_ids", "_in_degree", "_out_degree", "nH", "nH_gradient", "central_wavelength_H",
                 "nV", "nV_gradient", "central_wavelength_V", "length", "power_ratio_H", "power_ratio_V")
    
    _COMPONENT_NAME = "PS"

    def __init__(self, *, nH: float, nH_gradient: float, central_wavelength_H: float,
                 nV: float, nV_gradient: float, central_wavelength_V: float,
                 length: float, power_ratio_H: float = 0, power_ratio_V: float = 0):
        super().__init__(self._COMPONENT_NAME, 1, 1)
        self.nH = nH
        self.nH_gradient = nH_gradient
        self.central_wavelength_H = central_wavelength_H
        self.nV = nV
        self.nV_gradient = nV_gradient
        self.central_wavelength_V = central_wavelength_V
        self.length = length
        self.power_ratio_H = power_ratio_H
        self.power_ratio_V = power_ratio_V
    
    def get_s_matrix(self, wavelength: float) -> NDArray[np.complex128]:
        """Returns the modified S matrix that mathematically represents the component
        
        :param wavelength: Wavelength of the light going through the component
        :type wavelength: float
        :return: The modified S matrix
        :rtype: NDArray[np.complex128]
        """
        
        nH_group = self.nH - (wavelength - self.central_wavelength_H) * self.nH_gradient
        nV_group = self.nV - (wavelength - self.central_wavelength_V) * self.nV_gradient
        
        phase_H = (2 * np.pi * nH_group * self.length) / wavelength
        phase_V = (2 * np.pi * nV_group * self.length) / wavelength
        a_H = 10 ** ((-self.power_ratio_H * self.length) / 20)
        a_V = 10 ** ((-self.power_ratio_V * self.length) / 20)
        
        return np.array([
            [ 0, 0, a_H * np.exp(-1j * phase_H), 0],
            [ 0, 0, 0, a_V * np.exp(-1j * phase_V)],
            [ a_H * np.exp(-1j * phase_H), 0, 0, 0],
            [ 0, a_V * np.exp(-1j * phase_V), 0, 0]
        ])