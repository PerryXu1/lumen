from collections.abc import Sequence
from typing import Optional
from .component import Component
from .exceptions import MissingComponentException
from uuid import uuid4

class PhotonicCircuit:
    """Class representing a photonic circuit composed of components connected to one another. 
    The circuit will initially be empty and users can add components and connect them to build a
    functional circuit.
    """
    
    __slots__ = "_components", "input"

    def __init__(self):
        """Constructor method
        """
        
        self.id = uuid4()
        self._components: Optional[Component] = [] # list of componenets in the circuit
        self.input: Component = None # the component that the laser light inputs to

    def set_input(self, component: Component) -> None:
        """Sets the component that laser light source inputs to.
        
        :param component: The component that the laser light inputs to
        :type component: Component
        """
        
        if component not in self._components:
            raise MissingComponentException(component)
        self.input = component

    def add(self, component: Component) -> None:
        """Adds a component to the circuit.
        
        :param component: The component to be added to the circuit
        :type component: Component
        """
        
        self._components.append(component)

    def connect(self, component1: Component, output_name: str | int, component2: Component, input_name: str | int) -> None:
        """Connect the output of one component in the circuit to the input of another component
        in the circuit.
        
        :param component1: The component whose output is connected
        :type component1: Component
        :param output_name: The alias/index of the output port of component1 that is connected. 
        :type output_name: str (for aliases), int (for indices)
        :param component2: The component whose input is connected
        :type component2: Component
        :param input_name: The alias/index of the input port of component2 that is connected. 
        :type input_name: str (for aliases), int (for indices)
        """
        
        if component1 not in self._components or component2 not in self._components:
            raise Exception("One or both of the components are not in the circuit")
        component1.set_output(output_name, component2, input_name)
        component2.set_input(input_name, component1, output_name)
    
    @property
    def components(self) -> Sequence[Component]:
        """The list of components contained within the circuit. Property of the class.
        
        :return: The list of components contained within the circuit
        :rtype: list of Component
        """
        
        return self._components