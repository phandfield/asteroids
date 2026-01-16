import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Always destroy this asteroid first
        self.kill()

        # If it's already the smallest, just return
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
         # Log the split event
        log_event("asteroid_split")

        # Compute new radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Pick a random angle between 20 and 50 degrees
        angle = random.uniform(20, 50)

        # First asteroid velocity (rotate original vector by +angle)
        vel1 = self.velocity.rotate(angle) * 1.2

        # Second asteroid velocity (rotate original vector by -angle)
        vel2 = self.velocity.rotate(-angle) * 1.2

        # Create two new Asteroid objects
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Assign velocities
        a1.velocity = vel1
        a2.velocity = vel2
