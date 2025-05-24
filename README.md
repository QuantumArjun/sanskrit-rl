# Sanskrit-meter-RL

A Gym-style environment for training language models to generate metrically-correct Sanskrit poetry. The project provides:

* **Meter Verification**: Wrapper around the `chandas` library to verify Sanskrit meters
* **Rich Prompt Dataset**: 2000+ prompts combining various topics and meters (available on [HuggingFace](https://huggingface.co/datasets/QuantumArjun/sanskrit-meter-prompts))
* **RL Environment**: OpenAI Gym environment for training LLMs
* **Reward System**: Sophisticated reward calculation with anti-gaming mechanisms

## Installation

```bash
# Install package and development dependencies
pip install -e .[dev]

# Run tests
pytest

# Generate prompt dataset
python -m src.data.generate_dataset
```

## Usage

### 1. Get Prompts
You can either generate prompts locally or use the pre-generated dataset from HuggingFace:

```python
# Option 1: Generate locally
from src.data.generate_dataset import main as generate_prompts
generate_prompts()  # Creates prompts.jsonl

# Option 2: Use HuggingFace dataset
from datasets import load_dataset
dataset = load_dataset("QuantumArjun/sanskrit-meter-prompts")
```

### 2. Use the Environment
```python
from src.env import SanskritMeterEnv

env = SanskritMeterEnv()
obs = env.reset()

for _ in range(max_steps):
    action = model.predict(obs)  # Your model's prediction
    obs, reward, done, info = env.step(action)
    if done:
        break
```

## TODOs

### 1. Reward Hacking Prevention
Implement the following in `src/reward.py`:

- [ ] `check_syllable_patterns()`: Detect and penalize repetitive syllables
  - Split text into syllables
  - Identify unnatural repetitions
  - Calculate penalty scores

- [ ] `check_semantic_relevance()`: Ensure meaningful topic adherence
  - Implement keyword density checking
  - Add LLM-based semantic similarity
  - Verify logical coherence

- [ ] `check_self_references()`: Prevent critic-baiting
  - Identify self-referential patterns
  - Strip/mask problematic phrases
  - Apply appropriate penalties

- [ ] `check_plagiarism()`: Detect verse copying
  - Implement n-gram comparison
  - Add sequence alignment
  - Set proper similarity thresholds

### 2. Environment Enhancements
- [ ] Add support for more meters
- [ ] Implement temperature-based sampling
- [ ] Add logging and visualization tools

### 3. Dataset Improvements
- [ ] Add more topic categories
- [ ] Include example verses for each meter
- [ ] Add difficulty levels for prompts

## Contributing

Contributions are welcome! Please check the TODOs section for areas that need work.

## License

MIT License