
import numpy as np
import pandas as pd

from pygnu.guessaccount import guess

_fullname = 'Liabilities:Credit Card:SAS Eurocard'


def read(fp):
    def parse_descrition(row):
        if row['value_foreign'] > 0.0:
            s = '%s - %.2f (%s)' % (row['specification'], row['value_foreign'], row['currency'])
        else:
            s = '%s' % (row['specification'])
        return s

    df = pd.read_excel(fp)

    # Find where the data starts
    row_start = df.loc[df.Fakturadetaljer == 'Dato'].tail(1).index[0]

    df = pd.read_excel(fp,
                       dtypes={7: np.float64},
                       skiprows=row_start + 1)

    df['Dato'] = pd.to_datetime(df['Dato'], errors='coerce')
    df = df[~df['Dato'].isnull()]
    df.columns = ['date', 'date_booked', 'specification', 'location', 'currency', 'value_foreign', 'value']
    df['description'] = df.apply(lambda row: parse_descrition(row),
                                 axis=1)

    # Guess accounts
    df['expense_account'] = guess(_fullname, df.description)
    #
    fp = fp.replace('.xls', '.csv')

    return df, fp
