import time
import pygame
from stable_baselines3 import PPO
from env.guardian_env import GuardianEnv
from game.renderer import GameRenderer

def watch():
    # Load the latest model
    # For now, we assume a specific path or the user updates it
    model_path = "models/PPO/50000.zip" 
    
    try:
        model = PPO.load(model_path)
    except FileNotFoundError:
        print(f"Model not found at {model_path}. Please train the agent first using src/train.py")
        return

    env = GuardianEnv(render_mode="human")
    renderer = GameRenderer(grid_size=env.grid_size)
    
    obs, _ = env.reset()
    renderer.render(env)
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        action, _states = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        renderer.render(env)
        
        if terminated or truncated:
            print("Episode Finished!")
            obs, _ = env.reset()
            time.sleep(1) # Pause before restart
            
        time.sleep(0.1) # Slow down for viewing
        clock.tick(30)
        
    renderer.close()
    env.close()

if __name__ == "__main__":
    watch()
