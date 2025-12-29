# Deep Reinforcement Learning in "The Green Guardian"

This document explains how Deep Reinforcement Learning (DRL) is applied in this project. This is the core technical component for your Erasmus Mundus application.

## 1. The Core Concept
In this game, we are not programming the drone with "if-then" rules (e.g., "IF pollution > 50 THEN clean"). Instead, we are training a **Neural Network** to *learn* the best strategy through trial and error.

The Agent (Drone) interacts with the Environment (Grid World) in a loop:
1.  **Observe**: The agent looks at the state of the world.
2.  **Act**: The agent takes an action based on what it sees.
3.  **Reward**: The environment gives feedback (positive or negative points).
4.  **Learn**: The agent updates its brain (neural network) to maximize future rewards.

## 1.1 Who is the Agent?
This is a dual-mode project:
*   **Manual Mode (You play)**: You are the "brain". You use your human intuition to control the drone.
*   **AI Mode (The Computer plays)**: The **Deep Reinforcement Learning (DRL)** algorithm is the "brain". It controls the *same* drone in the *same* environment, but it makes decisions based on its training.

The goal of the project is to show that an **AI Agent** can learn to solve this sustainability problem just as well as (or better than) a human!

## 2. The MDP (Markov Decision Process)
We mathematically define the problem as an MDP:

### **State Space (Observation)**
What the AI "sees". It receives a 3D matrix (Tensor) of shape `(10, 10, 2)`:
-   **Channel 0**: The Object Grid (Where are the Trees, Cities, Waste, and the Agent itself?).
-   **Channel 1**: The Pollution Grid (A heat map of pollution intensity).

### **Action Space**
What the AI can "do". It has 5 discrete choices:
0.  Move Up
1.  Move Down
2.  Move Left
3.  Move Right
4.  **Interact** (Context-sensitive: Plant Tree, Clean Waste, or Install Filter)

### **Reward Function**
How we tell the AI what is "good" or "bad":
-   **+ Reward**: Planting trees, cleaning waste, lowering pollution.
-   **- Penalty**: High pollution levels, trees dying.
-   **Goal**: Maximize the cumulative "Sustainability Score".

## 3. The Algorithm: PPO (Proximal Policy Optimization)
We use **PPO**, a state-of-the-art DRL algorithm developed by OpenAI.

-   **Policy Network**: The "Actor". It takes the Grid Input and outputs probabilities for each of the 5 actions.
    -   *Example*: "I see high pollution on the left. Probability of moving Left: 80%, Right: 5%..."
-   **Value Network**: The "Critic". It estimates how good the current situation is.
    -   *Example*: "This state is dangerous; we are likely to lose soon."

PPO is chosen because it is:
-   **Stable**: It avoids drastic updates that could ruin the agent's learning.
-   **Efficient**: It learns relatively quickly for this type of problem.

## 4. The Neural Network Architecture
Since our input is a Grid (like an image), we use a **CNN (Convolutional Neural Network)** or a flattened **MLP (Multi-Layer Perceptron)**.
-   **Input Layer**: 10x10x2 Grid.
-   **Hidden Layers**: Extract features (e.g., detecting clusters of pollution or empty spots for trees).
-   **Output Layer**: 5 neurons (one for each action).

## 5. Training Process
1.  The agent starts knowing nothing (random actions).
2.  It plays thousands of games very fast.
3.  When it accidentally plants a tree and gets points, PPO strengthens the neural connections that led to that action.
4.  Over time, it "discovers" strategies:
    -   "I should clean waste before it builds up."
    -   "I need to surround cities with trees to contain pollution."
