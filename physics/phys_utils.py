"""
Contains all the function related to physics calculation
"""

import numpy as np
import Global_Var as Global_Var
from physics.props import *

def coulomb_sim_at_poi(positions, charges, poi, unit_vec=False):
    """
    Compute the E field (simulated constant) positions and charges corresponds by index
    :param positions: Array (n, 2) of all the position
    :param charges: Array(n, ) of all the charges
    :param poi: Vector (x, y) (2,) point of interest
    :return: Vector (x, y), if unit vector, then return unit vector
    """
    r = (poi - positions)/100 # 100 pixel is 1m
    r_magnitudes = np.linalg.norm(r, axis=1)

    # Compute the electric field contribution from each charge
    r_unit_vectors = r / r_magnitudes[:, np.newaxis]  # Normalize vectors, shape (n, 3)
    e_field_contributions = (charges[:, np.newaxis] * r_unit_vectors) / r_magnitudes[:, np.newaxis] ** 2

    # Sum the contributions
    e_field = np.sum(e_field_contributions, axis=0)

    return e_field


# Take electric field without prop with id
def net_E(r, id):
    sum_E = np.zeros(2)
    for object in ALL_PROPS:
        if(object.prop_id == id):
            pass
        
        if(object.has_E):
            # If object id is same as input id, then ignore
            sum_E += object.e_field(r)
    return sum_E
        # E-field of other objects...

# Take magnetic field without prop with id
def net_B(r):
    sum_B = 0
    for object in ALL_PROPS:
        if(object.prop_id == id):
            pass
        if(object.has_B):
            sum_B += object.b_field(r)

    return sum_B
