from collections.abc import Callable
from ..models.light import CoherentLight, FixedWavelengthCoherentLight

class Laser:
    """Representation of a laser input into the circuit
    
    :param light_func: a function mapping a time to a light state
    :type light_func: Callable[float] -> CoherentLight
    """

    # add more parameters
    __slots__ = "_light_func", "wavelength"
    
    def __init__(self, *, light_func: Callable[[float], FixedWavelengthCoherentLight], wavelength: float):
        self._light_func = light_func
        self.wavelength = wavelength
    
    def __call__(self, t: float) -> CoherentLight:
        """Makes the class's light function callable directly through the class
        
        :param t: time
        :type t: float
        :return: The value of the light function at the specified time
        :rtype: CoherentLight
        """
        eh, ev = self._light_func(t).e
        light = CoherentLight(eh, ev, self.wavelength)
        return light