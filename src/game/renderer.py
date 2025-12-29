import pygame
import numpy as np
import time

class GameRenderer:
    def __init__(self, grid_size=10, cell_size=60):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.width = grid_size * cell_size
        self.height = grid_size * cell_size + 120 # Increased UI space
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Green Guardian")
        self.font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.small_font = pygame.font.SysFont("Verdana", 14, bold=True)
        self.title_font = pygame.font.SysFont("Verdana", 30, bold=True)
        
        # Premium Dark Theme Colors
        self.COLOR_BG = (20, 24, 30) # Dark Blue-Grey
        self.COLOR_GRID = (40, 45, 55)
        self.COLOR_UI_BG = (25, 30, 40)
        self.COLOR_UI_BORDER = (60, 65, 75)
        
        # Object Colors
        self.COLOR_TREE = (46, 204, 113) # Emerald Green
        self.COLOR_CITY = (155, 89, 182) # Amethyst Purple
        self.COLOR_WASTE = (230, 126, 34) # Carrot Orange
        self.COLOR_AGENT = (52, 152, 219) # Peter River Blue
        self.COLOR_EVIL = (231, 76, 60) # Alizarin Red (More vibrant)
        self.COLOR_POLLUTION = (192, 57, 43) 
        self.COLOR_TEXT = (236, 240, 241) # Clouds White
        
    def render(self, env, score=0, message=None):
        self.screen.fill(self.COLOR_BG)
        
        # Draw Grid
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.COLOR_GRID, (x, 0), (x, self.grid_size * self.cell_size))
        for y in range(0, self.grid_size * self.cell_size + 1, self.cell_size):
            pygame.draw.line(self.screen, self.COLOR_GRID, (0, y), (self.width, y))
            
        # Draw Objects
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = c * self.cell_size
                y = r * self.cell_size
                center = (x + self.cell_size//2, y + self.cell_size//2)
                
                obj = env.grid_objects[r, c]
                pollution = env.grid_pollution[r, c]
                
                if obj == env.TREE:
                    self._draw_tree(center)
                elif obj == env.CITY:
                    self._draw_city(x, y)
                elif obj == env.WASTE:
                    self._draw_waste(center)
                
                # Draw Pollution Overlay (Dynamic Pulse)
                if pollution > 0.1:
                    self._draw_pollution(x, y, pollution)
                    
        # Draw Agent (Drone)
        ar, ac = env.agent_pos
        ax = ac * self.cell_size
        ay = ar * self.cell_size
        self._draw_drone(ax, ay)
        
        # Draw Evil Agent
        if env.evil_agent_active:
            er, ec = env.evil_agent_pos
            ex = ec * self.cell_size
            ey = er * self.cell_size
            is_stunned = env.evil_agent_stunned_timer > 0
            self._draw_evil_agent(ex, ey, is_stunned)
        
        # Draw UI Panel
        self._draw_ui(env, score)
        
        # Draw Message Overlay
        if message:
            self._draw_message(message)
        
        pygame.display.flip()
        
    def _draw_tree(self, center):
        x, y = center
        # Trunk
        pygame.draw.rect(self.screen, (139, 69, 19), (x - 4, y + 10, 8, 15))
        # Leaves (Layered circles)
        pygame.draw.circle(self.screen, (39, 174, 96), (x, y - 5), 18)
        pygame.draw.circle(self.screen, self.COLOR_TREE, (x - 10, y + 5), 12)
        pygame.draw.circle(self.screen, self.COLOR_TREE, (x + 10, y + 5), 12)
        
    def _draw_city(self, x, y):
        # Skyline silhouette
        color = self.COLOR_CITY
        margin = 10
        w = self.cell_size - 2*margin
        h = self.cell_size - 2*margin
        base_y = y + self.cell_size - margin
        
        # Building 1
        pygame.draw.rect(self.screen, color, (x + margin, base_y - 30, 10, 30))
        # Building 2 (Tall)
        pygame.draw.rect(self.screen, (142, 68, 173), (x + margin + 12, base_y - 40, 15, 40))
        # Building 3
        pygame.draw.rect(self.screen, color, (x + margin + 29, base_y - 25, 10, 25))
        
        # Windows (Dots)
        pygame.draw.circle(self.screen, (255, 255, 200), (x + margin + 19, base_y - 30), 2)
        pygame.draw.circle(self.screen, (255, 255, 200), (x + margin + 19, base_y - 20), 2)

    def _draw_waste(self, center):
        x, y = center
        # Trash bags
        pygame.draw.circle(self.screen, (100, 100, 100), (x - 5, y + 5), 8)
        pygame.draw.circle(self.screen, (80, 80, 80), (x + 5, y + 5), 8)
        pygame.draw.circle(self.screen, self.COLOR_WASTE, (x, y - 5), 9)
        # Stench lines
        pygame.draw.line(self.screen, (200, 200, 200), (x, y-15), (x, y-20), 1)
        pygame.draw.line(self.screen, (200, 200, 200), (x-5, y-12), (x-8, y-18), 1)

    def _draw_pollution(self, x, y, pollution):
        s = pygame.Surface((self.cell_size, self.cell_size))
        # Make pollution pulse slightly with time
        pulse = (np.sin(time.time() * 5) + 1) * 20 
        alpha = int(min(200, pollution * 180 + pulse))
        s.set_alpha(alpha)
        s.fill(self.COLOR_POLLUTION)
        self.screen.blit(s, (x, y))

    def _draw_drone(self, x, y):
        center = (x + self.cell_size//2, y + self.cell_size//2)
        # Body
        pygame.draw.circle(self.screen, self.COLOR_AGENT, center, 10)
        # Arms
        pygame.draw.line(self.screen, (200, 200, 200), (center[0]-15, center[1]-15), (center[0]+15, center[1]+15), 3)
        pygame.draw.line(self.screen, (200, 200, 200), (center[0]-15, center[1]+15), (center[0]+15, center[1]-15), 3)
        # Rotors (Spinning visual)
        offset = int((time.time() * 10) % 4)
        rotors = [(center[0]-15, center[1]-15), (center[0]+15, center[1]+15), (center[0]-15, center[1]+15), (center[0]+15, center[1]-15)]
        for rx, ry in rotors:
             pygame.draw.circle(self.screen, (100, 200, 255), (rx, ry), 6 + offset, 1)

    def _draw_evil_agent(self, x, y, is_stunned):
        center = (x + self.cell_size//2, y + self.cell_size//2)
        color = (100, 100, 100) if is_stunned else self.COLOR_EVIL
        
        # Spiky Shape
        points = [
            (center[0], center[1] - 20),
            (center[0] + 15, center[1] - 5),
            (center[0] + 20, center[1] + 10),
            (center[0], center[1] + 20),
            (center[0] - 20, center[1] + 10),
            (center[0] - 15, center[1] - 5)
        ]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, (0, 0, 0), points, 2)
        
        # Eyes
        if not is_stunned:
            pygame.draw.circle(self.screen, (255, 255, 0), (center[0]-7, center[1]), 3)
            pygame.draw.circle(self.screen, (255, 255, 0), (center[0]+7, center[1]), 3)
        else:
            # Zzz
            stun_text = self.font.render("Zzz", True, (255, 255, 255))
            self.screen.blit(stun_text, (x + 35, y))

    def _draw_ui(self, env, score):
        ui_rect = pygame.Rect(0, self.grid_size * self.cell_size, self.width, 120)
        pygame.draw.rect(self.screen, self.COLOR_UI_BG, ui_rect)
        pygame.draw.line(self.screen, self.COLOR_UI_BORDER, (0, self.grid_size * self.cell_size), (self.width, self.grid_size * self.cell_size), 3)
        
        # Helper for shadowed text
        def draw_text(text, x, y, color=self.COLOR_TEXT, font=self.font):
            shadow = font.render(text, True, (0, 0, 0))
            surface = font.render(text, True, color)
            self.screen.blit(shadow, (x+1, y+1))
            self.screen.blit(surface, (x, y))

        base_y = self.grid_size * self.cell_size + 15
        
        # Column 1: Stats
        trees = np.sum(env.grid_objects == env.TREE)
        draw_text(f"STAGE: {env.level}", 30, base_y, (255, 215, 0), self.title_font)
        draw_text(f"Trees: {trees}", 30, base_y + 40, self.COLOR_TREE)
        draw_text(f"Step: {env.current_step}/{env.max_steps}", 30, base_y + 70, (200, 200, 200), self.small_font)
        
        # Column 2: Score (Center)
        score_color = self.COLOR_TREE if score > 0 else self.COLOR_POLLUTION
        draw_text(f"SCORE", 250, base_y, (200, 200, 200), self.small_font)
        draw_text(f"{score:.1f}", 250, base_y + 20, score_color, self.title_font)
        
        # Column 3: Abilities
        bar_x = 400
        bar_y = base_y + 30
        bar_width = 180
        bar_height = 25
        
        draw_text("WATER CANNON", bar_x, base_y, (52, 152, 219), self.small_font)
        
        # Bar Background
        pygame.draw.rect(self.screen, (40, 40, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # Bar Fill
        if env.water_ready:
            fill_width = bar_width
            color = (52, 152, 219) # Bright Blue
            # Pulse effect for ready bar
            pulse = int((np.sin(time.time() * 10) + 1) * 20)
            color = (52, min(255, 152 + pulse), 219)
            text = "READY! (X)"
        else:
            pct = min(1.0, env.waste_cleaned_count / max(1, env.waste_needed_for_charge))
            fill_width = int(bar_width * pct)
            color = (41, 128, 185) # Darker Blue
            text = f"{env.waste_cleaned_count}/{env.waste_needed_for_charge}"
            
        if fill_width > 0:
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, bar_height), border_radius=5)
            
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        
        # Bar Text
        text_surf = self.small_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(bar_x + bar_width//2, bar_y + bar_height//2))
        self.screen.blit(text_surf, text_rect)

    def _draw_message(self, message):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        color = self.COLOR_POLLUTION if "Over" in message or "Failed" in message else self.COLOR_TREE
        text_msg = self.title_font.render(message, True, color)
        text_rect = text_msg.get_rect(center=(self.width/2, self.height/2))
        
        # Glow effect
        for offset in range(2, 0, -1):
            glow = self.title_font.render(message, True, (0, 0, 0))
            self.screen.blit(glow, (text_rect.x + offset, text_rect.y + offset))
        
        self.screen.blit(text_msg, text_rect)
        
        sub_msg = self.font.render("Press any key to continue", True, (200, 200, 200))
        sub_rect = sub_msg.get_rect(center=(self.width/2, self.height/2 + 50))
        self.screen.blit(sub_msg, sub_rect)

    def close(self):
        pygame.quit()
