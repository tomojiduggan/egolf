"""
File storing all the props class used in game
"""
import numpy as np

id_track = 0


def get_new_id():
    id_track += 1
    return id_track


class Props(object):
    def __init__(self, position, movable, prop_id):
        self.position = position
        self.movable = movable
        self.prop_id = prop_id


class WIRE:
    def __init__(self, start, end, current):  # start and end are positions of the two ends of the wire
        self.start = start
        self.end = end
        self.vec_l = end - start
        self.current = current

    def b_field(self, r):
        x1_r = r - self.start
        x2_r = r - self.end
        c1 = np.dot(x1_r, self.vec_l) / np.linalg.norm(x1_r)
        c2 = -np.dot(x2_r, self.vec_l) / np.linalg.norm(x2_r)
        norm_b_phi = self.current / (np.linalg.norm(self.vec_l)) * (c1 + c2)
        # Finding orientation (to find sign) using cross product
        cross_prod = x1_r[0] * self.vec_l[1] - x1_r[1] * self.vec_l[0]
        if (cross_prod > 0):
            return norm_b_phi
        elif (cross_prod < 0):
            return -norm_b_phi
        else:
            return 0

    def current_swap(self):
        self.current *= -1


class POINT_CHARGE(Props):
    def __init__(self, position, charge, movable):  # position is numpy array length 2
        super().__init__(position, movable, get_new_id())
        self.charge = charge
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)

    def e_field(self, r):
        return self.charge * (r - self.position) / (np.linalg.norm(r - self.position))

    def get_force(self):
        e_force = self.charge * net_E(self.position)
        b = net_B(self.position)
        b_force = np.array([self.velocity[1] * b, -self.velocity[0] * b])

        return e_force + b_force

    def update(self, force):  # force is np array
        if (not self.movable):
            print("Warning: Trying to move non-movable")
            return

        self.acceleration = force  # say mass is 1
        self.velocity += self.acceleration * DELTA_T
        self.position += self.velocity * DELTA_T
