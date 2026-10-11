# Fine-tuning Qwen 0.5B

A lightweight, configuration-driven project for preparing data and fine-tuning Qwen 0.5B models on accessible hardware.

The repository brings together data collection, preprocessing, training configuration, and evaluation in one workflow. It is designed for developers and researchers who want to experiment with smaller language models without relying on large, expensive infrastructure.

## Why this repository exists

Fine-tuning language models often involves complex setup, large hardware requirements, and many framework-specific configuration details. This project exists to make that process easier to understand and reproduce for smaller models.

The project was inspired by [Soup](https://github.com/razor-ai/soup), a GitHub trending project that uses YAML-based instructions to simplify model training and fine-tuning workflows. This repository explores a similar idea for Qwen 0.5B: keep the workflow modular, make configuration visible, and support practical experimentation on limited hardware.

The focus is not only on training a model, but also on documenting the surrounding workflow:

- Preparing and cleaning data
- Organizing training configurations
- Testing different hardware backends
- Evaluating fine-tuned model behavior
- Understanding the trade-offs of local fine-tuning

## Project workflow

```text
Collect data → Preprocess data → Configure training → Fine-tune Qwen 0.5B → Evaluate results
```

## Repository layout

```text
.
├── data/           # Training and evaluation data
├── evaluvation/    # Evaluation scripts and outputs
├── preprocessing/  # Dataset preparation and preprocessing
├── scrapper/       # Data collection and scraping utilities
├── training/       # Training scripts and YAML configuration files
├── requirements.txt
└── git.md          # Git and virtual-environment notes
```

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/RathnamS089/fintuneqwen0.5B.git
cd fintuneqwen0.5B
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell
```

### 3. Install the dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The current requirements include utilities for data collection and processing such as `requests`, `beautifulsoup4`, `lxml`, and `tqdm`. Training dependencies may need to be installed separately depending on your operating system, Python version, PyTorch version, and accelerator.

### 4. Prepare a dataset

Use the utilities in `scrapper/` to collect data and the scripts in `preprocessing/` to transform it into the format expected by the training workflow.

Before training, check that your dataset:

- Uses the expected format
- Does not contain private or sensitive information
- Has consistent input and output fields
- Contains clean, relevant examples
- Is split appropriately for training and evaluation

### 5. Configure a training run

Training settings are intended to be managed through YAML files in `training/`. A configuration can contain values such as:

```yaml
model_name: Qwen/Qwen2.5-0.5B
train_file: data/train.jsonl
output_dir: outputs/qwen-0.5b-finetuned
num_train_epochs: 3
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
learning_rate: 0.00002
max_seq_length: 512
```

Use the actual model identifier, dataset paths, and supported field names required by the training script in this repository. The example above is intended as a starting point rather than a guaranteed drop-in configuration.

### 6. Start training

Inspect the available files in `training/` and run the training entry point associated with your YAML configuration:

```bash
find training -maxdepth 2 -type f
python training/<training_script>.py --config training/<config>.yaml
```

Replace the placeholders with the relevant script and configuration file names in your checkout.

### 7. Evaluate the model

After training, use the scripts in `evaluvation/` to compare the fine-tuned model with the base model:

```bash
python evaluvation/<evaluation_script>.py \
  --model_path outputs/qwen-0.5b-finetuned
```

Evaluation should include both automated metrics, where available, and sample generations reviewed for relevance, consistency, and unwanted behavior.

## Hardware considerations

The project is intended for smaller-scale local experimentation. Memory usage depends on the model, sequence length, batch size, optimizer, precision, and training backend.

For lower-memory systems, consider:

- Reducing the sequence length
- Using a small per-device batch size
- Increasing gradient accumulation instead of batch size
- Training on a smaller dataset during initial tests
- Saving checkpoints regularly
- Using a compatible low-precision or parameter-efficient method when supported

PyTorch, CUDA, Apple MPS, and MLX have different compatibility requirements. Check that your Python version, framework versions, and hardware backend are supported together before starting a long training run.

## Current scope

This repository is primarily a practical reference and starting point for Qwen 0.5B fine-tuning experiments. It is intended to help users understand the end-to-end workflow and adapt the scripts and configurations to their own datasets and hardware.

Results will depend heavily on dataset quality, training configuration, hardware, and software versions. Reproducible runs should record the operating system, Python version, framework versions, hardware, dataset size, sequence length, and YAML configuration.

## Roadmap

- Add a complete, tested YAML training example
- Provide a reproducible environment with pinned versions
- Improve dataset validation and preprocessing utilities
- Add clearer evaluation metrics and sample comparisons
- Document supported CPU, CUDA, MPS, and MLX workflows
- Explore parameter-efficient fine-tuning for lower-memory devices

## Contributing

Issues, suggestions, documentation improvements, and reproducible experiment reports are welcome. When reporting a problem, include your operating system, Python version, PyTorch version, hardware backend, configuration, and error output.

## Disclaimer

This repository is intended for educational and research use. Verify that your datasets, model usage, and generated outputs comply with applicable licenses, privacy requirements, and the terms of the base model.
