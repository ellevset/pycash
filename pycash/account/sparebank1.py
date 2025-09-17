

import pandas as pd

from pycash.guessaccount import guess


class SpareBank1:
    _fullname = 'Assets:Current Assets:Peter:Flytende'

    def __init__(self):
        self.fp = None

    def read(self, fp):
        def parse_descrition(row):
            return row['beskrivelse']

        def set_internal_account(account):
            accounts = {90011417786: 'Assets:Current Assets:Peter:Flytende',
                        90011417794: 'Assets:Current Assets:Peter:Regninger',
                        90011377121: 'Assets:Current Assets:Felles:Leilighetskonto',
                        90011375714: 'Assets:Current Assets:Felles:Visa',
                        90011451372: 'Assets:Current Assets:Marita:Marita sin konto',
                        90011533743: 'Assets:Current Assets:Marita:Marita sin andre konto'}

            try:
                acc = accounts[account]
            except:
                acc = None
            return acc

        df = pd.read_csv(fp, delimiter=';',
                         encoding='utf-8',
                         #skiprows=1,
                         decimal=',')
        df.columns = ['date', 'beskrivelse', 'date_booked', 'value_in', 'value_out', 'account_to', 'account_from', 'NN']
        df['description'] = df.apply(lambda row: parse_descrition(row),
                                     axis=1)

        df['value_out'] = df['value_out'].abs()
        # df['value_out'] = df['value_out'].str.replace('−', '').str.replace(',', '.').astype(float)

        df.description = df.description.fillna('')

        self.fp = '{:s}_transactions.csv'.format(fp.rsplit('.')[0])

        # Set from the account_from value
        df.loc[df.value_in.isna(), 'expense_account'] = df.loc[df.value_in.isna(), 'account_to'].apply(set_internal_account)
        df.loc[df.value_out.isna(), 'expense_account'] = df.loc[df.value_out.isna(), 'account_from'].apply(set_internal_account)
        df.loc[df.expense_account.isna(), 'expense_account'] = guess(self._fullname, df.loc[df.expense_account.isna(), 'description'])

        return df