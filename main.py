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

        self.x = float(self.start_x)
        self.y = float(self.start_y)

        # Steering speed
        self.steer_speed = 5

        # Keep the car image
        self.image = pygame.image.load(
            "assets/Audi.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (self.width, self.height)
        )

        self.rect = self.image.get_rect(
            topleft=(self.x, self.y)
        )
    
    def update(self):
        keys = pygame.key.get_pressed()

        # Steering ONLY (Acceleration removed)
        if keys[pygame.K_d]:
            self.x += self.steer_speed
        if keys[pygame.K_a]:
            self.x -= self.steer_speed
        
        # Keep the car on the road
        road_left = WIDTH // 2 - 280 // 2
        road_right = road_left + 280

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

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ===== OBSTACLE (CUSTOM DRAWN TIRES) =====
class Obstacle:
    def __init__(self, x, y):
        self.width = 60
        self.height = 60
        
        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

    def draw(self, screen):
        # Coordinates for a cluster of 3 tires
        tire_centers = [
            (self.rect.x + 20, self.rect.y + 20),
            (self.rect.x + 40, self.rect.y + 20),
            (self.rect.x + 30, self.rect.y + 40)
        ]

        for cx, cy in tire_centers:
            # 1. Outer black/dark grey tire edge
            pygame.draw.circle(screen, (30, 30, 30), (cx, cy), 16)
            
            # 2. Inner dark grey rim highlight
            pygame.draw.circle(screen, (70, 70, 70), (cx, cy), 16, 2)
            
            # 3. Deep black center hole
            pygame.draw.circle(screen, (10, 10, 10), (cx, cy), 7)


# =======GAME========
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

        self.road_width = 280
        self.road_x = WIDTH // 2 - self.road_width // 2

        # Set a constant, fun speed for the world to move automatically
        self.obstacle_speed = 8

        self.start_time = pygame.time.get_ticks()
        self.road_offset = 0

        # Trees
        self.trees = []
        for i in range(20):
            self.trees.append([
                random.randint(20, self.road_x - 20),
                random.randint(-HEIGHT, HEIGHT)
            ])

            self.trees.append([
                random.randint(
                    self.road_x + self.road_width + 20,
                    WIDTH - 20
                ),
                random.randint(-HEIGHT, HEIGHT)
            ])

        # Create obstacles (Images removed, using custom drawn class)
        self.obstacles = []
        self.create_obstacles()

    def create_obstacles(self):
        self.obstacles.clear()

        spacing = 350

        for i in range(12):
            x = random.randint(
                self.road_x + 10,
                self.road_x + self.road_width - 70
            )

            y = -(i * spacing) - 300

            self.obstacles.append(
                Obstacle(x, y)
            )

    def restart(self):
        self.game_over = False
        self.car.reset()
        self.start_time = pygame.time.get_ticks()
        self.create_obstacles()

    def update(self):
        # Stop everything immediately if the game is over
        if self.game_over:
            return

        # Update environment (Automatic scrolling)
        self.road_offset += self.obstacle_speed

        if self.road_offset >= 80:
            self.road_offset = 0

        for tree in self.trees:
            tree[1] += self.obstacle_speed

            if tree[1] > HEIGHT + 20:
                tree[1] = -20

        # Update player car (Steering)
        self.car.update()

        current_time = pygame.time.get_ticks()

        # Shrink the car hitbox slightly for fair collisions
        car_hitbox = self.car.rect.inflate(-30, -10)

        for obstacle in self.obstacles:
            obstacle.rect.y += self.obstacle_speed

            # Recycle obstacle to top
            if obstacle.rect.y > HEIGHT:
                highest_y = min(
                    obs.rect.y for obs in self.obstacles
                )

                obstacle.rect.y = highest_y - 350

                obstacle.rect.x = random.randint(
                    self.road_x + 10,
                    self.road_x + self.road_width - 70
                )

            # Check collisions after start protection
            if current_time - self.start_time > 2000:
                # Shrink the tire stack hitbox slightly for extra fairness
                obs_hitbox = obstacle.rect.inflate(-10, -10)
                
                if car_hitbox.colliderect(obs_hitbox):
                    self.game_over = True

    def draw(self):
        # Grass
        self.screen.fill((40, 140, 40))

        # Trees
        for tree in self.trees:
            pygame.draw.circle(
                self.screen,
                (20, 100, 20),
                tree,
                12
            )

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

        # Center lane
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

        # Side lane markers
        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (
                    self.road_x + 40,
                    y + self.road_offset,
                    6,
                    30
                )
            )

            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (
                    self.road_x + self.road_width - 46,
                    y + self.road_offset,
                    6,
                    30
                )
            )

        # Road borders
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (self.road_x, 0),
            (self.road_x, HEIGHT),
            4
        )

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (self.road_x + self.road_width, 0),
            (self.road_x + self.road_width, HEIGHT),
            4
        )

        # Draw Obstacles (Tire barriers)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Draw Car
        self.car.draw(self.screen)

        current_time = pygame.time.get_ticks()

        # Start protection text
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

        # Game Over Screen
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