from dataclasses import dataclass
import numpy as np

# TODO: don't put the parenthesis; not needed
@dataclass
class Stokes():
    S0: float
    S1: float
    S2: float
    S3: float
        
    