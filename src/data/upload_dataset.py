"""
Upload the prompts dataset to HuggingFace's datasets hub.
"""
import json
from pathlib import Path
from datasets import Dataset
from huggingface_hub import HfApi

def load_jsonl(file_path: str) -> list:
    """Load data from a JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def main():
    # Load the prompts
    prompts_path = Path(__file__).parent / "prompts.jsonl"
    data = load_jsonl(prompts_path)
    
    # Convert to Dataset
    dataset = Dataset.from_list(data)
    
    # Push to hub
    dataset.push_to_hub(
        "QuantumArjun/sanskrit-meter-prompts",
        private=False,
        token=None  # Will use the token from the Hugging Face CLI
    )
    
    # Update the README
    readme_path = Path(__file__).parent / "dataset_readme.md"
    api = HfApi()
    api.upload_file(
        path_or_fileobj=str(readme_path),
        path_in_repo="README.md",
        repo_id="QuantumArjun/sanskrit-meter-prompts",
        repo_type="dataset"
    )

if __name__ == "__main__":
    main()
