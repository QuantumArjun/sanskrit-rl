"""
A Gym environment for training language models to generate Sanskrit poetry in specific meters.
"""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import json

class SanskritMeterEnv(gym.Env):
    """Environment for generating Sanskrit poetry in specific meters."""
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, render_mode: Optional[str] = None):
        super().__init__()
        
        # Load the prompts
        data_path = Path(__file__).parent / "data" / "prompts.jsonl"
        self.prompts = []
        with data_path.open("r", encoding="utf-8") as f:
            for line in f:
                self.prompts.append(json.loads(line))
        
        # TODO: Update vocabulary size based on actual tokenizer
        # Current size is just a placeholder
        self.action_space = spaces.Discrete(1000)
        
        # Define observation space
        # This will include the encoded prompt and current generated text
        # Assuming max sequence length of 512
        self.max_seq_len = 512
        self.observation_space = spaces.Dict({
            "prompt_ids": spaces.Box(low=0, high=1000, shape=(self.max_seq_len,), dtype=np.int32),
            "generated_ids": spaces.Box(low=0, high=1000, shape=(self.max_seq_len,), dtype=np.int32),
            "attention_mask": spaces.Box(low=0, high=1, shape=(self.max_seq_len,), dtype=np.int32)
        })
        
        self.render_mode = render_mode
        self.current_prompt = None
        self.current_generated = []
        
    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        super().reset(seed=seed)
        
        # Select a random prompt
        self.current_prompt = self.np_random.choice(self.prompts)
        self.current_generated = []
        
        # TODO: Integrate with actual tokenizer in reset
        # Need to:
        # 1. Encode prompt text using tokenizer
        # 2. Create proper attention mask for the prompt
        # 3. Initialize empty generated sequence
        obs = {
            "prompt_ids": np.zeros(self.max_seq_len, dtype=np.int32),
            "generated_ids": np.zeros(self.max_seq_len, dtype=np.int32),
            "attention_mask": np.zeros(self.max_seq_len, dtype=np.int32)
        }
        
        return obs, {}
        
    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        # Add token to generated sequence
        self.current_generated.append(action)
        
        # TODO: Update observation with new token
        # Need to:
        # 1. Keep prompt encoding from reset
        # 2. Update generated_ids with new token
        # 3. Update attention mask for the new sequence
        obs = {
            "prompt_ids": np.zeros(self.max_seq_len, dtype=np.int32),
            "generated_ids": np.zeros(self.max_seq_len, dtype=np.int32),
            "attention_mask": np.zeros(self.max_seq_len, dtype=np.int32)
        }
        
        # TODO: Implement proper reward calculation
        # Need to:
        # 1. Convert generated tokens to text
        # 2. Use chandas library to verify meter
        # 3. Calculate reward based on meter correctness
        reward = 0.0
        
        # Check if episode is done
        done = len(self.current_generated) >= self.max_seq_len
        
        return obs, reward, done, False, {}
    
    def render(self):
        if self.render_mode == "human":
            # TODO: Implement proper text generation and rendering
            # Need to:
            # 1. Decode token IDs back to text using tokenizer
            # 2. Format the text properly with Sanskrit characters
            # 3. Display both the prompt and generated text in a readable format
            print(f"Prompt: {self.current_prompt}")
            print(f"Generated: {self.current_generated}")
