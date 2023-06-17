#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pk.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import math
import pandas as pd
import numpy as np
from pk4adi.utils import print_table

__all__  = ["calculate_pk", "print_pk"]

def calculate_pk(x_in , y_in):
    """
    Compute the pk value to Measure the Performance of Anesthetic Depth Indicators.
        print_pk() will be called before return the ans.

    Parameters
    ----------
    x_in : a list or a pandas series (pandas.Series()).
        Indicator.
    y_in : a list or a pandas series (pandas.Series()).
        State.

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
    ans.update({"type" : "pk"})
    x = x_in
    y = y_in

    # check the input type of x and y.
    assert isinstance(x, list) or isinstance(x, pd.Series) , "x should be a list or pandas.Series."
    assert isinstance(y, list) or isinstance(y, pd.Series) ,  "y should be a list or pandas.Series."

    # convert the list to pandas.Series if needed.
    if isinstance(x_in, list):
        x = pd.Series(x_in)
    if isinstance(y_in, list):
        y = pd.Series(y_in)

    assert not x.apply(lambda n: not isinstance(n, (int, float))).any() , "x should not contain any non-num."
    assert not y.apply(lambda n: not isinstance(n, (int, float))).any(), "y should not contain any non-num."
    assert not x.isna().any() , "x should not contain any nan."
    assert not y.isna().any(), "y should not contain any nan."
    assert len(x) == len(y) , "x and y should contain the same cases."
    assert len(x) >= 2 , "x and y should contain at least two cases."

    # get n_cases.
    n_case = len(x)

    # construct basic matrix.
    data = pd.DataFrame({"x": x, "y": y, "k": range(n_case), "Ry": [0] * n_case,"Cx": [0] * n_case, "PKm": [0] * n_case})

    # check y and set the category.
    data.sort_values("y", inplace=True)
    current = data.iloc[0, 1]
    category = 0
    for i in range(n_case):
        if current == data.iloc[i, 1]:
            data.iloc[i, 3] = category
        else:
            current = data.iloc[i, 1]
            category += 1
            data.iloc[i, 3] = category

    # whether jackknife could be done or not.
    y_category = data.iloc[:, 1].tolist()
    jack_ok = True
    for i in set(y_category):
        if y_category.count(i) < 2:
            jack_ok = False

    # get the row num for the matrix.
    rows = len(set(y_category))
    assert rows >= 2 , "The distinct values of y should be at least two."
    if rows > 2:
        jack_ok = True

    # check x  and set the category.
    data.sort_values("x", inplace=True)
    current = data.iloc[0, 0]
    category = 0
    for i in range(n_case):
        if current == data.iloc[i, 0]:
            data.iloc[i, 4] = category
        else:
            current = data.iloc[i, 0]
            category += 1
            data.iloc[i, 4] = category

    # get the col num for the matrix
    x_category = data.iloc[:, 0].tolist()
    cols = len(set(x_category))

    # restore data by the index k.
    data.sort_values("k", inplace=True)

    # construct matrix A.
    A = np.zeros((rows, cols), dtype=int)
    for k in range(n_case):
        i = data.iloc[k, 3]
        j = data.iloc[k, 4]
        A[i, j] = A[i, j] + 1

    # construct matrix S.
    S = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        S[i, 0] = A[i, 0]
        for j in range(1, cols):
            S[i, j] = S[i, j - 1] + A[i, j]

    # construct matrix C, D and T with the help of the assist matrix SA, CA, DA and TA.
    C = np.zeros((rows, cols), dtype=int)
    D = np.zeros((rows, cols), dtype=int)
    T = np.zeros((rows, cols), dtype=int)
    SA = np.zeros((rows, 2), dtype=int)
    CA = np.zeros((rows, 2), dtype=int)
    DA = np.zeros((rows, 2), dtype=int)
    TA = np.zeros((rows, 2), dtype=int)
    for i in range(rows):
        for j in range(cols):
            if A[i, j] != 0:
                for ai in range(rows):
                    if ai < i:
                        if j > 0:
                            C[i, j] = C[i, j] + S[ai, j - 1]
                        if j < cols - 1:
                            D[i, j] = D[i, j] + S[ai, cols - 1] - S[ai, j]
                        T[i, j] = T[i, j] + A[ai, j]
                    elif ai > i:
                        if j < cols - 1:
                            C[i, j] = C[i, j] + S[ai, cols - 1] - S[ai, j]
                        if j > 0:
                            D[i, j] = D[i, j] + S[ai, j - 1]
                        T[i, j] = T[i, j] + A[ai, j]
                CA[i, 0] = CA[i, 0] + A[i, j] * C[i, j]
                DA[i, 0] = DA[i, 0] + A[i, j] * D[i, j]
                TA[i, 0] = TA[i, 0] + A[i, j] * T[i, j]
                CA[1, 1] = CA[1, 1] + A[i, j] * C[i, j] * C[i, j]
                DA[1, 1] = DA[1, 1] + A[i, j] * D[i, j] * D[i, j]
                TA[1, 1] = TA[1, 1] + A[i, j] * C[i, j] * D[i, j]
            else:
                pass
        SA[0, 0] = SA[0, 0] + S[i, cols - 1]
        CA[0, 1] = CA[0, 1] + CA[i, 0]
        DA[0, 1] = DA[0, 1] + DA[i, 0]
        TA[0, 1] = TA[0, 1] + TA[i, 0]

    # calculate.
    n = SA[0, 0]
    Qc = CA[0, 1]
    Qd = DA[0, 1]
    Qtx = TA[0, 1]
    Qcdt = Qc + Qd + Qtx
    dyx = (Qc - Qd) / Qcdt
    PK = (dyx + 1) / 2
    Qcc = CA[1, 1]
    Qdd = DA[1, 1]
    Qcd = TA[1, 1]
    Term1 = Qcc - 2 * Qcd + Qdd
    Term2 = 0
    Term3 = 0

    for i in range(rows):
        ni = S[i, cols - 1]
        Qci = CA[i, 0]
        Qdi = DA[i, 0]
        Term2 = Term2 + (n - ni) * (Qci - Qdi)
        Term3 = Term3 + ni * (n - ni) * (n - ni)

    Term2 = -2 * dyx * Term2
    Term3 = dyx * dyx * Term3
    SE1 = math.sqrt(Term1 + Term2 + Term3) / Qcdt
    SE0 = math.sqrt(Term1 - (Qc - Qd) * (Qc - Qd) / n) / Qcdt


    SPKm = np.nan
    SSPKm = np.nan
    PKj = np.nan
    SEj = np.nan

    # do jackknife.
    if jack_ok:
        SPKm = 0
        SSPKm = 0

        for k in range(n_case):
            i = data.iloc[k, 3]
            j = data.iloc[k, 4]
            Crc = C[i, j]
            Drc = D[i, j]
            Trc = T[i, j]
            Qcm = Qc - 2 * Crc
            Qdm = Qd - 2 * Drc
            Qtxm = Qtx - 2 * Trc
            Qcdtm = Qcm + Qdm + Qtxm
            PKm = (Qcm + Qtxm / 2) / Qcdtm
            data.iloc[k, 5] = PKm
            SPKm = SPKm + PKm
            SSPKm = SSPKm + PKm * PKm

        PKj = n_case * PK -(n_case - 1) * SPKm / n_case
        SEj = math.sqrt((n_case - 1) * (SSPKm - SPKm * SPKm / n_case) / n_case)


    # save the matrix.
    ans.update({"A" : A})
    ans.update({"S" : S})
    ans.update({"C" : C})
    ans.update({"D" : D})
    ans.update({"T" : T})
    ans.update({"SA" : SA})
    ans.update({"CA" : CA})
    ans.update({"DA" : DA})
    ans.update({"TA" : TA})

    # save the variables.
    ans.update({"jack_ok" : jack_ok})
    ans.update({"n_case": n_case})
    ans.update({"n" : n})
    ans.update({"Qc" : Qc})
    ans.update({"Qd" : Qd})
    ans.update({"Qtx" : Qtx})
    ans.update({"Qcdt" : Qcdt})
    ans.update({"dyx" : dyx})
    ans.update({"PK" : PK})
    ans.update({"Qcc" : Qcc})
    ans.update({"Qdd" : Qdd})
    ans.update({"Qcd" : Qcd})
    ans.update({"Term1" : Term1})
    ans.update({"Term2" : Term2})
    ans.update({"Term3" : Term3})
    ans.update({"SE1" : SE1})
    ans.update({"SE0" : SE0})
    ans.update({"PKm" : data["PKm"]})
    ans.update({"SPKm" : SPKm})
    ans.update({"SSPKm" : SSPKm})
    ans.update({"PKj" : PKj})
    ans.update({"SEj" : SEj})

    # format and print.
    print_pk(ans)

    # return the ans.
    return ans

def print_pk(result, floatfmt=".3f", tablefmt='simple'):
    """
    Pretty display of a pk calculation result.

    Parameters
    ----------
    result : a dict.
        Must be the return value of function calculate_pk().
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

    if isinstance(result, dict) and result.get("type","unkonwn") == "pk":
        df = pd.DataFrame({"PK": result.get("PK"),
                            'SE0': result.get("SE0"),
                            'SE1': result.get("SE1"),
                            'jack_ok': result.get("jack_ok"),
                            "PKj": result.get("PKj"),
                            'SEj': result.get("SEj")},
                            index=[0])
        print('==============\nPK calculation\n==============\n')
        print_table(df, floatfmt, tablefmt)


if __name__ == "__main__":

    x = [ 0, 0, 0, 0, 0, 0]
    y = [ 1, 1, 1, 1, 1, 2]
    calculate_pk(x, y)

    x = [0, 0, 0, 0, 0, 0, 1, 1, 2]
    y = [1, 1, 1, 1, 1, 2, 3, 3, 4]
    calculate_pk(x, y)

