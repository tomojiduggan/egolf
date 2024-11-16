"""
Contains all the function related to physics calculation
"""

import numpy as np

def coulomb_sim_at_poi(positions, charges, poi, constant=1000):
    """
    Compute the E field (simulated constant) positions and charges corresponds by index
    :param positions: Array (n, 3) of all the position
    :param charges: Array(n, ) of all the charges
    :param poi: Vector (x, y, 0) (3,) point of interest
    :return: Vector (x, y, z)
    """
    r = poi - positions
    r_magnitudes = np.linalg.norm(r, axis=1)

    # Compute the electric field contribution from each charge
    r_unit_vectors = r / r_magnitudes[:, np.newaxis]  # Normalize vectors, shape (n, 3)
    e_field_contributions = (charges[:, np.newaxis] * r_unit_vectors) / r_magnitudes[:, np.newaxis] ** 2

    # Sum the contributions
    e_field = np.sum(e_field_contributions, axis=0)

    return e_field


