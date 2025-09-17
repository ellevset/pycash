
import logging

import pandas as pd

from pycash.guessaccount import guess

logger = logging.getLogger(__name__)

_fullname = 'Liabilities:Credit Card:SAS Eurocard'


def read(fp):
    def parse_descrition(row):
        if row['value_foreign'] > 0.0:
            s = '%s - %.2f (%s)' % (row['specification'], row['value_foreign'], row['currency'])
        else:
            s = '%s' % (row['specification'])
        return s

    # Read the sheet
    #df = pd.read_excel(fp, skiprows=16)
    logger.info(f"Reading file {fp}")
    df = pd.read_excel(fp, engine='xlrd')

    idx = df.index[df['Fakturadetaljer'].str.contains(r'Kjøp/uttak', na=False)]
    idx = idx[0] + 2

    idx2 = df.index[df['Fakturadetaljer'].str.contains(r'Totalt beløp', na=False)]
    idx2 = idx2[1]

    columns = ('Dato', 'Bokført', 'Spesifikasjon', 'Sted', 'Valuta', 'Utl. beløp', 'Beløp')
    df = df[idx:idx2].copy()
    df.columns = columns

    df['Dato'] = pd.to_datetime(df['Dato'], errors='coerce')
    df['Bokført'] = pd.to_datetime(df['Bokført'], errors='coerce')
    df = df[~df['Dato'].isnull()]
    df.columns = ['date', 'date_booked', 'specification', 'location', 'currency', 'value_foreign', 'value']
    df['description'] = df.apply(lambda row: parse_descrition(row),
                                 axis=1)

    df['expense_account'] = guess(_fullname, df.description)

    df = df[['date', 'value', 'description', 'expense_account']]

    fp = fp.replace('.xlsx', '.csv')
    return df, fp
