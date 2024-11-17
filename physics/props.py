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
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        ALL_PROPS.append(self)
    

    def update(self):
        """
        on each update, for most prop do nothing
        """
        return
    
    def free(self):
        global ALL_PROPS
        if self in ALL_PROPS:
            ALL_PROPS.remove(self)
        self.__dict__.clear()

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

                if(isinstance(self, POINT_CHARGE)):
                    self.position = np.array([self.rect.x + 15, self.rect.y + 15])
                elif(isinstance(self, SOLENOID)):
                    self.position = np.array([self.rect.x + 30, self.rect.y + 30])
                else:
                    self.position = np.array([self.rect.x, self.rect.y])

class REGION(Props):
    """
    Abstract class for rectangular region
    """
    def __init__(self, tl, br, color=(0, 204, 102)):
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
    def __init__(self, tl, br, color=(0, 0, 0)):
        super().__init__(tl, br, color=color)

class BRICK(REGION):
    def __init__(self, tl, br):
        super().__init__(tl, br)
        
        self.distance  = br - tl
        self.position = tl
        self.image = pygame.image.load("pictures/brick.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=self.position)
    def draw(self, screen):
        self.br = self.position + self.distance
        self.tl = self.position
        screen.blit(self.image, self.rect)


class WIN(REGION):
    """
    class representing the rectangular region that represents winning.
    """
    def __init__(self, tl, br):
        super().__init__(tl, br)

class WIRE(Props):
    def __init__(self, start, end, current):  # start and end are positions of the two ends of the wire
        self.position = (end - start) / 2
        self.movable = True
        super().__init__((end - start) / 2, True)
        
        self.start = start
        self.end = end
        self.vec_l = end - start
        self.current = current * I
        self.has_B = True
        self.has_B = True
        top_left = (min(start[0], end[0]), min(start[1], end[1]))
        width = abs(end[0] - start[0])  # Calculate width
        height = abs(end[1] - start[1])  # Calculate height
        self.rect = pygame.Rect(top_left[0], top_left[1], width, height)

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
        pygame.draw.line(screen, "grey", self.start, self.end, width=5)
        pygame.draw.circle(screen, (189, 64, 63), self.start, 10)
        pygame.draw.circle(screen, "blue", self.end, 10)
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
        self.has_E = True
        self.image_path = 'pictures/plus_charge.png'
        if(charge > 0):
            self.image_path = "pictures/plus_charge.png"
        else:
            self.image_path = "pictures/minu_charge.png"
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=self.position - np.array([15, 15]))
        if(movable):
            self.has_B = True

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.position))

    def swap_sign(self):
        self.charge *= -1
        self.image_path = 'pictures/plus_charge.png' if self.charge > 0 else 'pictures/minu_charge.png'
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
    def e_field(self, r):
        return self.charge * (r - self.position) / (np.linalg.norm(r - self.position))**3

    def b_field(self, r):
        if(not self.movable):
            return 0
        return self.charge * np.cross(self.velocity, self.position - r) / (np.linalg.norm(self.position - r) ** 3)

    def get_force(self):
        e_force = self.charge * net_E(self.position, self.prop_id)
        b = net_B(self.position, self.prop_id)
        b_force = np.array([self.velocity[1] * b, -self.velocity[0] * b])
        em_force = e_force + b_force
        velocity_norm = np.linalg.norm(self.velocity)
        if(np.max(self.velocity) < 0.01 and np.linalg.norm(em_force) < FRICTION):
            self.velocity = np.array([0, 0])
            return np.array([0, 0]) 
        elif(velocity_norm < 0.01):
            return em_force
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
                    return 'collision'

            elif isinstance(p, WIN):
                if p.rect.colliderect(self.rect):
                    print("You Win")
                    return 'win'


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
    # Removed num_loops (same as putting current * n)
    # Removed direction (Say +I is counterclockwise, say -I is clockwise)
    def __init__(self, position, current, movable=True):
        super().__init__(position, movable)
        self.current = current * I * 50*200
        self.position = position 
        self.image_path = 'pictures/solenoid.png'
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.length = self.image.get_width()
        self.rect = self.image.get_rect(topleft=self.position-np.array([50,50]))
        self.movable = True
        self.has_B = True

    def draw(self, screen):
        
        screen.blit(self.image, self.rect)

    def b_field(self, point):
        """
        Calculate the magnetic field at a given point using the short solenoid approximation.

        :param point: A 3D numpy array [x, y, z].
        :return: Magnetic field vector as a numpy array [Bx, By, Bz].
        """
        # mu_0 = 4 * np.pi * 1e-7  # Magnetic constant (T·m/A)
        mu_0 = 1e-3 # Turns per unit length

        # Convert point to a numpy array and find relative position
        point = np.array(point)
        dx, dy = point - self.position
        r = np.sqrt(dx**2 + dy**2)  # Distance in 2D plane

        # Short solenoid approximation for field strength
        B_magnitude = mu_0 * self.current / 2

        # Decay field for global effect (outside solenoid)
        decay_factor = self.length / (self.length + r)  # Approximate global influence
        B_magnitude *= decay_factor

        # Assume the field is along z-axis (out of plane)
        B_field = B_magnitude
        return B_field