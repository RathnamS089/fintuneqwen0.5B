# Fine-tuning Qwen 0.5B

An experimental project for preparing data and fine-tuning **Qwen 0.5B** models on modest hardware.

> **Status:** Experimental / work in progress

## Motivation

This repository was inspired by [Soup](https://github.com/razor-ai/soup), a project that makes language-model training and fine-tuning configurable through YAML files and aims to reduce the hardware and setup burden for local experimentation. Soup describes a workflow where training can be driven from a single YAML configuration, including low-memory approaches such as layer streaming. citeturn0search0

The goal here was to explore a similar, practical workflow for a smaller Qwen model: collect or prepare data, preprocess it, configure training, and evaluate the result without requiring a large machine.

## Repository layout

```text
.
├── data/           # Training and evaluation data
├── evaluvation/    # Evaluation scripts and outputs
├── preprocessing/  # Dataset preparation and preprocessing
├── scrapper/       # Data collection / scraping utilities
├── training/       # Training scripts and configuration files
├── requirements.txt
└── git.md          # Git and virtual-environment notes
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/RathnamS089/fintuneqwen0.5B.git
cd fintuneqwen0.5B
```

### 2. Create a virtual environment

Using a virtual environment helps keep PyTorch and other machine-learning dependencies isolated from the rest of your system.

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

The current requirements file contains the utilities used for data collection and processing, including `requests`, `beautifulsoup4`, `lxml`, and `tqdm`. Training dependencies may need to be installed separately depending on your operating system, Python version, and accelerator.

### 4. Prepare data

Use the scripts in `scrapper/` and `preprocessing/` to collect and transform data into the format expected by the training workflow. Review the files in `data/` before starting a run, and keep private or copyrighted data out of the repository.

### 5. Configure and run training

Training configuration is intended to be controlled through YAML files in `training/`. Update the model, dataset, batch size, gradient accumulation, number of epochs, output directory, and device settings for your hardware before running a script.

Because this project is experimental, the exact command may depend on the training script and configuration currently present in `training/`. Start by inspecting that directory:

```bash
find training -maxdepth 2 -type f
```

## Hardware and backend notes

- A smaller model does not guarantee a successful fine-tuning run; memory usage also depends on sequence length, batch size, optimizer, precision, and framework versions.
- PyTorch versions must be compatible with your Python version and hardware backend.
- Apple Silicon users may encounter additional compatibility issues when combining PyTorch, MPS, and MLX-based tooling. MLX is a separate backend and should not be assumed to work with a PyTorch training script without corresponding support.
- If a run fails, first check the Python, PyTorch, Transformers, and accelerator versions together rather than upgrading one package in isolation.
- Use small datasets, short sequence lengths, gradient accumulation, and frequent checkpoints while debugging.

## Current limitations

This project did not consistently produce promising fine-tuning results yet. Some experiments were affected by:

- Python/PyTorch version compatibility problems
- Differences between CUDA, CPU, MPS, and MLX environments
- Limited hardware and memory
- Early-stage preprocessing and evaluation workflows
- The need for more careful dataset quality checks and hyperparameter tuning

The repository should therefore be treated as an experiment and learning resource, not as a guaranteed recipe for producing a high-quality fine-tuned model.

## Recommended next steps

- Pin and document a known-good Python and PyTorch environment.
- Add a reproducible training YAML example and a matching command.
- Record hardware, backend, dataset size, sequence length, and hyperparameters for every run.
- Add validation-loss and sample-generation comparisons before and after fine-tuning.
- Test a small, clean dataset before scaling up.
- Add automated checks for dataset format and duplicate or low-quality examples.

## Contributing

Issues, suggestions, and small improvements are welcome. If you reproduce a training result, please include your operating system, Python version, PyTorch version, backend, hardware, configuration, and error output.

## Disclaimer

This repository is for educational and experimental use. Always verify that your training data and generated outputs comply with applicable licenses, privacy requirements, and the terms of the base model.
