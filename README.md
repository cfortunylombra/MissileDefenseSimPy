# MissileDefenseSimPy
A Python-based simulation for a Patriot Air Defense System, designed to detect and neutralize hostile threats using radar signals.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/cfortunylombra/MissileDefenseSimPy/graphs/commit-activity) ![python 3.10](https://img.shields.io/badge/version-latest-blue.svg) ![python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)

## Overview

This project simulates the detection and engagement process of a Patriot Air Defense System. It processes radar data from a CSV file, detects hostiles based on binary patterns, and simulates engagements with a defined Probability of Kill (Pk). Results are logged for analysis.

## Features

- **Radar Data Processing**: Reads binary data from CSV to simulate radar signals.
- **Hostile Detection**: Detects hostiles by analyzing odd/even binary patterns.
- **Engagement Simulation**: Engages detected hostiles with a configurable success rate (Pk).
- **Reproducible Results**: Supports random seed for consistent simulation outcomes.
- **Real-Time Simulation**: Optional 1-second delay per time step for realism.

## Project Structure
    .
    ├── main.py # Main script to run the simulation
    ├── src/
    │ ├── functions.py # Contains the PatriotAirDefenseSystem class
    │ └── radar_data.csv # Sample radar data (semicolon-separated binary values)
    └── output/ # Output directory (generated for seeds 0,1,2,3,4,5,6,7,8,9,10)
    ├── log_0.txt # Example log file (seed=0)
    └── results_0.txt # Example simulation results (seed=0)
    └── README.md

## Prerequisites

- Python 3.x

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cfortunylombra/MissileDefenseSimPy.git
   cd MissileDefenseSimPy

2. **Create the output directory (required for saving results)**:
    ```bash
    mkdir output

3. **Run the simulation:**:
    ```bash
    python main.py

4. **View results**:
    - Check `output/log_0.txt` for detailed step-by-step logs ("_0" suffix indicates random seed=0).
    -  Check `output/results_0.txt` for aggregated simulation statistics ("_0" suffix indicates random seed=0)

## Configuration Parameters (in `main.py`)

- `rng_number = 0`: Random seed for reproducibility (determines output filenames, e.g., log_0.txt).
- `Pk = 0.8`: Probability of successful engagement (0.0 to 1.0).
- `time_bool = True`: Enable 1-second delay per time step for real-time simulation.

## How it works?

1. **Radar Data**: Each CSV row represents a time step with 11 binary numbers.
2. **Odd/Even Analysis**: Hostile detected if more binary numbers end with 1 (odd) than 0 (even).
3. **Engagement**: If detected, a missile is launched with an 80% success chance (configurable via Pk).

## Example Output 

Log File (`log_0.txt`):

    Time step  5s: Radar data ['0110100', '1011111', '0101101', '1010111', '1101011', '0010001', '1011111', '1111010', '0100100', '1000110', '0101010']
    Hostile detected & Missile launched! Engaging target...
    Hostile identified & Missile neutralized the target.

Result File (`result_0.txt`):

    --SIMULATION RESULTS--
    Total Hostiles: 20
    Hostiles Detected: 10
    Probability of Detection: 50.00%
    Hostiles Identified: 9
    Probability of Identification: 45.00%
    Simulated Pk Ratio [#Identification/#Detection]: 0.90


## Customization 

- **Modify Radar Data**: Update `src/radar_data.csv` with new binary values (semicolon-separated).
- **Adjust Parameters**: Change `Pk`, `rng_number`, or `time_bool` in main.py.