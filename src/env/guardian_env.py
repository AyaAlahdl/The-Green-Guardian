import gymnasium as gym
from gymnasium import spaces
import numpy as np

class GuardianEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    The Guardian Drone must manage a grid world ecosystem.
    """
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 4}

    def __init__(self, grid_size=10, render_mode=None):
        super(GuardianEnv, self).__init__()
        self.grid_size = grid_size
        self.render_mode = render_mode
        
        # Define constants
        self.EMPTY = 0
        self.TREE = 1
        self.CITY = 2
        self.WASTE = 3
        self.AGENT = 4
        self.EVIL_AGENT = 5
        
        # Action space: Up, Down, Left, Right, Interact, Water Attack
        self.action_space = spaces.Discrete(6)
        
        # Observation space: Grid with channels
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.grid_size, self.grid_size, 2), dtype=np.float32
        )
        
        self.agent_pos = [0, 0]
        self.evil_agent_pos = [0, 0]
        self.max_steps = 200
        self.current_step = 0
        self.sustainability_score = 0
        
        # Level System
        self.level = 1
        
        # Water Ability State
        self.waste_cleaned_count = 0
        self.waste_needed_for_charge = 3
        self.water_ready = False
        self.evil_agent_stunned_timer = 0
        
    def set_level(self, level):
        self.level = level
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Reset Ability State
        self.waste_cleaned_count = 0
        self.waste_needed_for_charge = self.np_random.integers(3, 6)
        self.water_ready = False
        self.evil_agent_stunned_timer = 0
        
        # Initialize grid
        self.grid_objects = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.grid_pollution = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        
        # Place Agent
        self.agent_pos = [self.grid_size // 2, self.grid_size // 2]
        
        # Level Configuration
        if self.level == 1:
            # Stage 1: Restoration (Easy, No Evil Agent)
            num_cities = 2
            num_waste = 4
            self.evil_agent_active = False
        elif self.level == 2:
            # Stage 2: Defense (Medium, Distracted Evil Agent)
            num_cities = 3
            num_waste = 5
            self.evil_agent_active = True
        else:
            # Stage 3: Crisis (Hard, Aggressive)
            num_cities = 4
            num_waste = 7
            self.evil_agent_active = True
            
        # Place Evil Agent (Random corner)
        corners = [[0,0], [0, self.grid_size-1], [self.grid_size-1, 0], [self.grid_size-1, self.grid_size-1]]
        self.evil_agent_pos = list(self.np_random.choice(corners))
        
        # Place initial Cities
        for _ in range(num_cities):
            pos = self._get_random_empty_pos()
            if pos is not None:
                self.grid_objects[pos[0], pos[1]] = self.CITY
                
        # Place initial Waste
        for _ in range(num_waste):
            pos = self._get_random_empty_pos()
            if pos is not None:
                self.grid_objects[pos[0], pos[1]] = self.WASTE
                
        self.current_step = 0
        self.sustainability_score = 0
        
        return self._get_obs(), {"water_ready": self.water_ready, "stunned": self.evil_agent_stunned_timer > 0}
    
    def step(self, action):
        self.current_step += 1
        reward = 0
        terminated = False
        truncated = False
        
        # Move Agent
        if action < 4:
            new_pos = self.agent_pos.copy()
            if action == 0: # Up
                new_pos[0] = max(0, new_pos[0] - 1)
            elif action == 1: # Down
                new_pos[0] = min(self.grid_size - 1, new_pos[0] + 1)
            elif action == 2: # Left
                new_pos[1] = max(0, new_pos[1] - 1)
            elif action == 3: # Right
                new_pos[1] = min(self.grid_size - 1, new_pos[1] + 1)
            
            self.agent_pos = new_pos
            
        # Interact
        elif action == 4:
            r, c = self.agent_pos
            obj = self.grid_objects[r, c]
            
            if obj == self.WASTE:
                self.grid_objects[r, c] = self.EMPTY
                reward += 5
                # Charge Water Ability
                if not self.water_ready:
                    self.waste_cleaned_count += 1
                    if self.waste_cleaned_count >= self.waste_needed_for_charge:
                        self.water_ready = True
                        reward += 2 # Bonus for charging
                        
            elif obj == self.EMPTY:
                self.grid_objects[r, c] = self.TREE
                reward += 2
            elif obj == self.CITY:
                if self.grid_pollution[r, c] > 0.5:
                    self.grid_pollution[r, c] = 0
                    reward += 3
                    
        # Water Attack
        elif action == 5:
            if self.water_ready:
                # Check distance to Evil Agent
                dist = np.abs(self.agent_pos[0] - self.evil_agent_pos[0]) + np.abs(self.agent_pos[1] - self.evil_agent_pos[1])
                if dist <= 3: # Range of 3 cells
                    self.evil_agent_stunned_timer = 5 # Stun for 5 turns
                    self.water_ready = False
                    self.waste_cleaned_count = 0
                    self.waste_needed_for_charge = self.np_random.integers(3, 6) # Reset requirement
                    reward += 10 # Big reward for stunning
                else:
                    reward -= 1 # Wasted shot
        
        # Move Evil Agent
        if self.evil_agent_active:
            self._move_evil_agent()
        
        # Environmental Dynamics
        self._update_environment()
        
        # Calculate Step Reward based on state
        num_trees = np.sum(self.grid_objects == self.TREE)
        total_pollution = np.sum(self.grid_pollution)
        
        # Reward is the change in sustainability or just the current state quality
        step_reward = (num_trees * 0.1) - (total_pollution * 0.05)
        reward += step_reward
        
        # Update Sustainability Score
        self.sustainability_score += reward
        
        # Check termination
        if self.sustainability_score < -10: # Loose condition
            terminated = True
            reward -= 50
        elif self.current_step >= self.max_steps:
            truncated = True
            if self.sustainability_score > 0:
                reward += 50
            
        info = {
            "score": self.sustainability_score,
            "water_ready": self.water_ready,
            "waste_count": self.waste_cleaned_count,
            "waste_needed": self.waste_needed_for_charge,
            "stunned": self.evil_agent_stunned_timer > 0,
            "level": self.level
        }
            
        return self._get_obs(), reward, terminated, truncated, info
    
    def _move_evil_agent(self):
        # Check Stun
        if self.evil_agent_stunned_timer > 0:
            self.evil_agent_stunned_timer -= 1
            return # Skip turn
            
        # Distraction Chance based on level
        distraction_chance = 0.3 if self.level == 2 else 0.1 # Harder in level 3
        
        if self.np_random.random() < distraction_chance:
            # Wander randomly
            move = self.np_random.integers(0, 4)
            er, ec = self.evil_agent_pos
            if move == 0: er = max(0, er - 1)
            elif move == 1: er = min(self.grid_size - 1, er + 1)
            elif move == 2: ec = max(0, ec - 1)
            elif move == 3: ec = min(self.grid_size - 1, ec + 1)
            self.evil_agent_pos = [er, ec]
            return

        # Otherwise, hunt nearest tree
        trees = np.argwhere(self.grid_objects == self.TREE)
        if len(trees) > 0:
            # Calculate distances
            distances = np.sum(np.abs(trees - self.evil_agent_pos), axis=1)
            nearest_tree_idx = np.argmin(distances)
            target = trees[nearest_tree_idx]
            
            # Move towards target
            er, ec = self.evil_agent_pos
            tr, tc = target
            
            if er < tr: er += 1
            elif er > tr: er -= 1
            
            if ec < tc: ec += 1
            elif ec > tc: ec -= 1
            
            self.evil_agent_pos = [er, ec]
            
            # Destroy tree if reached
            if self.grid_objects[er, ec] == self.TREE:
                self.grid_objects[er, ec] = self.WASTE # Turn tree into waste!
        else:
            # Wander randomly if no trees
            move = self.np_random.integers(0, 4)
            er, ec = self.evil_agent_pos
            if move == 0: er = max(0, er - 1)
            elif move == 1: er = min(self.grid_size - 1, er + 1)
            elif move == 2: ec = max(0, ec - 1)
            elif move == 3: ec = min(self.grid_size - 1, ec + 1)
            self.evil_agent_pos = [er, ec]

    def _get_obs(self):
        obs_objects = self.grid_objects.copy()
        obs_objects[self.agent_pos[0], self.agent_pos[1]] = self.AGENT
        if self.evil_agent_active:
            obs_objects[self.evil_agent_pos[0], self.evil_agent_pos[1]] = self.EVIL_AGENT
        
        obs = np.stack([obs_objects, self.grid_pollution], axis=-1).astype(np.float32)
        return obs
    
    def _update_environment(self):
        # Pollution Rate based on level
        pollution_rate = 0.1 if self.level < 3 else 0.15
        spread_rate = 0.05 if self.level < 3 else 0.08
        
        # Cities generate pollution
        cities = np.argwhere(self.grid_objects == self.CITY)
        for r, c in cities:
            self.grid_pollution[r, c] = min(1.0, self.grid_pollution[r, c] + pollution_rate)
            
            # Spread pollution to neighbors
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    self.grid_pollution[nr, nc] = min(1.0, self.grid_pollution[nr, nc] + spread_rate)
        
        # Trees absorb pollution but die if too high
        trees = np.argwhere(self.grid_objects == self.TREE)
        for r, c in trees:
            if self.grid_pollution[r, c] > 0.7:
                # Tree dies
                self.grid_objects[r, c] = self.EMPTY
            else:
                # Absorb pollution
                self.grid_pollution[r, c] = max(0.0, self.grid_pollution[r, c] - 0.15)
                
        # Random Waste Spawning
        spawn_rate = 0.05 if self.level < 3 else 0.08
        if self.np_random.random() < spawn_rate:
            pos = self._get_random_empty_pos()
            if pos is not None:
                self.grid_objects[pos[0], pos[1]] = self.WASTE

    def _get_random_empty_pos(self):
        empty_indices = np.argwhere(self.grid_objects == self.EMPTY)
        if len(empty_indices) > 0:
            idx = self.np_random.integers(0, len(empty_indices))
            return empty_indices[idx]
        return None

    def render(self):
        if self.render_mode == "human":
            pass
