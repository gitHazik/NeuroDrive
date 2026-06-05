import pygame
from stable_baselines3 import PPO
from game import NeuroDriveEnv

def main():
    print("Loading Environment (Visual Mode)...")
    # render_mode="human" means we WANT the window to open so we can watch
    env = NeuroDriveEnv(render_mode="human")

    print("Loading Trained AI Brain...")
    try:
        # This will automatically look for neurodrive_brain.zip!
        model = PPO.load("neurodrive_brain")
    except FileNotFoundError:
        print("Error: 'neurodrive_brain.zip' not found. Make sure you zipped the folder!")
        return

    obs, _ = env.reset()
    clock = pygame.time.Clock()
    running = True

    print("Watching the AI drive! (Close the window to stop)")

    while running:
        # Keep the window from freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Show the AI the road (obs)
        # deterministic=True means the AI uses its best learned reflexes, no random guessing
        action, _states = model.predict(obs, deterministic=True)

        # 2. The AI takes the steering wheel
        obs, reward, terminated, truncated, info = env.step(action)

        # 3. If it crashes, restart the track instantly
        if terminated or truncated:
            obs, _ = env.reset()

        # Lock the framerate so it looks perfectly smooth (120 FPS)
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()