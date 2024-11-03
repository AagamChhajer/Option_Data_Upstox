# README

## Overview

This Python script retrieves option chain data for specified financial instruments using the Upstox API. It calculates the required margin and premium for options trading and saves the results in an Excel file. The script is designed to be user-friendly, handling errors gracefully and providing informative output.

## Features

- Fetches option chain data for a given instrument and expiry date.
- Supports both Put (PE) and Call (CE) options.
- Calculates the margin required for trading options.
- Computes the premium earned from selling options.
- Exports the results to an Excel file.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- `pandas` library
- `requests` library
- `python-dotenv` library

You can install the required libraries using pip:

```bash
pip install pandas requests python-dotenv
```

## Environment Variables

The script uses environment variables to securely manage sensitive information. You need to create a `.env` file in the same directory as the script with the following content:

```
ACCESS_TOKEN=your_access_token_here
```

Replace `your_access_token_here` with your actual Upstox API access token.

## Usage

To use this script, follow these steps:

1. **Set Up Your Environment**: Ensure you have your `.env` file configured with your Upstox API access token.

2. **Run the Script**: Execute the script using Python. You can modify the parameters in the `get_option_chain_data` function call at the bottom of the script to specify different instruments, expiry dates, and option types.

   ```python
   if __name__ == "__main__":
       try:
           df = get_option_chain_data("Nifty 50", "2024-11-28", "PE")
           result_df = calculate_margin_and_premium(df)

           result_df.to_excel('option_chain_results.xlsx', index=False)
           print("Data saved to option_chain_results.xlsx")

       except Exception as e:
           print(f"An error occurred: {e}")
   ```

3. **View Results**: After running, check for an Excel file named `option_chain_results.xlsx` in your working directory containing the calculated margins and premiums.

## Functions

### `get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame`

Fetches option chain data from Upstox API based on instrument name, expiry date, and option type (PE or CE). Returns a DataFrame containing relevant option details.

### `calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame`

Calculates margin requirements and premium earned for each option contract in the provided DataFrame. Returns an updated DataFrame with additional columns for margin required and premium earned.

## Error Handling

The script includes error handling for network requests and data validation. In case of any issues (e.g., invalid parameters or network errors), appropriate messages will be printed to the console.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Your feedback is welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

By following this README, you should be able to set up and run the script successfully, gaining insights into options trading through Upstox's API. Happy trading!