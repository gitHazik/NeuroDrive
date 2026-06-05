from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from game import NeuroDriveEnv

def main():
    print("Loading NeuroDrive Environment...")
    env = NeuroDriveEnv(render_mode="human")

    # --- THE MAGIC CHECKER ---
    # This will scan your game and print a very clear error if anything is missing!
    print("Checking environment validity...")
    check_env(env)
    print("Environment is perfect! \n")
    # -------------------------

    print("Building Neural Network Brain...")
    model = PPO("MlpPolicy", env, verbose=1)

    print("Starting Training! Watch the window...")
    model.learn(total_timesteps=50000)

    print("Training complete! Saving brain to 'neurodrive_brain.zip'...")
    model.save("neurodrive_brain")

if __name__ == "__main__":
    main()