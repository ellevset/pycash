

import pandas as pd

from pycash.guessaccount import guess


class Dnb:
    _fullname = 'Liabilities:Credit Card:DNB Master'
    columns = ['date', 'description', 'NN', 'NN2', 'value_in', 'value_out']

    def __init__(self):
        pass

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

        df = pd.read_excel(fp)

        df.columns = self.columns

        df.description = df.description.fillna('')

        df['expense_account'] = guess(self._fullname, df['description'])

        self.fp = '{:s}_transactions.csv'.format(fp.rsplit('.')[0])

        return df


def make():
    return Dnb()