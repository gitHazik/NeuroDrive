import pygame
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces

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
        self.steer_speed = 3.5
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200, 50, 50)) 
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self, action):
        if action == 1: self.x -= self.steer_speed
        elif action == 2: self.x += self.steer_speed
        
        road_left = WIDTH // 2 - 280 // 2
        road_right = road_left + 280
        self.x = max(road_left, min(self.x, road_right - self.width))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def reset(self):
        self.x = float(self.start_x)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ===== OBSTACLE =====
class Obstacle:
    def __init__(self, x, y):
        self.width = 60
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        tire_centers = [(self.rect.x + 20, self.rect.y + 20), (self.rect.x + 40, self.rect.y + 20), (self.rect.x + 30, self.rect.y + 40)]
        for cx, cy in tire_centers:
            pygame.draw.circle(screen, (30, 30, 30), (cx, cy), 16)
            pygame.draw.circle(screen, (70, 70, 70), (cx, cy), 16, 2)
            pygame.draw.circle(screen, (10, 10, 10), (cx, cy), 7)

# ======= GAME ENVIRONMENT ========
class NeuroDriveEnv(gym.Env):
    def __init__(self, render_mode=None):
        super(NeuroDriveEnv, self).__init__()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(5,), dtype=np.float32)

        self.render_mode = render_mode
        if self.render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.font = pygame.font.SysFont(None, 60)
            self.small_font = pygame.font.SysFont(None, 30)

        self.car = Car()
        self.road_width = 280
        self.road_x = WIDTH // 2 - self.road_width // 2
        self.obstacle_speed = 4
        self.trees = [[random.randint(20, self.road_x - 20), random.randint(-HEIGHT, HEIGHT)] for _ in range(20)]
        self.reset()

    def get_observation(self):
        ahead_obs = sorted([obs for obs in self.obstacles if obs.rect.y < self.car.y], key=lambda o: self.car.y - o.rect.y)
        obs1 = ahead_obs[0] if len(ahead_obs) > 0 else self.obstacles[0]
        obs2 = ahead_obs[1] if len(ahead_obs) > 1 else self.obstacles[0]
        return np.array([self.car.x/WIDTH, obs1.rect.x/WIDTH, (obs1.rect.y + HEIGHT)/(HEIGHT*2), obs2.rect.x/WIDTH, (obs2.rect.y + HEIGHT)/(HEIGHT*2)], dtype=np.float32)

    def step(self, action):
        self.car.update(action)
        reward = 0.1 
        
        # Anti-Wall-Hugging
        if abs((self.car.x + 30) - (WIDTH // 2)) > 90: reward -= 0.05

        for obs in self.obstacles:
            obs.rect.y += self.obstacle_speed
            if obs.rect.y > HEIGHT:
                obs.rect.y = min(o.rect.y for o in self.obstacles) - 350
                obs.rect.x = random.randint(self.road_x + 10, self.road_x + self.road_width - 70)
                reward += 1.0
            if self.car.rect.inflate(-30, -10).colliderect(obs.rect.inflate(-10, -10)):
                self.game_over = True
                reward = -10.0

        return self.get_observation(), reward, self.game_over, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game_over = False
        self.car.reset()
        self.road_offset = 0
        self.obstacles = [Obstacle(random.randint(self.road_x+10, self.road_x+self.road_width-70), -(i*350)-300) for i in range(12)]
        return self.get_observation(), {}

    def render(self):
        self.screen.fill((40, 140, 40))
        for tree in self.trees: pygame.draw.circle(self.screen, (20, 100, 20), tree, 12)
        pygame.draw.rect(self.screen, (70, 70, 70), (self.road_x, 0, self.road_width, HEIGHT))
        self.car.draw(self.screen)
        for obs in self.obstacles: obs.draw(self.screen)
        pygame.display.flip()