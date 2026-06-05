# --- train.py ---
from stable_baselines3 import PPO
from game import NeuroDriveEnv

def main():
    print("Loading NeuroDrive Environment (Headless Mode)...")
    # render_mode=None means no window will open. It trains 10x faster!
    env = NeuroDriveEnv(render_mode=None)

    print("Building Neural Network Brain...")
    model = PPO("MlpPolicy", env, verbose=1)

    print("Starting Training! Check the console for progress...")
    # Let's train for 150,000 steps. This should take about 5-10 minutes.
    model.learn(total_timesteps=150000)

    print("Training complete! Saving brain to 'neurodrive_brain.zip'...")
    model.save("neurodrive_brain")

if __name__ == "__main__":
    main()