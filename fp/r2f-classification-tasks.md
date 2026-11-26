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
    *   **Understand `elapsed_hours`:** This is the relative clock for the simulation run. 
        *   `elapsed_hours <= 24`: Machine is healthy.
        *   `elapsed_hours > 24`: Machine is "sick" (fault active).
        *   **Sickness Duration:** `elapsed_hours - 24` is how many hours the machine has been operating under a fault.
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
    *   **Log Hyperparameters:** Track settings such as `learning_rate` (step size), `max_depth` (tree complexity), and `n_estimators` (number of trees).
    *   **Log Performance Metrics:**
        *   **Accuracy:** The ratio of correct predictions to total predictions. In our multiclass case, we specifically track **Balanced Accuracy** to account for different simulation lengths.
        *   **F1-Score:** The harmonic mean of Precision and Recall. It ensures the model doesn't just "guess" the most common class. In **Multiclass**, we use **Macro-averaged F1** to treat every fault family (Fouling, Leak, etc.) as equally important.
        *   **ROC-AUC:** The "Area Under the Receiver Operating Characteristic curve." It measures the model's ability to separate classes (Healthy vs. Faulty in Binary; One-vs-Rest in Multiclass). A value of 1.0 indicates a perfect detector.
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
2.  **Training Insight:**
    *   **Labeling:** During training, `elapsed_hours` is used to define the labels: 0 for healthy (<= 24h) and 1 for faulty (> 24h).
3.  **Inference Cascade:**
    *   **Stage 1:** Pass the window to the Binary Model. The output is a single probability (0 to 1).
    *   **Stage 2:** If Stage 1 detects a fault (`prob >= 0.5`), pass the SAME window to the Multi-class Model.
        *   **Softmax Output:** The Multi-class model outputs a probability vector (one per fault class) summing to 1.0.
        *   **Winner:** The fault with the highest probability is the predicted root cause.
        *   **Confidence:** The specific probability of that "winner" is the confidence score.
4.  **Real-time Feature Computation:** Must handle rolling data buffers efficiently.
5.  **Output Payload:** Structured JSON with Health Status, Fault Type (if any), and Confidence Score.

**Outcomes:**
*   Production Inference script/module.
*   Verified cascade logic preventing diagnostic calls on healthy machines.
