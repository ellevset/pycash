
"""
Script to convert

"""

import sys
import importlib
import logging

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    ###print kwargs
    #df = read_sas(fp)
    #df = read_sparebank1(fp)
    #df.to_csv(fp.replace('_L', 'L'),
    #          encoding='utf-8',
    #          index=False)
    #df.to_csv(fp.replace('xlsx', 'csv'),
    #          index=False)

    m = importlib.import_module('pycash.account.%s' % kwargs['model'])
    logger.info(f"Account {m}")
    df, fp = m.read(kwargs['fp'])

    # Writing out
    logger.info(f'Writing to {fp}')
    df.to_csv(fp,
              index=False,
              encoding='utf-8')


def set_argparser(parser):
    parser.description = 'Stuff'
    parser.add_argument('model')
    parser.add_argument('fp')


if __name__ == '__main__':
    main(model=sys.argv[1], fp=sys.argv[2])
