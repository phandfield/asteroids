import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH,
        )
