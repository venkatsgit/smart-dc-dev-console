# GitHub Issue Templates: R2F Failure Classification System

This file contains the detailed specifications for the three core components of the Run-to-Failure (R2F) failure classification system.

---

## Issue 1: Failure Classification Data Preprocessing Component
**Title:** Implement R2F Data Preprocessing Pipeline and Windowing Engine

**Description:**
Develop a robust data preprocessing component to transform raw centrifugal chiller simulation CSVs into model-ready feature matrices for binary and multi-class failure classification. These datasets are critical assets and must be versioned.

**Requirements:**
1.  **Data Ingestion:** Load raw CSV files from directory (Azure File Storage). Parse folder structures to identify Fault Family, Load (58/80), Severity (SL1-SL4), and Injection Type.
2.  **Sanity Checks:**
    *   Verify timestamp continuity and frequency (1-minute intervals).
    *   Detect and handle missing values (NaN) and infinities.
    *   Numeric conversion of object-type sensor columns.
    *   Confirm presence of healthy baseline (first 24 hours of every file).
3.  **Windowing Engine:**
    *   Implement a sliding window of **60 minutes** with a **10-minute stride** (50-minute overlap).
    *   Feature Extraction: Compute **Mean, Standard Deviation, Slope, and Last Value** per sensor per window.
4.  **Labeling & Weighting:**
    *   **Binary Label:** 0 (Healthy stretch) vs 1 (Fault injected stretch).
    *   **Multi-Class Label:** Specific Fault ID for faulty segments.
    *   **Sample Weights:** Calculate weights for the multi-class set to balance scenarios and fault classes:
        `Weight = 1.0 / (windows_per_scenario * scenarios_per_class)`
5.  **Data Versioning (MLflow):** 
    *   Log the resulting CSV datasets as **MLflow Artifacts**.
    *   Use MLflow tags to version the data assets (e.g., `data_version: v1.0`).

**Expected Data Outcomes (CSV):**

### Binary Classification Dataset (`df_binary.csv`)
| scenario_id | fault | severity | elapsed_hours | label | sensor_1__mean | sensor_1__std | ... |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| healthy__80 | 01_healthy | healthy | 5.0 | **0** | ... | ... | ... |
| fouling__SL1 | 02_fouling | SL1 | 24.0 | **1** | ... | ... | ... |

### Multiclass Classification Dataset (`df_multiclass.csv`)
| scenario_id | fault | fault_label | elapsed_hours | sensor_1__mean | ... | sample_weight |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| leak__SL2 | 04_leak | 1 | 25.5 | 180.2 | ... | 1.20 |
| gas__SL1 | 09_gas | 2 | 24.0 | 210.0 | ... | 3.50 |

---

## Issue 2: Failure Classification Training Engine
**Title:** Build Two-Stage Failure Classification Training Engine with MLflow Integration

**Description:**
Develop the training pipeline for the Stage-1 Detector (Binary) and Stage-2 Diagnostician (Multi-class) using the versioned CSV datasets from the preprocessing stage.

**Requirements:**
1.  **Model Architectures:** Implement both **Logistic Regression** (baseline) and **XGBoost** (optimized) for both stages.
2.  **Validation Strategy:**
    *   Use **Leave-One-Scenario-Out (LOSO)** cross-validation.
    *   Ensure no data leakage from overlapping windows by holding out entire simulation files during testing.
3.  **Training with Weights (Multi-class):**
    *   Utilize the `sample_weight` column from the input CSV during model training for the multi-class stage.
    *   Ensure weights are NOT used as features.
4.  **MLflow Governance:**
    *   Log all hyperparameters and performance metrics (Accuracy, F1, ROC-AUC).
    *   Register the winning model versions in the MLflow Model Registry.

**Outcomes:**
*   Trained Binary Model Artifact.
*   Trained Multi-class Model Artifact.
*   MLflow Experiment logs linking models to the specific data version used.

---

## Issue 3: Failure Classification Prediction Engine (Inference)
**Title:** Implement Real-time Failure Classification Prediction Engine

**Description:**
Create the inference component that applies the two-stage logic (Detector -> Diagnostician) to new sensor data streams.

**Requirements:**
1.  **Unified Preprocessing:** Mirror the 60-minute windowing and feature extraction logic used in Issue 1.
2.  **Inference Cascade:**
    *   **Stage 1:** Pass the window to the Binary Model.
    *   **Stage 2:** If Stage 1 detects a fault (`prob >= 0.5`), pass the SAME window to the Multi-class Model for diagnosis.
3.  **Real-time Feature Computation:** Must handle rolling data buffers efficiently.
4.  **Output Payload:** Structured JSON with Health Status, Fault Type (if any), and Confidence Score.

**Outcomes:**
*   Production Inference script/module.
*   Verified cascade logic preventing diagnostic calls on healthy machines.
