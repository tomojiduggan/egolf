"""
File storing all the props class used in game
"""
import numpy as np
from Global_Var import *
from physics.phys_utils import *
# from main import screen
import pygame



class Props(object):
    def __init__(self, position, movable):
        self.position = position
        self.movable = movable
        self.prop_id = len(ALL_PROPS)
        self.has_E = False
        self.has_B = False
        ALL_PROPS.append(self)
    

    def update(self):
        """
        on each update, for most prop do nothing
        """
        return

class REGION(Props):
    """
    Abstract class for rectangular region
    """
    def __init__(self, tl, br, color=(255, 0, 0)):
        super().__init__(np.array([(br[0]-tl[0])/2, (br[1]-tl[1])/2]), False)
        self.tl = tl
        self.br = br
        self.width = br[0]-tl[0]
        self.height = br[1]-tl[1]
        self.rect = pygame.Rect(tl[0], tl[1], self.width, self.height)

        self.color = color

    def draw(self, screen):
        """Draw the wall on the given screen with the specified color."""
        pygame.draw.rect(screen, self.color, self.rect)

class WALL(REGION):
    """
    Wall class representing perfectly elastic boxes that interacts with collision (objected decleared this class will
    be checked with collision system.
    """
    def __init__(self, tl, br):
        super().__init__(tl, br)

class WIN(REGION):
    """
    class representing the rectangular region that represents winning.
    """
    def __init__(self, tl, br):
        super().__init__(tl, br)

class WIRE(Props):
    def __init__(self, start, end, current):  # start and end are positions of the two ends of the wire
        self.position = (end - start) / 2
        self.movable = False
        super().__init__((end - start) / 2, False)
        
        self.start = start
        self.end = end
        self.vec_l = end - start
        self.current = current
        self.has_B = True

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

    def update(self):
        return

    def draw(self, screen):
        return

    def current_swap(self):
        self.current *= -1


class POINT_CHARGE(Props):
    def __init__(self, position, charge, movable):  # position is numpy array length 2
        super().__init__(position, movable)
        self.charge = charge * Q
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.radius = 15
        self.image_path = "img/charge.jpg"
        self.has_E = True
        if(movable):
            self.has_B = True

    def draw(self, screen):
        image = pygame.image.load(self.image_path)
        # pygame.transform.scale_by(image, )
        image = pygame.transform.scale(image, (30, 30))
        screen.blit(image, image.get_rect(center=self.position))

    def e_field(self, r):
        return self.charge * (r - self.position) / (np.linalg.norm(r - self.position))

    def b_field(self, r):
        if(not self.movable):
            return 0
        return self.charge * np.cross(self.velocity, self.position - r) / (np.linalg.norm(self.position - r) ** 3)

    def get_force(self):
        e_force = self.charge * net_E(self.position, self.prop_id)
        b = net_B(self.position, self.prop_id)
        b_force = np.array([self.velocity[1] * b, -self.velocity[0] * b])
        em_force = e_force + b_force
        if(np.max(self.velocity) < 0.001 and np.linalg.norm(em_force) < FRICTION):
            self.velocity = np.array([0, 0])
            return np.array([0, 0])
        else:
            return em_force - FRICTION * self.velocity / np.linalg.norm(self.velocity)

    def update(self):  # force is np array
        if (not self.movable):
            return
        force = self.get_force()

        self.acceleration = force # say mass is 1
        self.velocity = self.velocity + self.acceleration * DELTA_T
        self.position = self.position + self.velocity * DELTA_T



class PLAYER(POINT_CHARGE):
    def __init__(self, position):
        super().__init__(position, PLAYER_CHARGE, True)
        self.prop_id = -1 #Special ID for player
        self.rect = pygame.Rect(
                    self.position[0] - self.radius,
                    self.position[1] - self.radius,
                    self.radius * 2,
                    self.radius * 2,
                )

    def handle_collisions(self):
        """
        Checks for collisions with all props, infer different action depending on colliding object
        """
        for p in ALL_PROPS:
            if isinstance(p, WALL):
                if p.rect.colliderect(self.rect):
                    # Determine the direction of collision
                    if self.velocity[0] >= 0 and self.velocity[1] >= 0: # bot right v
                        if self.position[0] >= p.tl[0]:
                            normal = np.array([0, 1]) # top
                        else:
                            normal = np.array([1, 0]) # left
                    elif self.velocity[0] >= 0 and self.velocity[1] < 0:# top right v
                        if self.position[0] >= p.tl[0]:
                            normal = np.array([0, -1]) # bot
                        else:
                            normal = np.array([1, 0])  # left
                    elif self.velocity[0] < 0 and self.velocity[1] >= 0: # bot left v
                        if self.position[0] >= p.br[0]:
                            normal = np.array([-1, 0])  # right
                        else:
                            normal = np.array([0, 1])  # top
                    else: # top left v
                        if self.position[0] >= p.br[0]: # right
                            normal = np.array([-1, 0])
                        else:
                            normal = np.array([0, -1]) # bot

                    # Calculate the perpendicular component of the velocity (normal component)
                    velocity_normal_component = np.dot(self.velocity, normal) * normal

                    # Reverse the normal component of the velocity (bounce effect)
                    self.velocity -= 2 * velocity_normal_component

            elif isinstance(p, POINT_CHARGE) and p.prop_id != -1:
                # Circular collision check
                distance = np.linalg.norm(self.position - p.position)
                if distance - 2 * self.radius <= 0:
                    print("Collision detected", p.position)

            elif isinstance(p, WIN):
                if p.rect.colliderect(self.rect):
                    print("You Win")
                    # TODO: Implement winning screen


    def update(self):
        """
        Addition need to update bounding box on each tick
        """
        super().update()
        self.rect = pygame.Rect(
            self.position[0] - self.radius,
            self.position[1] - self.radius,
            self.radius * 2,
            self.radius * 2,
        )
class SOLENOID(Props):
    def __init__(self, num_loops, current, direction, position, image_path):
        self.num_loops = num_loops
        self.current = current
        self.direction = np.array(direction) / np.linalg.norm(direction)  # Normalize the direction vector
        self.position = list(position)  # Convert to list for mutability
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=self.position)
        self.length = self.rect.width  # Assuming the solenoid is a rectangle
        self.movable = True
        self.is_dragging = False

        self.has_B = True

    def draw(self, screen):
        """Draw the solenoid on the screen."""
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        """Handle mouse events for dragging."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y
                self.position = [self.rect.x, self.rect.y]

    def b_field(self, point):
        """
        Calculate the magnetic field at a given point using the short solenoid approximation.

        :param point: A 3D numpy array [x, y, z].
        :return: Magnetic field vector as a numpy array [Bx, By, Bz].
        """
        # mu_0 = 4 * np.pi * 1e-7  # Magnetic constant (T·m/A)
        mu_0 = 1e-3
        n = self.num_loops / self.length  # Turns per unit length

        # Convert point to a numpy array and find relative position
        point = np.array(point)
        dx, dy = point[:2] - self.position[:2]
        r = np.sqrt(dx**2 + dy**2)  # Distance in 2D plane

        # Short solenoid approximation for field strength
        B_magnitude = mu_0 * n * self.current / 2

        # Decay field for global effect (outside solenoid)
        decay_factor = self.length / (self.length + r)  # Approximate global influence
        B_magnitude *= decay_factor

        # Assume the field is along z-axis (out of plane)
        B_field = np.array([0, 0, B_magnitude])
        return B_field
