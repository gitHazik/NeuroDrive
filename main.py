import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from game import NeuroDriveEnv

def main():
    # 1. Initialize the environment with render_mode="human"
    # We wrap it in DummyVecEnv so the model can read it correctly
    env = DummyVecEnv([lambda: NeuroDriveEnv(render_mode="human")])
    
    # 2. Load the normalization stats (CRITICAL to match training)
    try:
        env = VecNormalize.load("vec_normalize.pkl", env)
        env.training = False 
        env.norm_reward = False
    except FileNotFoundError:
        print("Warning: 'vec_normalize.pkl' not found. AI may behave erratically.")

    # 3. Extract the underlying NeuroDriveEnv object so we can trigger render()
    game_env = env.envs[0]

    print("Loading Trained AI Brain...")
    model = PPO.load("neurodrive_brain")

    obs = env.reset()
    clock = pygame.time.Clock()
    running = True

    print("Watching the AI drive! (Close the window to stop)")

    while running:
        # Check for window exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 4. AI Action Prediction
        action, _ = model.predict(obs, deterministic=True)

        # 5. Step the environment
        obs, _, dones, _ = env.step(action)

        # 6. FORCE RENDER: This bypasses the wrapper to draw the car and obstacles
        game_env.render()

        if dones:
            obs = env.reset()

        clock.tick(60)

    env.close()
    pygame.quit()

if __name__ == "__main__":
    main()