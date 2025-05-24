"""
Prime-RL wrapper for the Sanskrit Meter environment.
"""
from typing import Dict, Any, Optional

import gymnasium as gym
import numpy as np
from transformers import AutoTokenizer

from .env import SanskritMeterEnv

class PrimeSanskritMeterEnv(gym.Wrapper):
    """
    A Prime-RL compatible wrapper for the Sanskrit Meter environment.
    This wrapper handles:
    1. Token-based action space
    2. Prime-RL compatible observation space
    3. Proper reward scaling
    4. Episode management
    """
    
    def __init__(
        self,
        model_name: str = "google/gemma-2b",
        max_length: int = 256,
        **kwargs
    ):
        env = SanskritMeterEnv(model_name=model_name, max_length=max_length)
        super().__init__(env)
        
        # Prime-RL expects these attributes
        self.current_step = 0
        self.max_episode_steps = max_length
        self.return_scale = 1.0  # Scale rewards to be roughly in [-1, 1]
        
        # Keep track of episode stats
        self._episode_rewards = []
        self._episode_lengths = []
    
    def reset(
        self, 
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ):
        """Reset the environment."""
        obs, info = super().reset(seed=seed, options=options)
        self.current_step = 0
        return obs, info
    
    def step(self, action):
        """Take a step in the environment."""
        obs, reward, terminated, truncated, info = super().step(action)
        
        self.current_step += 1
        
        # Scale reward to be roughly in [-1, 1]
        scaled_reward = reward * self.return_scale
        
        # Add episode stats to info
        if terminated or truncated:
            self._episode_rewards.append(reward)
            self._episode_lengths.append(self.current_step)
            info.update({
                "episode": {
                    "r": np.mean(self._episode_rewards[-100:]),
                    "l": np.mean(self._episode_lengths[-100:]),
                }
            })
        
        return obs, scaled_reward, terminated, truncated, info
    
    @property
    def unwrapped(self):
        """Get the base environment."""
        return self.env.unwrapped
    
    def get_normalized_score(self, reward: float) -> float:
        """
        Convert raw reward to normalized score (expected to be between 0 and 1).
        In our case, perfect meter = 1.0, completely wrong = 0.0
        """
        return max(0.0, min(1.0, (reward + 1.0) / 2.0))
