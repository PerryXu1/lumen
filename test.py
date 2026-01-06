import numpy as np
import matplotlib.pyplot as plt
from src.lumen.circuit.components.coupler import Coupler
from src.lumen.circuit.components.hwp import HWP
from src.lumen.circuit.components.polarization_beam_splitter import PolarizationBeamSplitter
from src.lumen.circuit.components.phase_shifter import PhaseShifter
from src.lumen.circuit.components.beam_splitter import BeamSplitter
from src.lumen.display.polarization_view_3d import PolarizationView3D
from src.lumen.display.polarization_ellipse import PolarizationEllipse
from src.lumen.circuit.component import PortRef
from src.lumen.display.poincare import Poincare
from src.lumen.models.stokes import Stokes
from src.lumen.models.light import FixedWavelengthCoherentLight, Light, CoherentLight, IncoherentLight
from src.lumen.circuit.laser import Laser
from src.lumen.circuit.components.qwp import QWP
from src.lumen.circuit.photonic_circuit import PhotonicCircuit
from src.lumen.simulation.simulation import Simulation

circuit = PhotonicCircuit()
coupler1 = Coupler(central_wavelength_H=1550e-9, central_wavelength_V=1550e-9,
                   central_coupling_strength_H=5e3, central_coupling_strength_V=8e3,
                   coupling_gradient_H=2e11, coupling_gradient_V=1e12,
                   length=1e-4, insertion_loss_db=0)
ps1 = PhaseShifter(nH=2.45, central_wavelength_H=1550e-9, 
                   nH_gradient=-1.1e6, nV=1.85, central_wavelength_V=1550e-9,
                   nV_gradient=-0.5e6, length=4e-4, power_ratio_H=300, power_ratio_V=100)
circuit.add(coupler1)
circuit.add(ps1)

def lf1(t: float) -> CoherentLight:
    wavelength = 1540e-9 + 2e-9 * t
    return CoherentLight.from_jones(1, 1, wavelength)

laser1 = Laser(light_func=lf1)

circuit.set_circuit_input(laser=laser1, port_ref=PortRef(coupler1, 1))
circuit.connect(source=PortRef(coupler1, 4), destination=PortRef(ps1, 1))
circuit.connect(source=PortRef(ps1, 2), destination=PortRef(coupler1, 2))
circuit.set_circuit_output(port_ref=PortRef(coupler1, 3))

sim = Simulation(circuit)
output = sim.simulate(np.linspace(0, 10, 500))

# 1. Create the figure and axis
plt.figure(figsize=(10, 6))

# 2. Plot both lines
# We usually use 'nm' for the x-axis display, so we multiply SI meters by 1e9
plt.plot(output.get_wavelengths(PortRef(coupler1, 3)) * 1e9, output.get_power_H(PortRef(coupler1, 3)), label='Horizontal (TE)', color='blue', linewidth=1.5)
plt.plot(output.get_wavelengths(PortRef(coupler1, 3)) * 1e9, output.get_power_V(PortRef(coupler1, 3)), label='Vertical (TM)', color='red', linestyle='--', linewidth=1.5)

# 3. Add labels and title
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Wavelength Sweep: Resonance Dips')

# 4. Add a legend and grid
plt.legend()
plt.grid(True, which='both', linestyle=':', alpha=0.5)

# 5. Show the plot
plt.show()