# Sanskrit‑meter‑RL

Utilities for
* **meter verification** (wrapping the `chandas` library),
* **prompt dataset** generation (`prompts.jsonl`),
to support RLHF / RLAIF research on Sanskrit poetry.

## Quick‑start
```bash
pip install -e .[dev]
pytest          # run unit tests
python -m src.generate_dataset    # regenerate prompt list