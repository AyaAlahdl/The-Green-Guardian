# AI Training Results Explained

This document explains the output you see when training the AI.

## 1. What does "Model saved at 50000 steps" mean?
It means the AI has practiced the game for **50,000 turns**.
-   Every 10,000 steps, we save a "checkpoint" (a snapshot of its brain) to the `models/PPO/` folder.
-   This allows you to stop training and resume later, or to see how the AI improves over time.

## 2. Key Metrics Explained
When you see the training log, here is what the numbers mean:

| Metric | Meaning | Good Trend |
| :--- | :--- | :--- |
| **ep_rew_mean** | **Average Reward per Game**. This is the most important number. It shows how many points the AI gets on average. | **INCREASING** (Higher is better) |
| **ep_len_mean** | **Average Game Length**. How long the AI survives. | **INCREASING** (Closer to 200 is better) |
| **fps** | **Frames Per Second**. How fast the training is running. | Stable (Higher is faster) |
| **value_loss** | **Prediction Error**. How wrong the AI was about its score prediction. | **DECREASING** (Lower is better) |

## 3. Your Results
In your latest training run:
-   **Start**: `ep_rew_mean` was around **191**.
-   **End**: `ep_rew_mean` reached **249**.

**Conclusion**: The AI is learning! It is getting significantly better at the game (gaining ~58 more points on average per game).

## 4. How to Use the Trained Model
Now that training is complete, you can watch this "smart" AI play:
1.  Run `run_game.bat`
2.  Select Option **2. Watch AI Agent**
3.  The script will automatically load the latest model (`50000.zip`) and show you the result.
