"""
Contains all the function related to physics calculation
"""

import numpy as np
import Global_Var as Global_Var
from Global_Var import *
# from physics.props import *


def get_E_level(poi):
    # Get all field except the player
    return net_E(poi, -1)

# Take electric field without prop with id
def net_E(r, id):
    """
    :param r: The position of POI
    :param id: The id of the charge, it will be excluded during E field calculation (It does not feel itself)
    :return: the Sum of eat
    """
    sum_E = np.zeros(2)
    for object in ALL_PROPS:
        if(object.prop_id == id):
            continue
        
        if(object.has_E):
            # If object id is same as input id, then ignore
            sum_E += object.e_field(r)
    return sum_E
        # E-field of other objects...

# Take magnetic field without prop with id
def net_B(r, id):
    sum_B = 0
    for object in ALL_PROPS:
        if(object.prop_id == id):
            continue
        if(object.has_B):
            sum_B += object.b_field(r)

    return sum_B
