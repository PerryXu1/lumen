from typing import Optional

from ..models.port import PortType
from ..models.light import Coherence


class InvalidLightTypeException(Exception):
    """Exception thrown when a coherent light is inputted into something that only
    takes incoherent light, or vice veras
    
    :param light_type: Type of the light inputted (coherent or incoherent)
    :type light_type: Coherence 
    :param message: A message printed when the exception is thrown. If no message
        is given, a default message is printed
    :type message: optional str
    """
    
    __slots__ = "light_type", "coherence"
    
    def __init__(self, coherence: Coherence, message: Optional[str] = None):
        super().__init__(coherence, message)
        self.message = message
        self.light_type = coherence

        
    def __str__(self):
        """Method that defines the message printed when the exception is thrown.
        Either a custom message passed into the constructor or the default message.

        :return: A message to be printed when the exception is thrown
        :rtype: str
        """
        
        if self.message is None:
            if self.light_type == Coherence.COHERENT:
                return "Inputted light is coherent, but only incoherent light is accepted"
            elif self.light_type == Coherence.INCOHERENT:
                return "Inputted light is incoherent, but only coherent light is accepted"
        return self.message

class PortTypeException(Exception):
    """Exception thrown when an input port is used for an output-port-specific task or vice versa
    
    :param port_type: The type of the port inputted
    :type port_type: PortType
    :param message: A message printed when the exception is thrown. If no message
        is given, a default message is printed
    :type message: optional str
    """
    
    __slots__ = "port_type", "message"
    
    def __init__(self, port_type: PortType, message: Optional[str] = None):
        super().__init__(port_type, message)
        self.message = message
        self.port_type = port_type

        
    def __str__(self):
        """Method that defines the message printed when the exception is thrown.
        Either a custom message passed into the constructor or the default message.

        :return: A message to be printed when the exception is thrown
        :rtype: str
        """
        
        if self.message is None:
            if self.light_type == PortType.INPUT:
                return f"Selected port is an input port, but only output ports are accepted"
            elif self.light_type == PortType.OUTPUT:
                return f"Selected port is an output port, but only input ports are accepted"
        return self.message