import pygame 




WIDTH = 800
HEIGHT = 600



class Car:
    def __init__(self):
        self.width = 60
        self.height = 85

        self.start_x = WIDTH // 2 - self.width // 2
        self.start_y = HEIGHT -140

        self.x = float(self.start_x)
        self.y = float(self.start_y)

        self.steer_speed = 4

        self.car_image = pygame.image.load(
            "assets/Audi.png"
        ).convert_alpha()

        self.car_image = pygame.transform.scale(
            self.car_image,
        (self.width, self.height)
        )

        self.rect = self.car_image.get_rect(
            topleft = (self.x, self.y)
        )

    def update():
        