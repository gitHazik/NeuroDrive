from stable_baselines3 import PPO
from game import NeuroDriveEnv

env =  NeuroDriveEnv()

model = PPO("MlpPolicy", env, verbose = 1)


print("Starting training..")


model.learn(total_timesteps=100000)

model.save("neurodrive_brain")

