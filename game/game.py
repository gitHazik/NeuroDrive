import pygame
from .car import Car


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("NeuroDrive")

        self.clock = pygame.time.Clock()
        self.car = Car()

        self.running = True

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.car.update()

            self.screen.fill((0, 0, 0))
            self.car.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()