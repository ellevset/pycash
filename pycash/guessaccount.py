from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

import pandas as pd
from math import fabs
import piecash
from piecash import open_book

# Path to the gnucash-book
# TODO find a smarter way
# fp = '/home/ellevset/Dropbox/Documents/Gnucash/working/working.gnucash'
fp = '/Users/ellevset/Dropbox/Documents/Gnucash/working/working.gnucash'


def guess(account, description):

    book = open_book(fp, open_if_lock=True, readonly=True)

    data = list()
    for t in book.transactions:
        row = {'description': t.description,
               'date': t.post_date}

        for s in t.splits:
            if s.account.type == 'EXPENSE':
                row['expense_account'] = s.account.fullname
            else:
                row['charge_account'] = s.account.fullname
        row['value'] = fabs(t.splits[0].value)

        data.append(row)
    df = pd.DataFrame(data).dropna()

    # Only get data from the account we are ML-ing
    df = df.loc[df.charge_account == account]

    # Train the machine
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB(alpha=0.4))])
    text_clf = text_clf.fit(df.description, df.expense_account)

    return text_clf.predict(description)