

import pandas as pd

from pycash.account.dnb import Dnb
from pycash.guessaccount import guess

class DnbBrukskonto(Dnb):
    _fullname = 'Assets:Current Assets:DNB:Peter:Brukskonto'
    columns = ['date', 'description', 'NN', 'value_out', 'value_in']

    def __init__(self):
        super().__init__()

def make():
    return DnbBrukskonto()