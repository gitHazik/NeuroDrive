import pygame
from game import NeuroDriveEnv 

def main():
    # Initialize our RL Environment
    env = NeuroDriveEnv()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # In the future, this is where you ask your AI model: action = model.predict(observation)
        keys = pygame.key.get_pressed()
        action = 0  # Default: Drive Straight

        if keys[pygame.K_a]:
            action = 1 
        elif keys[pygame.K_d]:
            action = 2  

        # 3. Advance the environment by one step
        game_over, score = env.step(action)

        # 4. Draw the environment
        env.render()

        # 5. Handle crashes
        if game_over:
            # If playing manually, wait for the 'R' key to restart
            # if keys[pygame.K_r]:
            #     env.reset()
            
             env.reset() 

        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()