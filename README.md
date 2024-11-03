# README

## Overview

This repository contains two Python scripts that interact with the Upstox API to facilitate options trading. The first script retrieves an access token necessary for API requests, while the second script fetches option chain data, calculates required margins and premiums, and saves the results to an Excel file.

## Features

### Script 1: Access Token Retrieval
- Authenticates with the Upstox API using OAuth 2.0.
- Retrieves and saves an access token in a `.env` file for secure access.

### Script 2: Option Chain Data Retrieval
- Fetches option chain data for specified financial instruments.
- Supports both Put (PE) and Call (CE) options.
- Calculates the margin required for trading options.
- Computes the premium earned from selling options.
- Exports the results to an Excel file.

## Requirements

Before running the scripts, ensure you have the following installed:

- Python 3.x
- `pandas` library
- `requests` library
- `python-dotenv` library

You can install the required libraries using pip:

```bash
pip install pandas requests python-dotenv
```

## Environment Variables

Both scripts use environment variables to manage sensitive information. Create a `.env` file in the same directory as the scripts with the following content:

```plaintext
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
CODE=your_authorization_code_here
REDIRECT_URI=https://127.0.0.2
```

Replace `your_api_key_here`, `your_api_secret_here`, and `your_authorization_code_here` with your actual Upstox API credentials.

## Usage Instructions

### Step 1: Run the Access Token Retrieval Script

1. **Set Up Your Environment**: Ensure your `.env` file is configured with your Upstox API credentials.

2. **Run the Script**: Execute this script to retrieve an access token:

   ```bash
   python access_token_script.py
   ```

   If successful, this script will save the access token in your `.env` file. You should see a confirmation message indicating that the access token has been saved.

### Step 2: Run the Option Chain Data Retrieval Script

1. **Set Up Your Environment**: Ensure your `.env` file now contains the newly saved access token.

2. **Run the Script**: Execute this script using Python. You can modify the parameters in the `get_option_chain_data` function call at the bottom of the script to specify different instruments, expiry dates, and option types.

   ```bash
   python option_chain_script.py
   ```

3. **View Results**: After running, check for an Excel file named `option_chain_results.xlsx` in your working directory containing the calculated margins and premiums.

## Functions

### Script 1 Functions

#### `save_access_token(token: str)`

Saves the retrieved access token to the `.env` file for future use.

### Script 2 Functions

#### `get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame`

**Inputs**:
- `instrument_name`: Name of the instrument (e.g., NIFTY or BANKNIFTY).
- `expiry_date`: The expiration date of the options, in YYYY-MM-DD format.
- `side`: Type of option to retrieve; use "PE" for Put and "CE" for Call.

**Function Logic**:
1. Retrieve option chain data from Upstox API.
2. For each strike price:
   - If `side == "PE"`, select the highest bid price.
   - If `side == "CE"`, select the highest ask price.
3. Organize this data into a DataFrame with columns:
   - `instrument_name`, `strike_price`, `side`, and `bid/ask`.

#### `calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame`

**Inputs**:
- `data`: The DataFrame returned by `get_option_chain_data`.

**Function Logic**:
1. **Margin Calculation**:
   - For each row (representing an option contract), request margin requirement from Upstox API based on transaction type "Sell".
   
2. **Premium Calculation**:
   - Multiply the bid/ask price by a predefined lot size for each option to calculate premium earned.

**Output**:
- Return the modified DataFrame with new columns:
  - `margin_required` and `premium_earned`.

## Error Handling

Both scripts include error handling for network requests and data validation. In case of any issues (e.g., invalid parameters or network errors), informative messages will be printed to the console.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Your feedback is welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

By following this README, you should be able to set up and run both scripts successfully, gaining insights into options trading through Upstox's API while securely managing your credentials. Happy trading!