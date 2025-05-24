"""
A Gym environment for training language models to generate Sanskrit poetry in specific meters.
"""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from .reward import calculate_reward

class SanskritMeterEnv(gym.Env):
    """Environment for generating Sanskrit poetry in specific meters."""
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, render_mode: Optional[str] = None, model_name: str = "google/gemma-2b"):
        super().__init__()
        
        # Load Gemma tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Load the prompts
        data_path = Path(__file__).parent / "data" / "prompts.jsonl"
        self.prompts = []
        with data_path.open("r", encoding="utf-8") as f:
            for line in f:
                self.prompts.append(json.loads(line))
        
        # Action space is Gemma's vocabulary
        self.action_space = spaces.Discrete(self.tokenizer.vocab_size)
        
        # Define observation space based on model's config
        self.max_seq_len = self.model.config.max_position_embeddings
        self.observation_space = spaces.Dict({
            "prompt_ids": spaces.Box(low=0, high=self.tokenizer.vocab_size, shape=(self.max_seq_len,), dtype=np.int32),
            "generated_ids": spaces.Box(low=0, high=self.tokenizer.vocab_size, shape=(self.max_seq_len,), dtype=np.int32),
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
        
        # Create prompt text
        prompt_text = f"Write a Sanskrit verse in {self.current_prompt['meter']} meter about {self.current_prompt['topic']}:\n"
        
        # Encode prompt
        encoded = self.tokenizer(prompt_text, return_tensors="np", padding="max_length", max_length=self.max_seq_len)
        
        obs = {
            "prompt_ids": encoded["input_ids"][0],
            "generated_ids": np.zeros(self.max_seq_len, dtype=np.int32),
            "attention_mask": encoded["attention_mask"][0]
        }
        
        return obs, {}
        
    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        # Add token to generated sequence
        self.current_generated.append(action)
        
        # Create full sequence (prompt + generated)
        generated_array = np.array(self.current_generated)
        padded_generated = np.pad(generated_array, 
                                 (0, self.max_seq_len - len(generated_array)),
                                 mode='constant')
        
        # Update observation
        obs = {
            "prompt_ids": self.observation_space["prompt_ids"].low.copy(),  # Keep original prompt
            "generated_ids": padded_generated,
            "attention_mask": np.ones(self.max_seq_len, dtype=np.int32)  # All tokens visible
        }
        
        # Convert generated tokens to text
        generated_text = self.tokenizer.decode(self.current_generated)
        
        # Calculate reward using the meter from the prompt
        reward_info = calculate_reward(generated_text, self.current_prompt["meter"])
        reward = reward_info["reward"]
        
        # Episode is done if we hit max length or generate EOS token
        done = (len(self.current_generated) >= self.max_seq_len or
                action == self.tokenizer.eos_token_id)
        
        return obs, reward, done, False, {}
    
    def render(self):
        if self.render_mode == "human":
            print(f"Prompt Topic: {self.current_prompt['topic']}")
            print(f"Target Meter: {self.current_prompt['meter']}")
            print("Generated Text:")
            if self.current_generated:
                text = self.tokenizer.decode(self.current_generated)
                print(text)
            else:
                print("<no text generated yet>")
