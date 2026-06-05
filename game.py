import pygame 
import random





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

    def update(self):
        keys = pygame.key.get_pressed()


        if keys[pygame.K_d]:
            self.x += self.steer_speed
        if keys[pygame.K_a]:
            self.x -= self.steer_speed


        road_left = WIDTH // 2 - 280 // 2 
        road_right  = road_left + 280


        self.x = max(
            road_left,
            min(
                self.x,
                road_right - self.width
            )
        )


        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        

        self.rect.x = float(self.x)
        self.rect.y = float(self.y)

    def draw(self, screen):
        screen.blit(self.car_image, self.rect)







class Obstacles:
    
    def __init__(self,x,y):
        
        self.width = 60
        self.height = 60


        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )
    def draw(self,screen):
        tire_centers = [
            (self.rect.x + 20 , self.rect.y + 20)
            (self.rect.x + 40 , self.rect.y + 20)
            (self.rect.x + 30 , self.rect.y + 20)
        ]
        
        for cx , cy in tire_centers:
            pygame.draw.circle(screen, (30,30,30), (cx,cy), 16)

            pygame.draw.circle(screen, (70,70,70), (cx,cy), 16, 2)
            pygame.draw.circle(screen, (10,10,10), (cx,cy), 7)
    

class Game:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NeuroDrive")

        self.clock = pygame.time.Clock()

        self.car  = Car()

        self.running = True
        self.game_over = False 

        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 30)

        self.score = 0
        self.road.x = WIDTH // 2 - self.road_width // 2

        self.obstacle_speed = 4

        self.start_time = pygame.time.get_ticks()
        self.road_offset = 0

        #Trees

        self.trees = []
        for i in range(20):
            self.trees.append([
                rando
            ])