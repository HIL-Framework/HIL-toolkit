# Setup

## Requirements

- Python 3.10 or higher. Download [here](https://www.python.org/downloads/release/python-3100/)
- liblsl (Lab Streaming Layer). More information [here](https://labstreaminglayer.readthedocs.io/)

## Installation

### 1. Install Python

Download and install Python 3.10 or higher from the official Python website.

### 2. Install liblsl

There are two ways to install liblsl depending on your system:

#### Option A: Using pre-built binaries (recommended for Windows and macOS)

1. Download the appropriate package for your system from [here](https://github.com/sccn/liblsl/releases)
2. Extract the package and follow the installation instructions provided in the package

#### Option B: Building from source (for Linux, Raspberry Pi, or if pre-built binaries are not available)

Use the provided installation script:

```bash
./install_liblsl.sh
```

This script will:
1. Clone the liblsl repository if it doesn't exist
2. Compile liblsl
3. Set up the necessary environment variables

Note: This method is recommended for Linux and Raspberry Pi systems, or if pre-built binaries are not available for your system.

### 3. Install Python requirements

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Install the HIL package

To install the HIL package in editable mode, run:

```bash
pip install -e .
```

## Testing

To run all tests, use pytest:

```bash
pytest tests/
```

This will run all test files in the `tests/` directory.

## Verifying the Installation

After installation, you can verify that everything is set up correctly by running:

```bash
python -c "import pylsl; print(pylsl.__version__)"
```

This should print the version of pylsl without any errors.
