# Sanskrit Meter Prompts

A dataset of prompts for generating Sanskrit poetry in various meters.

## Dataset Structure

Each example contains:
- `topic`: The topic in Devanagari with English translation
- `meter`: The Sanskrit meter name in Devanagari
- `prompt`: A formatted instruction for the model

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("QuantumArjun/sanskrit-meter-prompts")

# Example usage
for example in dataset['train']:
    print(f"Topic: {example['topic']}")
    print(f"Meter: {example['meter']}")
    print(f"Prompt: {example['prompt']}")
    print()
```

## Citation

```bibtex
@misc{karanam2025sanskrit,
    title={Sanskrit Meter Prompts},
    author={Arjun Karanam},
    year={2025},
    publisher={Hugging Face}
}
```
