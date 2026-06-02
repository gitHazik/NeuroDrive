import pygame

class Car:
    def __init__(self):
        self.x = 400
        self.y = 300

        self.width = 40
        self.height = 20

        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.x, self.y, self.width, self.height)
        )