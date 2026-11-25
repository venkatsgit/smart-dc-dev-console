import pandas as pd
import numpy as np
import os

def read_fault_signature(file_path):
    """
    Reads a fault signature Parquet file and returns a formatted DataFrame.
    
    Columns in the Parquet:
    - timestamp: The start time of the capture.
    - sample_rate: The sampling frequency in Hz.
    - acceleration: A list of 32,768 vibration samples.
    - type: The sensor identifier (e.g., 'z_high_frequency', 'x_low_frequency').
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    
    df = pd.read_parquet(file_path)
    
    print(f"\n--- Summary for: {os.path.basename(file_path)} ---")
    print(f"Total Rows (Sensors): {len(df)}")
    
    for idx, row in df.iterrows():
        n_samples = len(row['acceleration'])
        duration = n_samples / row['sample_rate']
        print(f"Row {idx}: Type={row['type']}, Sample Rate={row['sample_rate']} Hz, Samples={n_samples}, Duration={duration:.2f}s")
        
    return df

def get_time_axis(row):
    """
    Calculates the relative time axis for a specific sensor row.
    """
    n_samples = len(row['acceleration'])
    sample_rate = row['sample_rate']
    return np.linspace(0, (n_samples - 1) / sample_rate, n_samples)

if __name__ == "__main__":
    # Example usage for cavitation
    base_path = r"poc/smart-dc-dev-console/groundup/groundup/fault signatures"
    target_file = os.path.join(base_path, "cavitation.parquet")
    
    df_cav = read_fault_signature(target_file)
    
    if df_cav is not None:
        # Example: Accessing the X-axis low frequency data
        x_low = df_cav[df_cav['type'] == 'x_low_frequency']
        if not x_low.empty:
            accel_data = x_low.iloc[0]['acceleration']
            time_axis = get_time_axis(x_low.iloc[0])
            print(f"\nFirst 5 timestamps for x_low_frequency: {time_axis[:5]}")
            print(f"First 5 acceleration values: {accel_data[:5]}")
