import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from env.guardian_env import GuardianEnv

def train():
    # Create directories
    models_dir = "models/PPO"
    log_dir = "logs"
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Create Environment
    # We can use a vectorized environment for faster training
    env = make_vec_env(lambda: GuardianEnv(), n_envs=4)
    
    # Initialize Agent
    # MlpPolicy is good for vector observations. 
    # Since our observation is a small grid (10x10x2), MlpPolicy works well by flattening it.
    model = PPO("MlpPolicy", env, verbose=1)
    
    TIMESTEPS = 10000
    iters = 0
    
    print("Starting training...")
    while True:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
        print(f"Model saved at {TIMESTEPS*iters} steps")
        
        # For demonstration, we stop after 5 iterations (50k steps)
        if iters >= 5:
            break
            
    print("Training complete!")

if __name__ == "__main__":
    train()
