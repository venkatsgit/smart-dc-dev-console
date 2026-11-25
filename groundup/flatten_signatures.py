import pandas as pd
import os
import glob

def flatten_parquet_to_csv(folder_path):
    parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))
    
    for file in parquet_files:
        filename = os.path.basename(file)
        wide_csv_filename = filename.replace(".parquet", "_wide.csv")
        wide_csv_path = os.path.join(folder_path, wide_csv_filename)
        
        print(f"Processing {filename} into wide format...")
        df = pd.read_parquet(file)
        
        # In wide format, we group by timestamp and pivot the 'type' into columns
        # Since 'sample_rate' can differ per type, we'll include it in the column name or as a separate column
        
        # We need to handle the fact that 'acceleration' is a list. 
        # Pivot doesn't easily handle lists without some help.
        
        # Create a dictionary to hold the wide data
        wide_data = {'timestamp': df['timestamp'].iloc[0]}
        
        for _, row in df.iterrows():
            sensor_type = row['type']
            wide_data[f"{sensor_type}_sample_rate"] = row['sample_rate']
            wide_data[f"{sensor_type}_acceleration"] = str(list(row['acceleration']))
            
        wide_df = pd.DataFrame([wide_data])
        wide_df.to_csv(wide_csv_path, index=False)
        print(f"Created {wide_csv_filename}")

if __name__ == "__main__":
    target_folder = r"poc/smart-dc-dev-console/groundup/groundup/fault signatures"
    flatten_parquet_to_csv(target_folder)
