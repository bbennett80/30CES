# Introduction
The `30CES` project is a colloborative effort at CSU - Bakersfield in the Department of Biology, under the guidance of Dr. Luke Hall, PhD, and lead by Gradute students Megan McCullah-Boozer and Rachel Budge.

# Stack
- [Streamlit](https://streamlit.io/)
- [birdnetlib](https://github.com/joeweiss/birdnetlib)

# Installation and Usage Guide

[![Astral UV](https://img.shields.io/badge/Astral%20UV-Fast%20Python%20Package%20Management-blue)](https://astral.sh/uv)

Astral UV (or simply "UV") is a fast, modern Python package management tool designed as a drop-in replacement for pip, pip-tools, and virtualenv. This guide explains how to install and use UV on both macOS and Windows systems.

## Table of Contents

- [Installation](#installation)
  - [macOS Installation](#macos-installation)
  - [Windows Installation](#windows-installation)
- [Basic Usage](#basic-usage)
  - [Creating Virtual Environments](#creating-virtual-environments)
  - [Activating Virtual Environments](#activating-virtual-environments)
  - [Installing Packages](#installing-packages)
  - [Installing from requirements.txt](#installing-from-requirementstxt)
- [Troubleshooting](#troubleshooting)

## Installation

### macOS Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows Installation

#### Using PowerShell (Official Installation Script)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## Basic Usage

### Creating Virtual Environments

Create a new virtual environment in the current directory:

```bash
uv venv
```

This creates a `.venv` directory with a Python environment.

To use a specific Python version:

```bash
uv venv --python=python3.11
```

Or use the included python [virtual enfironment](https://docs.python.org/3/tutorial/venv.html).

### Activating Virtual Environments

#### On macOS/Linux:

```bash
source .venv/bin/activate
```

#### On Windows:

```powershell
.venv\Scripts\activate
```

### Installing Packages

### Installing from requirements.txt

```bash
uv pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

**"Command not found" after installation**:
- Make sure the installation directory is in your PATH
- Restart your terminal or command prompt

**Permission errors on macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sudo sh
```

**Windows execution policy issues**:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
irm https://astral.sh/uv/install.ps1 | iex
```

**Launch WebUI**:
```base
streamlit run ui/Home.py
```
The WebUI uses [Streamlit](docs.streamlit.io) to simplify develpment and usage.


**Compatibility with existing environments**:
UV is designed to be compatible with environments created by virtualenv/venv.

For more information, visit the [official Astral UV documentation](https://astral.sh/uv).



# 30CES

Make sure to double check variables:
  - min_conf = 0.7
  - padding_secs = 0.5
  - dpi = 300
  - audio_format = 'wav'
  - spectrogram_format = 'jpg'

 `30CES` is not associated with BirdNET-Lite, BirdNET-Analyzer, `birdnetlib` or the K. Lisa Yang Center for Conservation Bioacoustics.

 # CONTRIBUTIONS
 Always welcome:)

