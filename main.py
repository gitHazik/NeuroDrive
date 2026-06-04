import pygame
import random

# ===== SETTINGS =====
WIDTH = 800
HEIGHT = 600

# ===== CAR =====
class Car:
    def __init__(self):
        self.width = 60
        self.height = 85

        self.start_x = WIDTH // 2 - self.width // 2
        self.start_y = HEIGHT - 140

        self.x = self.start_x
        self.y = self.start_y

        self.speed = 8
        self.image = pygame.image.load("assets/Audi.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.width, self.height)
        )

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self):
        keys = pygame.key.get_pressed()

        # WASD controls
        if keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_d]:
            self.x += self.speed

        road_left = WIDTH // 2 - 280 // 2
        road_right = road_left + 280
        
        self.x = max(
            road_left,
            min(self.x, road_right - self.width)
        )

        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Obstacles:
    def __init__(self,x,y,image):
        
        self.image = image 
        

# ===== GAME =====
class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NeuroDrive")

        self.clock = pygame.time.Clock()

        self.car = Car()

        self.running = True
        self.game_over = False

        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 30)

        # Road
        self.road_width = 280
        self.road_x = WIDTH // 2 - self.road_width // 2

        # Obstacle speed
        self.obstacle_speed = 5

        # 2-second protection timer
        self.start_time = pygame.time.get_ticks()

        # Obstacles
        self.obstacles = []
        self.create_obstacles()
        self.road_offset = 0

    def create_obstacles(self):
          self.obstacles.clear()

          obstacle_count = 12
          spacing = 350

          for i in range(obstacle_count):

              x = random.randint(
                  self.road_x,
                  self.road_x + self.road_width - 60
              )

              y = -(i * spacing) - 300

              self.obstacles.append(
                  pygame.Rect(x, y, 60, 85)
              )


    def restart(self):
        self.game_over = False

        self.car.reset()

        self.start_time = pygame.time.get_ticks()

        self.create_obstacles()

    def update(self):
     
     self.road_offset += self.obstacle_speed

     if self.road_offset >= 80:
         self.road_offset = 0

     if self.game_over:
         return

     self.car.update()

     current_time = pygame.time.get_ticks()

     for obstacle in self.obstacles:

         obstacle.y += self.obstacle_speed

         # Recycle obstacle
         if obstacle.y > HEIGHT:

             highest_y = min(obs.y for obs in self.obstacles)

             obstacle.y = highest_y - 350

             obstacle.x = random.randint(
                 self.road_x,
                 self.road_x + self.road_width - obstacle.width
             )

         # No collision during first 2 seconds
         if current_time - self.start_time > 2000:

             if self.car.rect.colliderect(obstacle):
                 self.game_over = True

    def draw(self):

        # Grass
        self.screen.fill((40, 140, 40))

        # Road
        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            (
                self.road_x,
                0,
                self.road_width,
                HEIGHT
            )
        )

        # Lane markings
        for y in range(-80, HEIGHT, 80):

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (
                    WIDTH // 2 - 5,
                    y + self.road_offset,
                    10,
                    40
                )
            )

        # Obstacles
        for obstacle in self.obstacles:

            pygame.draw.rect(
                self.screen,
                (220, 50, 50),
                obstacle
            )
        pygame.draw.line(
            self.screen,
            (255,255,255),
            (self.road_x, 0),
            (self.road_x, HEIGHT ),
            4
        )
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (self.road_x + self.road_width, 0),
            (self.road_x + self.road_width, HEIGHT),
            4
        )

        # Car
        self.car.draw(self.screen)

        # Spawn protection message
        current_time = pygame.time.get_ticks()

        if current_time - self.start_time < 2000:

            text = self.small_font.render(
                "START PROTECTION",
                True,
                (255, 255, 0)
            )

            self.screen.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, 20)
            )



        
      
        # Game Over
        if self.game_over:

            game_over_text = self.font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

            restart_text = self.small_font.render(
                "Press R to Restart",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                game_over_text,
                (
                    WIDTH // 2 - game_over_text.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )

            self.screen.blit(
                restart_text,
                (
                    WIDTH // 2 - restart_text.get_width() // 2,
                    HEIGHT // 2 + 30
                )
            )

    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.restart()

            self.update()

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


# ===== START =====
if __name__ == "__main__":
    game = Game()
    game.run()