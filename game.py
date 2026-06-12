import gymnasium as gym
from gymnasium import spaces
import numpy as np
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
        self.steer_speed = 3.5

        # --- THE BULLETPROOF FALLBACK ---
        try:
            self.image = pygame.image.load("assets/Audi.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except FileNotFoundError:
            # If Colab/Drive can't find the image, just use a red box!
            print("Warning: Audi.png not found. Using a red box instead.")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 50, 50)) # Red color
        # --------------------------------

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self, action):
        # AI ACTIONS: 0 = Straight, 1 = Left, 2 = Right
        if action == 1:
            self.x -= self.steer_speed
        elif action == 2:
            self.x += self.steer_speed
        
        # Keep the car on the road
        road_left = WIDTH // 2 - 280 // 2
        road_right = road_left + 280
        self.x = max(road_left, min(self.x, road_right - self.width))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
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
        tire_centers = [
            (self.rect.x + 20, self.rect.y + 20),
            (self.rect.x + 40, self.rect.y + 20),
            (self.rect.x + 30, self.rect.y + 40)
        ]
        for cx, cy in tire_centers:
            pygame.draw.circle(screen, (30, 30, 30), (cx, cy), 16)
            pygame.draw.circle(screen, (70, 70, 70), (cx, cy), 16, 2)
            pygame.draw.circle(screen, (10, 10, 10), (cx, cy), 7)


# ======= GAME ENVIRONMENT ========
class NeuroDriveEnv(gym.Env):
    def __init__(self, render_mode="human"):
        super(NeuroDriveEnv, self).__init__()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(3,), dtype=np.float32)
        # --------------------------------------------------------------------------------

        self.render_mode = render_mode
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NeuroDrive - RL Environment")
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 30)
        
        self.car = Car()
        self.road_width = 280
        self.road_x = WIDTH // 2 - self.road_width // 2
        self.obstacle_speed = 4

        # Initialize state variables
        self.reset()

        # Trees (Visual only, AI won't care about these)
        self.trees = []
        for i in range(20):
            self.trees.append([random.randint(20, self.road_x - 20), random.randint(-HEIGHT, HEIGHT)])
            self.trees.append([random.randint(self.road_x + self.road_width + 20, WIDTH - 20), random.randint(-HEIGHT, HEIGHT)])

    def create_obstacles(self):
        self.obstacles.clear()
        spacing = 350
        for i in range(12):
            x = random.randint(self.road_x + 10, self.road_x + self.road_width - 70)
            y = -(i * spacing) - 300
            self.obstacles.append(Obstacle(x, y))
    def get_observation(self):
        """Calculates what the AI sees right now."""
        # Find the obstacle closest to the car (but ahead of it)
        closest_obs = None
        min_dist = float('inf')
        
        for obs in self.obstacles:
            if obs.rect.y < self.car.y: # Only look at obstacles ahead
                dist = self.car.y - obs.rect.y
                if dist < min_dist:
                    min_dist = dist
                    closest_obs = obs
                    
        # If no obstacle is ahead (rare), just look at the first one
        if closest_obs is None:
            if len(self.obstacles) > 0:
                closest_obs = self.obstacles[0]
            else:
                # Fallback if list is empty
                return np.zeros(3, dtype=np.float32)

        # Normalize the numbers between 0 and 1 so the Neural Network learns easily
        obs = np.array([
            self.car.x / WIDTH,
            closest_obs.rect.x / WIDTH,
            (closest_obs.rect.y + HEIGHT) / (HEIGHT * 2) # Handle negative Y values
        ], dtype=np.float32)
        
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game_over = False
        self.car.reset()
        self.start_time = pygame.time.get_ticks()
        self.score = 0
        self.last_score_time = self.start_time
        self.road_offset = 0
        self.obstacles = []
        self.create_obstacles()
        return self.get_observation(), {}

    def step(self, action):
        """The AI's main loop."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 2000: # Wait until start protection ends
            if current_time - self.last_score_time >= 1000:
                self.score += 1
                self.last_score_time = current_time

        # Update environment
        self.road_offset += self.obstacle_speed
        if self.road_offset >= 80:
            self.road_offset = 0

        for tree in self.trees:
            tree[1] += self.obstacle_speed
            if tree[1] > HEIGHT + 20:
                tree[1] = -20

        # Pass AI action to car
        self.car.update(action)

        # Base Reward for surviving this frame
        reward = 0.1  

        # Check Collisions
        car_hitbox = self.car.rect.inflate(-30, -10)
        for obstacle in self.obstacles:
            obstacle.rect.y += self.obstacle_speed

            # Recycle obstacles and give a big reward!
            if obstacle.rect.y > HEIGHT:
                highest_y = min(obs.rect.y for obs in self.obstacles)
                obstacle.rect.y = highest_y - 350
                obstacle.rect.x = random.randint(self.road_x + 10, self.road_x + self.road_width - 70)
                reward += 1.0 # Bonus reward for passing an obstacle!

            if current_time - self.start_time > 2000:
                obs_hitbox = obstacle.rect.inflate(-10, -10)
                if car_hitbox.colliderect(obs_hitbox):
                    self.game_over = True
                    reward = -10.0 # Massive penalty for crashing

        # Get the new observation after moving
        observation = self.get_observation()

        # Draw the frame if we are watching
        if self.render_mode == "human":
            self.render()

        # ====== GYMNASIUM REQUIRES THESE 5 EXACT VALUES ======
        return observation, reward, self.game_over, False, {}

    def render(self):
        """Draws the current frame to the screen."""
        self.screen.fill((40, 140, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for tree in self.trees:
            pygame.draw.circle(self.screen, (20, 100, 20), tree, 12)

        pygame.draw.rect(self.screen, (70, 70, 70), (self.road_x, 0, self.road_width, HEIGHT))

        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(self.screen, (255, 255, 255), (WIDTH // 2 - 5, y + self.road_offset, 10, 40))
            pygame.draw.rect(self.screen, (255, 255, 0), (self.road_x + 40, y + self.road_offset, 6, 30))
            pygame.draw.rect(self.screen, (255, 255, 0), (self.road_x + self.road_width - 46, y + self.road_offset, 6, 30))

        pygame.draw.line(self.screen, (255, 255, 255), (self.road_x, 0), (self.road_x, HEIGHT), 4)
        pygame.draw.line(self.screen, (255, 255, 255), (self.road_x + self.road_width, 0), (self.road_x + self.road_width, HEIGHT), 4)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.car.draw(self.screen)

        current_time = pygame.time.get_ticks()
        
        shadow_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(shadow_text, (22, 22)) 
        self.screen.blit(score_text, (20, 20))

        if current_time - self.start_time < 2000:
            text = self.small_font.render("START PROTECTION", True, (255, 255, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

        if self.game_over:
            game_over_text = self.font.render("CRASHED", True, (255, 50, 50))
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))

        pygame.display.flip()ew