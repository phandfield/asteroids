import os
import time
#from asteroid import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from logger import log_state, log_event
from shot import Shot



# Try to import pygame; if missing (CI/test env), provide a minimal stub
try:
    import pygame  # type: ignore
except Exception:
    from types import SimpleNamespace

    class _Display:
        def __init__(self):
            self._size = (SCREEN_WIDTH, SCREEN_HEIGHT)

        def set_mode(self, size):
            self._size = size
            return self

        def get_size(self):
            return self._size

        def fill(self, _):
            return None

        def flip(self):
            return None

    class _Event:
        @staticmethod
        def get():
            return []

    class _Time:
        @staticmethod
        def delay(ms):
            time.sleep(ms / 1000.0)

    _Display.__module__ = "pygame"
    _Event.__module__ = "pygame"
    _Time.__module__ = "pygame"

    class _Group(list):
        def add(self, *sprites):
            for sprite in sprites:
                self.append(sprite)

    pygame = SimpleNamespace(
        init=lambda: None,
        quit=lambda: None,
        display=_Display(),
        event=_Event,
        time=_Time,
        QUIT=256,
        sprite=SimpleNamespace(Group=_Group),
    )

from player import Player
from logger import log_state

def main():
    # ✅ Create updatable/drawable groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()


    # ✅ Set Player class containers BEFORE instantiation
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)

    # ✅ Instantiate player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Headless display check
    if "DISPLAY" not in os.environ:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        screen = None

    clock = pygame.time.Clock()
    dt = 0

    log_state()  # initial state

    try:
        while True:
            dt = clock.tick(60) / 1000  # seconds per frame

            # Update all objects
            for obj in updatable:
                obj.update(dt)

            # Check for player–asteroid collisions
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    print("Game over!")
                    sys.exit()

            # Check for shot–asteroid collisions
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Draw all objects
            if screen is not None:
                screen.fill("black")
                for obj in drawable:
                    obj.draw(screen)
                pygame.display.flip()

            log_state()  # log state each frame

    except KeyboardInterrupt:
        return
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
