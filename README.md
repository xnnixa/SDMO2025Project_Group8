# 811372A-3007 Software Development, Maintenance and Operations 2025 Projects

This repository contains example data and scripts showcasing data collection and processing
for projects of the Software Development, Maintenance and Operations.

The three projects are:

- Project 1: Developer de-duplication
- Project 2: Temporal centrality and monitoring metrics
- Project 3: Temporal state detection and anomaly detection

## Contents

- `project1devs/`: Directory with data for Project 1
  - `devs.csv`: List of developers mined from eShopOnContainersProject
  - `devs_similarity.csv`: Similarity tests for each pair of developers
  - `devs_similarity_t=0.7.csv`: Similarity tests for each pair of developers with similarity threshold 0.7
- `project1developers.py`: Script demonstrating mining developer information and Bird heuristic to determine duplicate developers
- `project2&3traces/`: Directory with data for Projects 2 & 3
  - `train-ticket-traces.csv`: CSV file with traces for train-ticket system from an open dataset
  - `project2edgeflow.csv`: CSV file providing a list of real-time service calls for Project 2
  - `project3anomaly.csv`: CSV file providing snapshot networks for service calls grouped by intervals for Project 3
  - `project2_katz_exponential.csv`: CSV file with Temporal Katz Centrality with exponential decay
  - `project2_katz_constant.csv`: CSV file with Temporal Katz Centrality with constant decay
  - `project2_katz_truncated.csv`: CSV file with Temporal Katz Centrality with truncated exponential decay
- `project2&3data.py`: Script processing raw traces into formats required by Projects 2&3
- `project2centrality.py`: Script demonstrating temporal katz centrality on temporal edge flow network of microservice calls for Project 2
- `project3anomaly.py`: Script demonstrating temporal state detection on temporal networks of microservice calls for Project 3
- `requirements.txt`: List of used libraries with specified versions

## Running the scripts

The scripts were developed and tested on a Mac (UNIX) environment with Python 3.10.
There should be no compatibility issues with running the scripts on Windows.

The versions of imported libraries are provided in `requirements.txt`.

It is recommended to create a Python virtual environment and install the exact versions there.

## Environment Setup

The scripts were developed and tested on Python **3.13**, but they are compatible with Python **3.10+**.

It is recommended to use a **virtual environment** to isolate dependencies.

### Steps

1. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scripts**
   ```bash
   python project1developers.py
   python project2centrality.py
   python project3anomaly.py
   ```

## Unit Tests

### Purpose

Unit tests verify the correctness of main functionalities:

- Developer name normalization and similarity (Project 1)
- Inter-service call extraction from trace data (Project 2)
- Temporal state detection and anomaly grouping (Project 3)

---

### Files

- `tests/test_project1developers.py` – tests developer name processing and similarity
- `tests/test_project2centrality.py` – tests data preparation and inter-service call mapping
- `tests/test_project3anomaly.py` – tests interval grouping and state detection (mocked)

---

### How to Run Tests

1. **Navigate to the project directory**  
   Make sure you are in the main project folder (the same level as `requirements.txt`). Example:

   ```bash
   cd SDMO2025Project
   ```

2. **Install pytest and required packages**

   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```

3. **Run all tests**

   ```bash
   pytest -v
   ```

4. **Run a single test file**

   ```bash
   pytest tests/test_project2centrality.py -v
   ```

5. **Stop after first failure (optional)**
   ```bash
   pytest -x
   ```

---
