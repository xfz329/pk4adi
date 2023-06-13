#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pkc.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University

@Modify Time        @Author       @Version    @Desciption
------------        -------       --------    -----------
2023/6/13 16:20   silencejiang      1.0         None
"""

import math
from pk4adi.pk import PK


class PKCompare:
    ALL_CHECKS_OK = 0
    ALL_CALCULATION_OK = 1

    INPUT_TYPE_ERROR =  10
    INPUT_CASES_NOT_EQUAL = 11


    def __init__(self):
        self.PKmD = None
        self.n_case = 0
        self.PKD = None
        self.SED = None
        self.ZD = None
        self.SumD = None
        self.SSD = None
        self.DF = None
        self.PKDJ = None
        self.SEDJ = None
        self.TD = None


    def compare(self,pk_in_1= None,pk_in_2 = None):
        state = self.check_cases(pk_in_1,pk_in_2)
        if state != PK.ALL_CHECKS_OK:
            return state

        self.calculate(pk_in_1, pk_in_2)
        self.show_result()


    def check_cases(self,pk_in_1= None,pk_in_2 = None):
        if not ( isinstance(pk_in_1,PK) and isinstance(pk_in_2,PK) ):
            print("INPUT_TYPE_ERROR")
            return PKCompare.INPUT_TYPE_ERROR
        if not  ( (pk_in_1.n_case > 1) and (pk_in_1.n_case > 1) and (pk_in_1.n_case == pk_in_2.n_case ) ):
            print("INPUT_CASES_NOT_EQUAL")
            return PKCompare.INPUT_CASES_NOT_EQUAL
        self.n_case = pk_in_1.n_case
        return PKCompare.ALL_CHECKS_OK

    def calculate(self,pk_in_1= None,pk_in_2 = None):
        self.PKD = pk_in_1.dict.get("PKj") - pk_in_2.dict.get("PKj")
        self.SED = math.sqrt(pk_in_1.dict.get("SEj") * pk_in_1.dict.get("SEj") + pk_in_2.dict.get("SEj") * pk_in_2.dict.get("SEj") )
        self.ZD = self.PKD / self.SED

        self.PKmD = pk_in_1.dict.get("PKm") - pk_in_2.dict.get("PKm")
        self.SumD = 0
        self.SSD = 0
        for i in range(self.n_case):
            current = self.PKmD[i]
            self.SumD = self.SumD + current
            self.SSD = self.SSD + current * current

        self.DF = self.n_case - 1
        self.PKDJ = self.n_case * self.PKD - self.DF / self.n_case * self.SumD
        self.SEDJ = math.sqrt(self.DF / self.n_case * (self.SSD - 1 / self.n_case * self.SumD * self.SumD))
        self.TD = self.PKDJ / self.SEDJ

    def show_result(self):
        print("The result is as following :")
        print("For groups :")
        print("PKD is %.3f" % self.PKD)
        print("SED is %.3f" % self.SED)
        print("ZD  is %.3f" % self.ZD)

        print("For pairs :")
        print("PKD is %.3f" % self.PKDJ)
        print("SED is %.3f" % self.SEDJ)
        print("TD  is %.3f" % self.TD)
        print("DF  is %3d" % self.DF)

        print("PKmD matrix is :")
        print(self.PKmD)

if __name__ == "__main__":

    x1 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
    y1 = [ 1, 1, 1, 1, 1, 2, 1, 1, 3, 3, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3 ]

    pk1 = PK()
    pk1.calculate_pk(x_in = x1, y_in = y1)

    x2 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
    y2 = [ 1, 1, 2, 1, 1, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 2 ]

    pk2 = PK()
    pk2.calculate_pk(x_in = x2, y_in = y2)

    pkc = PKCompare()
    pkc.compare(pk_in_1 = pk1, pk_in_2 = pk2)

