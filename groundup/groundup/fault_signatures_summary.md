# Fault Signatures Summary

This document summarizes the fault signatures found in the `poc/smart-dc-dev-console/groundup/groundup/fault signatures` folder, based on the provided Parquet files and the "Fault Patterns For Pumps_Chillers.pdf" documentation.

## Overview

The dataset consists of high-frequency vibration signatures for various fault types in pumps and chillers. Unlike the Run-to-Failure (R2F) scenarios which track degradation over time, these files are **Steady State Fault Signatures** (snapshots of the machine in a specific faulty state).

## Sensors and Data Format

Each signature contains vibration data captured across different axes and frequency bands.

**Common Sensors (Types):**

- **x_low_frequency**: Vibration in X-axis (low frequency)
- **y_low_frequency**: Vibration in Y-axis (low frequency)
- **z_low_frequency**: Vibration in Z-axis (low frequency)
- **z_high_frequency**: Vibration in Z-axis (high frequency)
- **z_long**: Longitudinal vibration in Z-axis (present in some files)

**Data Format:**

- **timestamp**: ISO 8601 timestamp of the capture.
- **sample_rate**: Sampling frequency (e.g., 4001 Hz).
- **acceleration**: A list of vibration amplitudes (typically 32,768 samples per row).
- **type**: The sensor/frequency identifier.



## Fault Signatures Details

Each file represents a single synchronous capture burst. For each row in a file, the `acceleration` column contains a 32,768-sample vibration array.


| Fault Type                 | File                             | Rows | Sensors Present                     | Timestamp           |
| -------------------------- | -------------------------------- | ---- | ----------------------------------- | ------------------- |
| **Cavitation**             | `cavitation.parquet`             | 4    | x_low, y_low, z_low, z_high         | 2025-01-07 07:29:58 |
| **Damaged Bearing**        | `damaged_bearing.parquet`        | 1    | y_low                               | 2024-12-27 16:59:58 |
| **Damaged Coupling**       | `damaged_coupling.parquet`       | 4    | x_low, y_low, z_low, z_high         | 2024-12-19 06:59:58 |
| **Damaged Impeller Blade** | `damaged_impeller_blade.parquet` | 5    | x_low, y_low, z_low, z_high, z_long | 2024-12-12 07:59:58 |
| **Misalignment**           | `misalignment.parquet`           | 5    | x_low, y_low, z_low, z_high, z_long | 2025-06-17 23:59:58 |
| **Structural Looseness**   | `structural_looseness.parquet`   | 4    | x_low, y_low, z_low, z_high         | 2024-08-09 21:59:58 |
| **Unbalance**              | `unbalance.parquet`              | 4    | x_low, y_low, z_low, z_high         | 2024-09-09 06:59:58 |




## File Descriptions



### 1. Cavitation (`cavitation.parquet`)

- **Description:** High-frequency broadband noise caused by vapor bubbles collapsing.
- **Coverage:** Tri-axial (X, Y, Z) low frequency + Mono-axial (Z) high frequency.
- **Key Evidence:** Significant 1X vibration in direction of looseness and high-frequency broadband noise.



### 2. Damaged Bearing (`damaged_bearing.parquet`)

- **Description:** Snapshot of a machine with a loose roller element or race defect.
- **Coverage:** Mono-axial (Y) low frequency only.
- **Key Evidence:** High-frequency energy at bearing defect frequencies.



### 3. Damaged Coupling (`damaged_coupling.parquet`)

- **Description:** Vibration profile of a damaged jaw coupling.
- **Coverage:** Tri-axial (X, Y, Z) low frequency + Mono-axial (Z) high frequency.
- **Key Evidence:** Elevated 1X and 2X radial vibration.



### 4. Damaged Impeller Blade (`damaged_impeller_blade.parquet`)

- **Description:** Worn or damaged vanes in a centrifugal pump.
- **Coverage:** Full Tri-axial + Z-High + Z-Longitudinal.
- **Key Evidence:** High peaks at the vane-pass frequency.



### 5. Misalignment (`misalignment.parquet`)

- **Description:** Common shaft misalignment between motor and pump.
- **Coverage:** Full Tri-axial + Z-High + Z-Longitudinal.
- **Key Evidence:** High radial vibration at 1X running speed; sometimes high 2X.



### 6. Structural Looseness (`structural_looseness.parquet`)

- **Description:** Mechanical looseness in the machine base or housing.
- **Coverage:** Tri-axial (X, Y, Z) low frequency + Mono-axial (Z) high frequency.
- **Key Evidence:** Significant 1X vibration primarily in the direction of the looseness.



### 7. Unbalance (`unbalance.parquet`)

