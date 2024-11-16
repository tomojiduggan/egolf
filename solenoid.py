import pygame
import numpy as np

class Solenoid:
    def __init__(self, num_loops, current, direction, position,image_path):
        """
        Initialize the Solenoid with parameters.

        :param num_loops: Number of loops in the solenoid (integer).
        :param current: Magnitude of the current in amperes (float).
        :param direction: Direction of the current as a unit vector (numpy array of length 3).
        :param position: Initial position of the solenoid as a tuple (x, y).
        :param image_path: Path to the image of the solenoid.
        """
        self.num_loops = num_loops
        self.current = current
        self.direction = np.array(direction) / np.linalg.norm(direction)  # Normalize the direction vector
        self.position = list(position)  # Convert to list for mutability
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=self.position)
        self.length = self.rect.width  # Assuming the solenoid is a rectangle
        self.is_dragging = False

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

    def magnetic_field(self, point):
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


    def __repr__(self):
        return (f"Solenoid(Num Loops: {self.num_loops}, Current: {self.current} A, "
                f"Position: {self.position}, Direction: {self.direction})")

class POINT_CHARGE:
    def __init__(self, position, charge, movable, velocity=None):
        """
        Initialize the point charge.

        :param position: Initial position as a numpy array [x, y].
        :param charge: Magnitude of the charge.
        :param movable: Boolean, whether the charge can move.
        :param velocity: Initial velocity as a numpy array [vx, vy] (optional).
        """
        self.position = np.array(position, dtype=float)
        self.charge = charge
        self.movable = movable
        self.velocity = np.array(velocity if velocity is not None else [0.0, 0.0], dtype=float)

    def update(self, magnetic_field, delta_t):
        """
        Update the position of the charge based on the magnetic field.

        :param magnetic_field: Magnetic field vector (numpy array [Bx, By, Bz]).
        :param delta_t: Time step for the update (float).
        """
        if not self.movable:
            return  # Static charges don't move

        # Assume a uniform magnetic field
        B = magnetic_field
        v = np.append(self.velocity, 0.0)  # Extend velocity to 3D (add zero for z)
        F = self.charge * np.cross(v, B)  # Lorentz force
        print(F)

        # Acceleration (F = ma, assume mass = 1 for simplicity)
        acceleration = F[:2]  # Only x, y components
        self.velocity += acceleration * delta_t
        self.position += self.velocity * delta_t

    def draw(self, screen, color, radius):
        """Draw the point charge."""
        pygame.draw.circle(screen, color, self.position.astype(int), radius)


# for testing
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Charge Motion in Magnetic Field")

# Clock for controlling frame rate
clock = pygame.time.Clock()
DELTA_T = 0.05  # Time step for simulation (in seconds)

# Create the solenoid and the moving charge
solenoid_image_path = "solenoid.png"  # Path to your solenoid image
solenoid = Solenoid(num_loops=500, current=50.0, direction=[0, 0, 1], position=(300, 300),image_path=solenoid_image_path)
moving_charge = POINT_CHARGE(position=[500, 400], charge=10.0, movable=True, velocity=[10.0, 0.0])

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle solenoid dragging
        solenoid.handle_event(event)

    # Calculate the magnetic field at the charge's position
    position_3d = np.append(moving_charge.position, 0.0)  # Extend to 3D
    B_field = solenoid.magnetic_field(position_3d)

    # Update the charge's motion
    moving_charge.update(B_field, DELTA_T)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the solenoid
    solenoid.draw(screen)

    # Draw the moving charge
    moving_charge.draw(screen, color=(255, 0, 0), radius=10)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()