from constants import PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED
import pygame
from shot import Shot
from circleshape import CircleShape  # if Player inherits CircleShape

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=20)
        self.rotation = 0

    def rotate(self, dt, direction=1):
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, forward=True):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        speed = PLAYER_SPEED * dt * (1 if forward else -1)
        self.position += rotated_vector * speed

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt, direction=-1)  # left
        if keys[pygame.K_d]:
            self.rotate(dt, direction=1)   # right
        if keys[pygame.K_w]:
            self.move(dt, forward=True)    # forward
        if keys[pygame.K_s]:
            self.move(dt, forward=False)   # backward
        if keys[pygame.K_SPACE]:
            self.shoot()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)

        direction = pygame.Vector2(0, 1)
        direction = direction.rotate(self.rotation)

        shot.velocity = direction * PLAYER_SHOOT_SPEED