# Marvelous Algorithm

---

First of all, you might be wondering why we called it *marvelous*. While trying to come up with a name, we thought about using the initials of our names: **R** and **J**. That reminded us of the *Marvelous City*, Rio de Janeiro. So... why not call it the **Marvelous Algorithm**?

## Introduction

---

Our final assignment for the *Graphs* course uses **SAGA (Scheduling Algorithms Gathered)**, a Python toolkit/library for designing, comparing, and visualizing DAG-based computational workflow scheduling on heterogeneous compute networks (also known as *dispersed computing*).

SAGA includes a collection of scheduling algorithms, such as classic heuristics (HEFT, CPOP), brute-force baselines, SMT-based optimizers, and more — all accessible through a unified API.

All algorithms are implemented in Python with a common interface.
**Credits to the creator: Bhaskar Krishnamachari.**

Our goal is to compare our custom implementation against existing algorithms using a graph dataset provided by the SAGA library.

## Project Layout

---

The source code is located in the `src/` directory and organized as follows:

```
├── data/                   # Input datasets and task graphs (GXL, CSV, etc.)
├── experiments.py          # Main script for running and comparing experiments
├── graph_utils.py          # Utility functions for loading and handling graphs
├── image/                  # Generated visual outputs (graphs, Gantt charts, etc.)
├── image_gen.py            # Script for automated image generation
├── marvelous_algorithm.py  # Custom task scheduling algorithm implementation
├── marvelous_scheduler.py  # Wrapper to integrate the custom algorithm into the SAGA framework
├── processors.py           # Processor architecture definitions (e.g., heterogeneity)
├── results/                # Experimental results (CSV files, logs, makespan data, etc.)
└── saga/                   # Original SAGA library source (schedulers, utils, etc.)
```

## Prerequisites

---

### Python version

All components of this project have been tested with **Python 3.11**.
To ensure compatibility and simplify environment management, we recommend using **Conda**.

To create a new Conda environment:

```bash
conda create -n saga-env python=3.11
conda activate saga-env
```

## Usage

---

### Local Installation

Clone the repository and install the requirements:

```bash
git clone https://github.com/ryann0097/marvelous-matching-algorithm.git
cd marvelous-matching-algorithm
pip install -e .
```

This command installs all the project's dependencies 😄
Note that this work is focused on evaluating a **single custom algorithm**. If you're interested in testing a broader set of schedulers, we recommend installing the original SAGA library from its official repository.
