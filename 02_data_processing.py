import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
import glob
import re

def clean_and_process_data(raw_dir="data/raw", processed_dir="data/processed"):
    os.makedirs(processed_dir, exist_ok=True)
    
    # 1. Clean 02_nav_history.csv
    print("Cleaning 02_nav_history...")
    nav_df = pd.read_csv(f"{raw_dir}/02_nav_history.csv")
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(by=['amfi_code', 'date'])
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    # Forward-fill missing NAVs (grouping by scheme)
    nav_df = nav_df.set_index('date').groupby('amfi_code').apply(lambda x: x.asfreq('D').ffill()).reset_index(level=0, drop=True).reset_index()
    # Validate NAV > 0
    nav_df = nav_df[nav_df['nav'] > 0]
    nav_df.to_csv(f"{processed_dir}/02_nav_history_clean.csv", index=False)

    # 2. Clean 08_investor_transactions.csv
    print("Cleaning 08_investor_transactions...")
    txn_df = pd.read_csv(f"{raw_dir}/08_investor_transactions.csv")
    
    # Parse the specific 'transaction_date' column and rename it to 'date' for the SQL schema
    if 'transaction_date' in txn_df.columns:
        txn_df['transaction_date'] = pd.to_datetime(txn_df['transaction_date'], errors='coerce')
        txn_df.rename(columns={'transaction_date': 'date'}, inplace=True)

    # Standardize transaction types
    if 'transaction_type' in txn_df.columns:
        txn_df['transaction_type'] = txn_df['transaction_type'].astype(str).str.upper().str.strip()
        valid_types = ['SIP', 'LUMPSUM', 'REDEMPTION']
        txn_df.loc[~txn_df['transaction_type'].isin(valid_types), 'transaction_type'] = 'OTHER'
    
    # Validate amounts (must be > 0)
    if 'amount' in txn_df.columns:
        txn_df = txn_df[txn_df['amount'] > 0]
        
    # Check KYC status
    if 'kyc_status' in txn_df.columns:
        txn_df['kyc_status'] = txn_df['kyc_status'].astype(str).str.upper().fillna('PENDING')
        
    txn_df.to_csv(f"{processed_dir}/08_investor_transactions_clean.csv", index=False)

    # 3. Clean 07_scheme_performance.csv
    print("Cleaning 07_scheme_performance...")
    perf_df = pd.read_csv(f"{raw_dir}/07_scheme_performance.csv")
    return_cols = [col for col in perf_df.columns if 'return' in col.lower()]
    for col in return_cols:
        perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
    
    # Rename expense_ratio_pct to expense_ratio to match the SQLite schema
    if 'expense_ratio_pct' in perf_df.columns:
        perf_df.rename(columns={'expense_ratio_pct': 'expense_ratio'}, inplace=True)
        
    perf_df['expense_ratio'] = pd.to_numeric(perf_df['expense_ratio'], errors='coerce')
    
    # Flag expense ratio anomalies
    perf_df['expense_anomaly_flag'] = ~perf_df['expense_ratio'].between(0.1, 2.5)
    perf_df.to_csv(f"{processed_dir}/07_scheme_performance_clean.csv", index=False)

    # Process remaining generic CSVs
    all_files = glob.glob(f"{raw_dir}/*.csv")
    
    # Core files to skip in the generic loop
    core_files = ['02_nav_history.csv', '08_investor_transactions.csv', '07_scheme_performance.csv']
    
    for file in all_files:
        filename = os.path.basename(file)
        if filename not in core_files:
            df = pd.read_csv(file)
            df.to_csv(f"{processed_dir}/{filename.replace('.csv', '_clean.csv')}", index=False)

    return nav_df, txn_df, perf_df

def load_to_sqlite(processed_dir="data/processed", db_path="sqlite:///bluestock_mf.db"):
    print(f"\nLoading datasets into {db_path}...")
    engine = create_engine(db_path)
    
    csv_files = glob.glob(f"{processed_dir}/*.csv")
    for file in csv_files:
        base_name = os.path.basename(file)
        table_name = base_name.replace('_clean.csv', '')
        table_name = re.sub(r'^\d{2}_', '', table_name) 
        
        df = pd.read_csv(file)
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        # FIXED: Wrapped {table_name} in double quotes for SQLite
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
            print(f"Table '{table_name}' loaded with {result} rows. (Matches CSV: {len(df) == result})")


if __name__ == "__main__":
    clean_and_process_data()
    load_to_sqlite()