from env.guardian_env import GuardianEnv
from gymnasium.utils.env_checker import check_env

def main():
    env = GuardianEnv()
    print("Checking environment...")
    check_env(env)
    print("Environment check passed!")

    # Test a random episode
    obs, _ = env.reset()
    print(f"Initial Observation Shape: {obs.shape}")
    
    done = False
    step = 0
    while not done:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        step += 1
        
    print(f"Random episode finished in {step} steps.")

if __name__ == "__main__":
    main()
