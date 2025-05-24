# Sanskrit-meter-RL

A Gym-style environment for training language models to generate metrically-correct Sanskrit poetry. The project provides:

* **Meter Verification**: Wrapper around the `chandas` library to verify Sanskrit meters
* **Rich Prompt Dataset**: 2000+ prompts combining various topics and meters
* **RL Environment**: OpenAI Gym environment for training LLMs
* **Reward System**: Sophisticated reward calculation with anti-gaming mechanisms

## Features

### 1. Prompt Generation
- **Topics**: 280+ carefully curated topics across categories:
  - Traditional Rasas (emotional essences)
  - Seasons and natural phenomena
  - Philosophical concepts
  - Epic and heroic themes
  - Cultural elements
  - Abstract concepts

- **Meters**: Support for major Sanskrit meters:
  - अनुष्टुप् (Anushtup)
  - मन्दाक्रान्ता (Mandakranta)
  - शार्दूलविक्रीडितम् (Shardulavikridita)
  - वसन्ततिलका (Vasantatilaka)
  - प्रियदर्शिनी (Priyadarshini)
  - त्रिष्टुप् (Trishtup)
  - जगती (Jagati)

### 2. RL Environment
- Gym-compatible interface
- Integration with Hugging Face's Transformers
- Support for various LLM architectures

### 3. Reward System
Comprehensive reward calculation with anti-gaming mechanisms:

- **Meter Accuracy**: Basic verification of metrical correctness
- **Anti-Gaming Mechanisms** (TODO):
  1. Syllable Pattern Check: Prevent repetitive patterns
  2. Semantic Relevance: Ensure topic adherence
  3. Self-Reference Detection: Avoid critic-baiting
  4. Plagiarism Check: Prevent copying known verses

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

### 1. Generate Prompts
```python
from src.data.generate_dataset import main as generate_prompts
generate_prompts()  # Creates prompts.jsonl
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