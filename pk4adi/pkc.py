#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pkc.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import math
import pandas as pd
from scipy.stats import norm, t
from pk4adi.utils import print_table
from pk4adi.pk import calculate_pk

__all__  = ["compare_pks", "print_pks"]

def compare_pks(pk1, pk2):
    """
    Compare two answers of the pk values, which is the output of the function calculate_pk().
        print_pks() will be called before return the ans.

    Parameters
    ----------
    pk1 : a dict.
        The output of the function calculate_pk().
    pk2 : a dict.
        The output of the function calculate_pk().

    Returns
    -------
    ans : a dict.
        A dict containing all the matrix and variables involved in.
        Use to script 'print(ans.keys())' to get the details.
        The most important variables all already been printed.

    References
    ----------
    To be added.

    Notes
    -----
    To be added.

    """

    ans = {}
    ans.update({"type": "pkc"})

    # check the input type of pk1 and pk2.
    assert isinstance(pk1, dict) and pk1.get("type", "unknown") == "pk", "pk1 must be the output of the function calculate_pk()."
    assert isinstance(pk2, dict) and pk2.get("type", "unknown") == "pk", "pk2 must be the output of the function calculate_pk()."
    assert pk1.get("n_case") == pk2.get("n_case"), "The n_case of pk1 and pk2 must be the same."
    assert pk1.get("n_case") > 1, "The n_case of pk1 and pk2 must be greater than 1."


    n_case = pk1.get("n_case")
    ans.update({"n_case": n_case})

    # calculate the p value using scipy.norm.
    PKD = pk1.get("PKj") - pk2.get("PKj")
    SED = math.sqrt(pk1.get("SEj") * pk1.get("SEj") + pk2.get("SEj") * pk2.get("SEj"))
    ZD = PKD / SED
    ZP, ZJ = Z2P(ZD)

    # save the variables.
    ans.update({"PKD": PKD})
    ans.update({"SED": SED})
    ans.update({"ZD": ZD})
    ans.update({"ZP": ZP})
    ans.update({"ZJ": ZJ})

    # calculate the p value using scipy.t.
    PKmD = pk1.get("PKm") - pk2.get("PKm")
    SumD = 0
    SSD = 0
    for i in range(n_case):
        current = PKmD[i]
        SumD = SumD + current
        SSD = SSD + current * current

    DF = n_case - 1
    PKDJ = n_case * PKD - DF / n_case * SumD
    SEDJ = math.sqrt( DF / n_case * ( SSD - 1 / n_case * SumD * SumD ))
    TD = PKDJ / SEDJ
    TP, TJ = T2P(TD, DF)

    # save the variables.
    ans.update({"PKmD": PKmD})
    ans.update({"SumD": SumD})
    ans.update({"SSD": SSD})
    ans.update({"DF": DF})
    ans.update({"PKDJ": PKDJ})
    ans.update({"SEDJ": SEDJ})
    ans.update({"TD": TD})
    ans.update({"TP": TP})
    ans.update({"TJ": TJ})

    # format and print.
    print_pks(ans)

    # return the ans.
    return ans


def print_pks(result, floatfmt=".3f", tablefmt='simple'):
    """
    Pretty display of two pk calculation result comparison.

    Parameters
    ----------
    result : a dict.
        Must be the return value of function compare_pks().
    floatfmt : string.
        Decimal number formatting.
    tablefmt : string.
        Table format (e.g. 'simple', 'plain', 'html', 'latex', 'grid', 'rst').
        For a full list of available formats, please refer to
        https://pypi.org/project/tabulate/

    Returns
    -------
    Nothing will be returned.

    Notes
    -----
    To be added.

    """

    if isinstance(result, dict) and result.get("type", "unkonwn") == "pkc":
        df1 = pd.DataFrame({"PKD": result.get("PKD"),
                            'SED': result.get("SED"),
                            'ZD': result.get("ZD"),
                            'P value': result.get("ZP"),
                            "Comment": result.get("ZJ")},
                            index=[0])
        df2 = pd.DataFrame({"PKDJ": result.get("PKDJ"),
                            'SEDJ': result.get("SEDJ"),
                            'DF': result.get("DF"),
                            'TD': result.get("TD"),
                            'P value': result.get("TP"),
                            "Comment": result.get("TJ")},
                            index=[0])

        print('==============\nPKs comparison\n==============\n')
        print('=================\nFor Group (z-test)\n=================\n')
        print_table(df1, floatfmt, tablefmt)
        print('=================\nFor Pair (t-test)\n=================\n')
        print_table(df2, floatfmt, tablefmt)


def Z2P(target):
    """
    Query the p value matching the output of pks comparison using scipy.norm.

    Parameters
    ----------
    target : float.
        Must be ZD in the return dict of function compare_pks().

    Returns
    -------
    p: float.
        The p value.
    comment: string.
        The interval of the returned p value.

    Notes
    -----
    Please refer https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html for more details.

    """

    value = abs(target)
    auc = norm.cdf(value) - 0.5
    p = 1 - 2 * auc
    return p, judgeP(p)


def T2P(target, df, verbose = False):
    """
    Query the p value matching the output of pks comparison using scipy.t.

    Parameters
    ----------
    target : float.
        Must be TD in the return dict of function compare_pks().
    df : int.
        The degrees of freedom.
    verbose : bool, default value is False.
        Choose whether print the intermediate output of locating the p value using the dichotomy algorithm.

    Returns
    -------
    p: float.
        The p value.
    comment: string.
        The interval of the returned p value.

    Notes
    -----
    Please refer https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html for more details.

    """

    value = abs(target)
    left = 0.99999
    right = 0.00001
    current = 10000
    mid = None
    while abs(current - value) > 0.0001:
        lv = t.ppf(1 - left, df)
        rv = t.ppf(1 - right, df)

        mid = (left + right) / 2
        current = t.ppf(1 - mid, df)

        if verbose:
            print("left is %.4f , right  ppf is %.5f" % (left, right))
            print("left value is %.4f , right  ppf is %.5f" % (lv, rv))
            print("mid is %.4f (not exact p-value), current ppf is %.5f" % (mid, current))

        if current < value:
            left, right = mid, right
        else:
            left, right = left, mid

    p = mid
    if verbose:
        print("The p value for df at %3d and ppf at %.4f is %.4f (delta < 0.0001)." % (df, value, p))

    return p, judgeP(p)


def judgeP(p):
    """
    Judge the interval of a p value.

    Parameters
    ----------
    p: float.
        The p value.

    Returns
    -------
    comment: string.
        The interval of the returned p value.

    Notes
    -----
    To be added.

    """

    if p > 0.05:
        return "P > 0.05"
    elif p > 0.01:
        return "P > 0.01"
    elif p > 0.001:
        return "P > 0.001"
    else:
        return "P < 0.001"

if __name__ == "__main__":

    x1 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
    y1 = [ 1, 1, 1, 1, 1, 2, 1, 1, 3, 3, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3 ]

    pk1 = calculate_pk(x_in = x1, y_in = y1)

    x2 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
    y2 = [ 1, 1, 2, 1, 1, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 2 ]

    pk2 = calculate_pk(x_in = x2, y_in = y2)

    ans = compare_pks(pk1, pk2)
    print_pks(ans)