- **Description:** Mass unbalance in the rotating assembly.
- **Coverage:** Tri-axial (X, Y, Z) low frequency + Mono-axial (Z) high frequency.
- **Key Evidence:** High 1X radial vibration.



## Sensor Frequency & Payload Matrix

This matrix shows the **Sampling Rate** and the **Array Length** (number of acceleration samples) for each sensor in each fault capture.


| Sensor Type          | Cavitation    | Damaged Bearing | Damaged Coupling | Damaged Impeller Blade | Misalignment   | Structural Looseness | Unbalance     |
| -------------------- | ------------- | --------------- | ---------------- | ---------------------- | -------------- | -------------------- | ------------- |
| **x_low_frequency**  | 8kHz / 9216   | -               | 4kHz / 5120      | 4kHz / 5120            | 4kHz / 5120    | 4kHz / 5120          | 4kHz / 5120   |
| **y_low_frequency**  | 8kHz / 9216   | 4kHz / 5120     | 4kHz / 5120      | 4kHz / 5120            | 4kHz / 5120    | 4kHz / 5120          | 4kHz / 5120   |
| **z_high_frequency** | 32kHz / 32768 | -               | 51kHz / 16384    | 51kHz / 16384          | 51kHz / 16384  | 51kHz / 16384        | 51kHz / 16384 |
| **z_long**           | -             | -               | -                | 51kHz / 131072         | 51kHz / 131072 | -                    | -             |
| **z_low_frequency**  | 8kHz / 9216   | -               | 5kHz / 9216      | 5kHz / 9216            | 5kHz / 9216    | 5kHz / 9216          | 5kHz / 9216   |


*(Note: 4kHz = 4001Hz, 5kHz = 5120Hz, 32kHz = 32000Hz, 51kHz = 51200Hz)*

## Technical Definitions



### Fault vs. Failure

The data in these files represents the machine in a **faulty** state, not necessarily a state of total **failure**.

- **Fault:** A physical abnormality (e.g., cavitation, misalignment). The machine is **still running**, but it is vibrating in a way that indicates a problem is present.
- **Failure:** The point where the machine stops working or trips (e.g., a broken shaft).



### Data Structure Confirmation

Each signature consists of the following physical components:


| Component             | Meaning in Physics                                                                                                                 |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Triaxial Sensors**  | Vibration measured in three orthogonal axes: **X** (horizontal), **Y** (vertical), and **Z** (axial/longitudinal).                 |
| **Acceleration**      | The physical quantity measured (m/s^2 or g). Represents the rate of change of surface velocity.                                    |
| **Frequency Band**    | The "Type" (Low vs. High) focuses on specific physical phenomena (e.g., high-frequency hiss vs. low-frequency thumping).           |
| **Sample Rate** (f_s) | The number of times the sensor "listens" per second. High f_s captures fast shocks (bearings); Low f_s captures mechanical shifts. |
| **Array of Values**   | A discrete time-series of 32,768 individual measurements.                                                                          |




## Usage in Machine Learning



### 1. Classification (Fault Type)

The primary use for this data is **Fault Classification**. A model reads a vibration window and predicts the label (e.g., "Cavitation" vs. "Unbalance").

### 2. The "Single Timestamp" Limitation

You are correct: **one timestamp per fault is insufficient** for training a robust, generalized deep learning model from scratch.

- **Why it's insufficient:** It only provides a single operating point. It doesn't show how the fault looks at different speeds, loads, or stages of severity.
- **What is missing:** A **degradation sequence** (like the R2F datasets) is required to see the "path" from healthy to failure.



### 3. How to use this data anyway

Despite the limitation, these files are used as:

- **Gold Standards:** Reference patterns to compare against live telemetry.
- **Data Augmentation:** One 32,768-sample array can be chopped into 32 smaller windows of 1,024 samples each, creating 32 "labeled" training rows from a single capture.
- **Synthetic Pre-training:** Using these physics-based patterns to "teach" a model what a fault looks like before fine-tuning it on real, noisy plant data.



## Comparison: R2F vs. Fault Signatures


| Feature         | Fault Signatures (this folder)                       | R2F Scenarios (r2f folder)                                |
| --------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| **Nature**      | Steady state snapshots of specific faults.           | Time-series tracking degradation from healthy to failure. |
| **Time Depth**  | Single timestamp per fault type.                     | Hours/days of data showing fault evolution.               |
| **Purpose**     | Identifying frequency patterns for specific defects. | Training models to predict Remaining Useful Life (RUL).   |
| **Injection**   | Pre-injected / Already present.                      | Transition from healthy to faulty is captured.            |
| **Final State** | A specific faulty operating point.                   | Trip or dirty state after a failure progression.          |


**Conclusion:** These files are **not R2F** datasets; they are **Fault Signatures** used for pattern recognition of specific mechanical failures in Xylem pumps and Trane chillers.