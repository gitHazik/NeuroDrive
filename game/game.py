import pygame

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((20,20,20))

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()