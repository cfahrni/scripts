import pandas as pd
import requests
from datetime import datetime, timedelta
from io import BytesIO
import sys

# define variables
firefly_api = 'https://www.example.com/api/v1/data/export/transactions'
bearer_token = '<token>'
account_id = '<id>'

# Get the filename from the command line argument
filename = sys.argv[1]

# Load the CSV file into a Pandas DataFrame
raiffeisen_df = pd.read_csv(filename, encoding='ISO-8859-1', delimiter=';')

# Get the first and last "Valuta Date" values
first_valuta_date = raiffeisen_df.loc[0, 'Valuta Date']
last_valuta_date = raiffeisen_df.loc[raiffeisen_df.index[-1], 'Valuta Date']

# Convert the first and last "Valuta Date" values to datetime objects
first_valuta_date = datetime.strptime(first_valuta_date, '%Y-%m-%d %H:%M:%S.%f')
last_valuta_date = datetime.strptime(last_valuta_date, '%Y-%m-%d %H:%M:%S.%f')

# Subtract 5 days from the first "Valuta Date" value and add 3 days to the last "Valuta Date" value
first_valuta_date = first_valuta_date - timedelta(days=5)
last_valuta_date = last_valuta_date + timedelta(days=5)

# Print the dates
print(f'First Valuta Date: {first_valuta_date.strftime("%Y-%m-%d")}')
print(f'Last Valuta Date: {last_valuta_date.strftime("%Y-%m-%d")}')

# only use rows with negative values = withdrawals
raiffeisen_df = raiffeisen_df[raiffeisen_df["Credit/Debit Amount"] < 0]

# Set the API parameters
params = {
    'start': first_valuta_date.strftime('%Y-%m-%d'),
    'end': last_valuta_date.strftime('%Y-%m-%d'),
    'accounts': account_id,
    'type': 'csv'
}

# Set the request headers with the bearer token
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

# Make the API request and save the response as a variable
api_response = requests.get(firefly_api, params=params, headers=headers)

# Check if the API request was successful (status code 200)
if api_response.status_code == 200:

    # Load the API response into a new Pandas DataFrame
    firefly_df = pd.read_csv(BytesIO(api_response.content))

    # Print the first 5 rows of the API DataFrame
    # print(firefly_df.head())

    # Create a dictionary to track counts of values in both DataFrames
    raiffeisen_df_counts = raiffeisen_df['Credit/Debit Amount'].value_counts().to_dict()
    firefly_df_counts = firefly_df['amount'].value_counts().to_dict()

    # Find missing rows from raiffeisen_df in firefly_df
    raiffeisen_missing_rows = []
    for key, value in raiffeisen_df_counts.items():
        if key not in firefly_df_counts or firefly_df_counts[key] < value:
            raiffeisen_missing_rows.extend([key] * (value - firefly_df_counts.get(key, 0)))

    # Create a new DataFrame for missing transactions
    raiffeisen_diff_df = raiffeisen_df[raiffeisen_df['Credit/Debit Amount'].isin(raiffeisen_missing_rows)]

    # Find missing rows from firefly_df in raiffeisen_df
    firefly_missing_rows = []
    for key, value in firefly_df_counts.items():
        if key not in raiffeisen_df_counts:
            firefly_missing_rows.extend([key] * (value - raiffeisen_df_counts.get(key, 0)))

    # Create a new DataFrame for missing transactions
    firefly_diff_df = firefly_df[firefly_df['amount'].isin(firefly_missing_rows)]

    # only show needed columns
    raiffeisen_diff_df = raiffeisen_diff_df[['Valuta Date', 'Text', 'Credit/Debit Amount']]
    firefly_diff_df = firefly_diff_df[['date', 'description', 'amount', 'type', 'group_title']]

    # set justify option to left for both column headers
    pd.set_option('colheader_justify', 'left')

    # save csv to html file
    raiffeisen_diff_df.to_html('missing_in_firefly.html', index=False)
    firefly_diff_df.to_html('missing_in_raiffeisen.html', index=False)

else:
    # Print an error message if the API request was not successful
    print(f'API request failed with status code {api_response.status_code}')

