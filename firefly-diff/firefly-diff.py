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
df = pd.read_csv(filename, encoding='ISO-8859-1', delimiter=';')

# Get the first and last "Valuta Date" values
first_valuta_date = df.loc[0, 'Valuta Date']
last_valuta_date = df.loc[df.index[-1], 'Valuta Date']

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
df = df[df["Credit/Debit Amount"] < 0]

# check how many duplicate values are in given csv
df_duplicates = df.duplicated(subset=["Credit/Debit Amount"]).sum()

# Print duplicate count
print(f'Raiffeisen Duplicates: {df_duplicates}')

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
    api_df = pd.read_csv(BytesIO(api_response.content))

    # save all firefly-transactions to html
    api_df.to_html('firefly.html', index=False)

    # Print the first 5 rows of the API DataFrame
    #print(api_df.head())

    # check how many duplicate values are in given csv
    api_df_duplicates = api_df.duplicated(subset=["amount"]).sum()

    # Print duplicate count
    print(f'Firefly Duplicates: {api_df_duplicates}')

    # use isin() to check if the transaction already exists in firefly
    diff_df = df[~df['Credit/Debit Amount'].isin(api_df['amount'])]

    # only show needed columns
    diff_df = diff_df[['Valuta Date', 'Text', 'Credit/Debit Amount']]

    # set justify option to left for both column headers
    pd.set_option('colheader_justify', 'left')

    # print the number of missing transactions
    print(f'Missing Transactions: {len(diff_df)}')

    # save csv to html file
    diff_df.to_html('index.html', index=False)

else:
    # Print an error message if the API request was not successful
    print(f'API request failed with status code {api_response.status_code}')
