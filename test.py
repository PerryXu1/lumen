import numpy as np
from src.lumen.display.polarization_view_3d import PolarizationView3D
from src.lumen.display.polarization_ellipse import PolarizationEllipse
from src.lumen.circuit.component import PortRef
from src.lumen.display.poincare import Poincare
from src.lumen.models.stokes import Stokes
from src.lumen.models.light import Light
from src.lumen.circuit.laser import Laser
from src.lumen.circuit.components.qwp import QWP
from src.lumen.circuit.photonic_circuit import PhotonicCircuit
from src.lumen.simulation.simulation import Simulation



circuit = PhotonicCircuit()
qwp1 = QWP(fast_axis="vertical")
qwp2 = QWP(fast_axis="horizontal")
circuit.add(qwp1)
circuit.add(qwp2)
circuit.connect(
    PortRef(qwp1, 0),
    PortRef(qwp2, 0)
)
# circuit.connect(qwp1, 0, qwp2, 0)
# circuit.connect(qwp1, 0, qwp2, 0)
# circuit.connect(qwp2, 0, qwp3, 0)

def lf(_: float) -> Light:
    stokes = Stokes(0, 0, 0, 0)
    return Light.from_stokes(stokes=stokes)
    
laser = Laser(light_func=lf)
display1 = Poincare()

circuit.set_circuit_input(laser, PortRef(qwp1, 0))
circuit.set_circuit_output(PortRef(qwp2, 0))

sim = Simulation(circuit)
output = sim.simulate([0, 1, 2])
display2 = PolarizationView3D()
# display1.display()
display2.display_one(output[0])
