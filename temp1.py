import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    # Validate the side input
    if side not in ["PE", "CE"]:
        raise ValueError("Side must be 'PE' for Put or 'CE' for Call.")

    url = 'https://api.upstox.com/v2/option/chain'
    params = {
        'instrument_key': f'NSE_INDEX|{instrument_name}',
        'expiry_date': expiry_date
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    # Fetch data from the API
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json().get('data', [])
        
        if not data:
            raise ValueError("No data found for the given parameters.")

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

    options_data = []

    # Process each entry in the response data
    for entry in data:
        strike_price = entry['strike_price']
        option_data = entry.get('put_options' if side == "PE" else 'call_options')

        if option_data:
            instrument_key = option_data['instrument_key']
            price = option_data['market_data'].get('bid_price' if side == "PE" else 'ask_price', 0)
            options_data.append({
                'instrument_name': instrument_key,
                'strike_price': strike_price,
                'side': side,
                'bid/ask': price
            })

    # Convert the options data into a DataFrame
    df = pd.DataFrame(options_data, columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    return df

# Constant for lot size
LOT_SIZE = 25

# Function to calculate margin and premium
def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        print("No data available for margin calculation.")
        return data

    # API endpoint for margin calculation
    margin_api_url = 'https://api.upstox.com/v2/charges/margin'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    margins = []
    premiums = []

    # Iterate over each option contract in the DataFrame
    for _, row in data.iterrows():
        instrument_key = row['instrument_name']
        price = row['bid/ask']

        # Check for missing or zero prices
        if price <= 0:
            print(f"Invalid price for instrument {instrument_key}. Skipping.")
            margins.append(0)
            premiums.append(0)
            continue

        # Calculate premium earned
        premium_earned = price * LOT_SIZE
        premiums.append(premium_earned)

        # Prepare margin calculation request payload
        margin_data = {
            "instruments": [
                {
                    "instrument_key": instrument_key,
                    "quantity": LOT_SIZE,
                    "transaction_type": "SELL",
                    "product": "D"
                }
            ]
        }

        # Request margin requirement from API
        try:
            response = requests.post(margin_api_url, headers=headers, json=margin_data)
            response.raise_for_status()  # Raise an error for bad responses

            margin_info = response.json()
            if 'data' in margin_info and 'margins' in margin_info['data']:
                margin_required = margin_info['data']['margins'][0].get('total_margin', 0)
            else:
                print("Unexpected response structure for margin:", margin_info)
                margin_required = 0

        except requests.RequestException as e:
            print(f"Error fetching margin for {instrument_key}: {e}")
            margin_required = 0  # Fallback if API request fails

        margins.append(margin_required)

    # Add the calculated margins and premiums to the DataFrame
    data['margin_required'] = margins
    data['premium_earned'] = premiums

    return data

if __name__ == "__main__":
    try:
        df = get_option_chain_data("Nifty 50", "2024-11-28", "PE")
        result_df = calculate_margin_and_premium(df)

        result_df.to_excel('option_chain_results.xlsx', index=False)
        print("Data saved to option_chain_results.csv")

    except Exception as e:
        print(f"An error occurred: {e}")
