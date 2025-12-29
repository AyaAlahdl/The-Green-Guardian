import pygame
import time
from env.guardian_env import GuardianEnv
from game.renderer import GameRenderer

def play():
    env = GuardianEnv(render_mode="human")
    renderer = GameRenderer(grid_size=env.grid_size)
    
    current_level = 1
    max_levels = 3
    
    while current_level <= max_levels:
        env.set_level(current_level)
        obs, info = env.reset()
        
        # Show Level Start Screen
        renderer.render(env, score=0, message=f"STAGE {current_level} START!")
        pygame.time.wait(2000)
        
        renderer.render(env)
        
        running = True
        level_complete = False
        clock = pygame.time.Clock()
        
        print(f"Starting Level {current_level}...")
        
        while running:
            action = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    current_level = 99 # Exit game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = 0
                    elif event.key == pygame.K_DOWN:
                        action = 1
                    elif event.key == pygame.K_LEFT:
                        action = 2
                    elif event.key == pygame.K_RIGHT:
                        action = 3
                    elif event.key == pygame.K_SPACE:
                        action = 4
                    elif event.key == pygame.K_x:
                        action = 5
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        current_level = 99 # Exit game
                        
            if action is not None:
                obs, reward, terminated, truncated, info = env.step(action)
                score = info.get("score", 0)
                renderer.render(env, score=score)
                print(f"Reward: {reward:.2f}, Score: {score:.2f}")
                
                if terminated or truncated:
                    if terminated: # Lost
                        msg = "Game Over! Ecosystem Collapsed."
                        print(msg)
                        renderer.render(env, score=score, message=msg)
                        pygame.time.wait(3000)
                        running = False # Restart level or quit? Let's just restart level
                        # Actually, let's just break and let the user restart the script for now, or retry level
                        # Simple: Retry Level
                        
                    elif truncated: # Won (Survived max steps with positive score)
                        if score > 0:
                            msg = "Level Complete! Ecosystem Sustained."
                            print(msg)
                            renderer.render(env, score=score, message=msg)
                            pygame.time.wait(3000)
                            level_complete = True
                            running = False
                        else:
                            msg = "Failed! Score too low."
                            print(msg)
                            renderer.render(env, score=score, message=msg)
                            pygame.time.wait(3000)
                            running = False
                    
            clock.tick(30)
            
        if level_complete:
            current_level += 1
        else:
            # Retry same level?
            # For simplicity, let's ask to retry or quit
            # If user quit (current_level=99), loop ends
            pass
            
    if current_level == max_levels + 1:
        renderer.render(env, score=0, message="YOU WON THE GAME!")
        pygame.time.wait(5000)
        
    renderer.close()
    env.close()

if __name__ == "__main__":
    play()
