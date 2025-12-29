# The Green Guardian: AI for Sustainability

## Overview
**The Green Guardian** is a Deep Reinforcement Learning (DRL) game designed to demonstrate the potential of AI in solving complex sustainability challenges. This project combines engaging gameplay with a meaningful narrative about environmental stewardship.

## Game Concept
The player (or AI agent) controls a **Guardian Drone** in a dynamic grid-world environment representing a fragile ecosystem.

### Core Mechanics
- **The Grid**: A 10x10 map containing **Forests**, **Cities**, **Waste**, and **Pollution**.
- **The Agent**: The Guardian Drone can move, **Plant Trees**, **Clean Waste**, and **Install Filters** on cities.
- **The Evil Agent**: A rogue bot that hunts down and destroys trees. It is imperfect and sometimes gets **distracted** (wanders randomly).
- **Dynamics**:
    - Cities generate economic value but also produce **Pollution** and **Waste**.
    - **Pollution** spreads and destroys nearby Forests.
    - **Forests** absorb Pollution and generate "Sustainability Score".
    - **Waste** accumulates and reduces the Sustainability Score.
- **Goal**: Maintain a positive **Sustainability Score** for 200 steps to advance to the next stage.
    - **Stage 1**: Restoration (Easy, No Evil Agent).
    - **Stage 2**: Defense (Medium, Distracted Evil Agent).
    - **Stage 3**: Crisis (Hard, Aggressive Evil Agent).
    - **Win**: Complete all 3 stages.
    - **Lose**: Sustainability Score drops below -10 (Ecosystem Collapse).

## Quick Start
Double-click `run_game.bat` to launch the menu.

Or run from command line:
- **Play Game**: `python src/play.py`
- **Watch AI**: `python src/watch.py`
- **Train Agent**: `python src/train.py`

## Controls (Manual Mode)
- **Arrow Keys**: Move
- **Space**: Interact (Plant Tree / Clean Waste / Filter City)
- **X**: Water Attack (Stun Evil Agent when ready)
- **Esc**: Quit

## Technology Stack
- **Language**: Python 3.11
- **Environment**: Gymnasium (Custom Environment)
- **RL Library**: Stable Baselines3 (PPO)
- **Visualization**: Pygame

## Project Structure
- `src/env/`: Custom Gymnasium environment logic.
- `src/agent/`: DRL agent training scripts.
- `src/game/`: Pygame-based rendering.
- `models/`: Saved trained models.
