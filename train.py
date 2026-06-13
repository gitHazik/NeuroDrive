from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import dummy_vec_env , VecNormalize
from game import NeuroDriveEnv




def main ():

    print("Loading NeuroDrive Environment")
    env = dummy_vec_env([lambda: NeuroDriveEnv(render_mode=None)])
    env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

    print("Building Neural Network Brain with optimized architecture...")
    # Using a slightly larger hidden layer structure (128x128) for better decision making
    policy_kwargs = dict(net_arch=dict(pi=[128, 128], vf=[128, 128]))
    
    model = PPO(
        "MlpPolicy", 
        env, 
        policy_kwargs=policy_kwargs, 
        verbose=1,
        learning_rate=0.0003
    )


    print("Starting Training! Check the console for progress...")
    # Training for 200,000 steps to ensure convergence
    model.learn(total_timesteps=200000)

    print("Training complete! Saving brain to 'neurodrive_brain.zip'...")
    model.save("neurodrive_brain")
    
    # Save the normalization stats as well, otherwise the agent will be confused during inference!
    env.save("vec_normalize.pkl")
    print("Normalization stats saved to 'vec_normalize.pkl'.")

if __name__ == "__main__":
    main()
