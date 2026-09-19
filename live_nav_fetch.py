import requests
import pandas as pd
import os

def fetch_and_save_nav(scheme_code, scheme_name, output_dir="data/raw"):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching NAV for {scheme_name} ({scheme_code})...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            # Cast the API response types
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df['nav'] = pd.to_numeric(df['nav'])
            df['scheme_code'] = scheme_code
            df['scheme_name'] = scheme_name
            
            file_path = os.path.join(output_dir, f"{scheme_code}_nav_live.csv")
            df.to_csv(file_path, index=False)
            print(f"Success: Saved {len(df)} records to {file_path}")
        else:
            print(f"Warning: No historical NAV data found for {scheme_code}.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {scheme_code}: {e}")

if __name__ == "__main__":
    # Ensure raw data directory exists
    os.makedirs("data/raw", exist_ok=True)
    
    # Target schemes mapped by AMFI code
    target_schemes = {
        "125497": "HDFC Top 100 Direct",
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    
    for code, name in target_schemes.items():
        fetch_and_save_nav(code, name)