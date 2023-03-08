import sys
import pandas as pd

# get the file names from command-line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py firefly.csv raiffeisen.csv")
    sys.exit(1)

firefly_file = sys.argv[1]
raiffeisen_file = sys.argv[2]

# read in the two CSV files
firefly = pd.read_csv(firefly_file, encoding='ISO-8859-1', delimiter=',')
raiffeisen = pd.read_csv(raiffeisen_file, encoding='ISO-8859-1', delimiter=';')

# use isin() to check if column H of firefly exists in column D of raiffeisen
matches = raiffeisen[~raiffeisen['Credit/Debit Amount'].isin(firefly['amount'])]

# output the missing rows to missing.csv
matches.to_csv('missing.csv', index=False)
