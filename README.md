data since methodology
First GitHub Project 
-----------------------------------------------------------------------
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
all_crypto_data = []
pages_to_fetch = 5  # To ensure more than 1000 rows (5 * 250 = 1250)

print("Starting data extraction... Please wait and do not interrupt the code.")

for page in range(1, pages_to_fetch + 1):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': page,
        'sparkline': 'false'
    }
    
    success = False
    attempts = 0
    
    while not success and attempts < 3:  # Try up to 3 times per page
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                all_crypto_data.extend(data)
                print(f" Page {page}: Retrieved {len(data)} coins.")
                success = True
            
            elif response.status_code == 429:
                print(f" Page {page}: Rate limit reached. Waiting 60 seconds...")
                time.sleep(65)  # Slightly longer wait
                attempts += 1
            
            else:
                print(f" Error on page {page}: Status code {response.status_code}")
                break
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
            
    # Normal delay between pages to avoid being blocked
    if success:
        print("Short break (5 seconds)...")
        time.sleep(5)

# Final saving
if len(all_crypto_data) > 0:
    df = pd.DataFrame(all_crypto_data)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"crypto_data_raw_{current_time}.csv"
    df.to_csv(filename, index=False)
    
    print(f"\n Success! Data saved as: {filename}")
    print(f"Dataset shape: {df.shape}")
else:
    print("\n Failed to retrieve data. Try changing your internet connection or try again later.")
import pandas as pd
import os

# 1. Search for the file that starts with "crypto_data_raw"
# (This helps so you don't need to type the date & time manually)
files = [f for f in os.listdir() if f.startswith('crypto_data_raw') and f.endswith('.csv')]
files.sort()  # Sort files so the latest file is last

if files:
    latest_file = files[-1]  # Select the most recently generated file
    print(f" Opening file: {latest_file}")
    
    # 2. Read the file
    df = pd.read_csv(latest_file)
    
    # 3. Display the first 5 rows
    display(df.head())
    
    print(f"\n Number of rows: {df.shape[0]}")
    print(f" Number of columns: {df.shape[1]}")
else:
    print(" No file found starting with 'crypto_data_raw'. Make sure you successfully ran step 1.")
data=pd.read_csv('crypto_data_raw_2025-12-04_15-14.csv')
data.head(1)
data.info()
for col in data.columns:
    print(f'{col}')
    print(f'unique {len(data[col].value_counts())}')
    print(f'null: {data[col].isnull().sum()}')
    print(f'dublicated: {data[col].duplicated().sum()}')
    print('-'*10)
    num_col= data.select_dtypes(include=['int64','float64'])
obj_col= data.select_dtypes(include='object')
num_col.describe()
num_col.info()
data= data.drop_duplicates()
data.duplicated().sum()
df['Price Range (24h)'] = data['high_24h'] - data['low_24h']
df['Price Range Pct (24h)'] = df['Price Range (24h)'] / data['current_price']
df['Volume To Market Cap'] = data['total_volume'] / data['market_cap']
df['Mc Rank Inv'] = 1 / (data['market_cap_rank'] + 1)   # higher rank → higher value
df['Distance From Ath Pct'] = data['ath_change_percentage']      
df['Distance From Atl Pct'] = data['atl_change_percentage']      
df['Log Price'] = np.log1p(data['current_price'])
df['Log Volume'] = np.log1p(data['total_volume'])
df['Log Market Cap'] = np.log1p(data['market_cap'])
df['Profitable (24h)'] = (data['price_change_percentage_24h'] > 0).astype(int)
dff= df[['Log Price', 'Log Volume', 'Log Market Cap',
      'Price Range Pct (24h)', 'Volume To Market Cap',
      'Distance From Ath Pct', 'Distance From Atl Pct',
      'Mc Rank Inv', 'Profitable (24h)']]
      dff.head()

