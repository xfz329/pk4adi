#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   utils.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""


from tabulate import tabulate

__all__ = ["print_table"]

def print_table(df, floatfmt=".3f", tablefmt='simple'):
    """
    Pretty display of table.

    Parameters
    ----------
    df : a pandas.DataFrame.
        Dataframe to print.
    floatfmt : string.
        Decimal number formatting.
    tablefmt : string.
        Table format (e.g. 'simple', 'plain', 'html', 'latex', 'grid', 'rst').
        For a full list of available formats, please refer to
        https://pypi.org/project/tabulate/.

    Returns
    -------
    Nothing will be returned.

    Notes
    -----
    To be added.

    """

    print(tabulate(df, headers="keys", showindex=False, floatfmt=floatfmt,
                    tablefmt=tablefmt))
    print("\n")