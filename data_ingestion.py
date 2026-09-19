import pandas as pd
import os
import glob

def load_and_inspect_datasets(raw_dir="data/raw"):
    # Look for the 10 provided CSVs
    csv_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    dataframes = {}
    
    print("--- Inspecting Raw CSV Datasets ---")
    for file in csv_files:
        filename = os.path.basename(file)
        try:
            df = pd.read_csv(file)
            dataframes[filename] = df
            print(f"\nDataset: {filename} | Shape: {df.shape}")
            print("Data Types:\n", df.dtypes.to_dict())
            print("First 3 rows:\n", df.head(3))
            
            # Simple anomaly check: highlight columns with high null values
            nulls = df.isnull().sum()
            if nulls.any():
                print("Anomalies (Null Counts):\n", nulls[nulls > 0].to_dict())
                
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            
    return dataframes

def explore_and_validate(dataframes):
    print("\n--- Exploring Fund Master ---")
    
    # Look for the relevant files (adjust exact filenames based on your 10 provided CSVs)
    master_file = next((f for f in dataframes.keys() if 'master' in f.lower()), None)
    nav_file = next((f for f in dataframes.keys() if 'nav' in f.lower() and 'live' not in f.lower()), None)
    
    if master_file and nav_file:
        fund_master = dataframes[master_file]
        nav_history = dataframes[nav_file]
        
        # 1. Print unique segments (assuming standard column names)
        cols = fund_master.columns.str.lower()
        if 'fund_house' in cols:
            print("Unique Fund Houses:", fund_master['fund_house'].nunique())
        if 'category' in cols:
            print("Categories:", fund_master['category'].unique())
        if 'risk_grade' in cols:
            print("Risk Grades:", fund_master['risk_grade'].unique())
            
        # 2. AMFI Code Structure Note
        if 'scheme_code' in fund_master.columns:
            code_lengths = fund_master['scheme_code'].astype(str).str.len().unique()
            print(f"AMFI Code length structure: {code_lengths} digits")
        
        # 3. Validation and DQ Summary
        print("\n--- Validation: AMFI Code Integrity ---")
        if 'scheme_code' in fund_master.columns and 'scheme_code' in nav_history.columns:
            master_codes = set(fund_master['scheme_code'].unique())
            history_codes = set(nav_history['scheme_code'].unique())
            
            missing_in_history = master_codes - history_codes
            missing_in_master = history_codes - master_codes
            
            dq_summary = f"""
Data Quality Summary:
- Successfully parsed {len(master_codes)} unique AMFI codes from the fund master.
- {len(history_codes)} unique schemes possess historical NAV data.
- Anomalies: {len(missing_in_history)} master codes lack historical data.
- Anomalies: {len(missing_in_master)} codes in NAV history are orphaned (missing from fund master).
            """
            print(dq_summary.strip())
    else:
        print("\nNote: Fund Master or NAV History CSV not detected among the files.")

if __name__ == "__main__":
    dfs = load_and_inspect_datasets()
    if dfs:
        explore_and_validate(dfs)
    else:
        print("No CSV files found in data/raw. Please place the 10 provided datasets there before running.")