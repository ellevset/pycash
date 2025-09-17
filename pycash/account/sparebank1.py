

import pandas as pd

from pycash.guessaccount import guess

_fullname = 'Liabilities:Credit Card:SAS Eurocard'


def read(fp):
    def parse_descrition(row):
        return row['beskrivelse']

    df = pd.read_csv(fp, delimiter=';',
                     encoding='utf-8',
                     skiprows=1,
                     decimal=',')
    df.columns = ['date', 'beskrivelse', 'date_booked', 'value_in', 'value_out', 'account_to', 'account_from', 'NN']
    df['description'] = df.apply(lambda row: parse_descrition(row),
                                 axis=1)
    df['value_out'] = df['value_out'].abs()

    if fp[0] == '_':
        fp = fp[1:]

    df['expense_account'] = guess(_fullname, df.description)

    return df, fp
