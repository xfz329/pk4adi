#   -*- coding:utf-8 -*-
#   The pk.py in pk
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 15:41 on 2023/1/1
import pandas as pd
import numpy as np


class PK:
    ALL_CHECKS_OK = 0
    ALL_CALCULATION_OK = 1

    CHECK_CASE_ERROR_DATA_FRAME_COLUMNS = 10
    CHECK_CASE_ERROR_XY_TYPE = 11
    CHECK_CASE_ERROR_UNKNOWN_TYPE = 12
    CHECK_CASE_ERROR_CONTAIN_NON_NUM = 13
    CHECK_CASE_ERROR_CONTAIN_NON_NAN = 14
    CHECK_CASE_ERROR_NUMS = 15
    CHECK_Y_ERROR_CONTAIN_VALUES = 16

    JACKKNIFE_WARN = 20

    def __init__(self):
        self.data = None
        self.n_case = 0
        self.rows = 1
        self.cols = 1
        self.jack_ok = True
        self.A = None
        self.S = None
        self.C = None
        self.D = None
        self.T = None
        self.SA = None
        self.CA = None
        self.DA = None
        self.TA = None
        self.dict = {}

    def calculate_pk(self, *, x_in=None, y_in=None, dataframe=None):
        state = self.check_case(x_in=x_in, y_in=y_in, dataframe=dataframe)
        if state != PK.ALL_CHECKS_OK:
            return state
        state = self.check_y()
        if state != PK.ALL_CHECKS_OK:
            return state
        self.check_x()
        self.construct_A()
        self.construct_S()
        self.construct_CDT()
        state = self.calculate()
        self.show_result()
        return state

    def check_case(self, *, x_in=None, y_in=None, dataframe=None):
        x = None
        y = None
        if dataframe is not None and isinstance(dataframe, pd.DataFrame):
            if len(dataframe.columns) < 2:
                return PK.CHECK_CASE_ERROR_DATA_FRAME_COLUMNS
            contain_xy = 0
            if 'x' in dataframe.columns:
                x = dataframe['x']
                contain_xy = contain_xy & 1
            if 'X' in dataframe.columns:
                x = dataframe['X']
                contain_xy = contain_xy & 1
            if 'y' in dataframe.columns:
                y = dataframe['y']
                contain_xy = contain_xy & 2
            if 'Y' in dataframe.columns:
                y = dataframe['Y']
                contain_xy = contain_xy & 2
            if contain_xy != 3:
                x = dataframe.iloc[:, 0]
                y = dataframe.iloc[:, 1]
        elif x_in is not None and y_in is not None:
            if isinstance(x_in, list) and isinstance(y_in, list):
                x = pd.Series(x_in)
                y = pd.Series(y_in)
            elif isinstance(x_in, pd.Series) and isinstance(y_in, pd.Series):
                x = x_in
                y = y_in
            else:
                return PK.CHECK_CASE_ERROR_XY_TYPE
        else:
            return PK.CHECK_CASE_ERROR_UNKNOWN_TYPE

        if x.apply(lambda n: not isinstance(n, (int, float))).any() or y.apply(
                lambda n: not isinstance(n, (int, float))).any():
            return PK.CHECK_CASE_ERROR_CONTAIN_NON_NUM
        if x.isna().any() or y.isna().any():
            return PK.CHECK_CASE_ERROR_CONTAIN_NON_NAN

        l1 = len(x)
        l2 = len(y)
        if l1 != l2 or l1 < 2:
            print("Not enough cases (rows) selected; need at least two.")
            return PK.CHECK_CASE_ERROR_NUMS
        self.n_case = l1
        self.data = pd.DataFrame({'x': x, 'y': y, 'k': range(self.n_case), 'Ry': [
            0] * self.n_case,
            'Cx': [0] * self.n_case, 'PKm': [0] * self.n_case})
        return PK.ALL_CHECKS_OK

    def check_y(self):
        self.data.sort_values('y', inplace=True)
        current = self.data.iloc[0, 1]
        category = 0
        for i in range(self.n_case):
            if current == self.data.iloc[i, 1]:
                self.data.iloc[i, 3] = category
            else:
                current = self.data.iloc[i, 1]
                category += 1
                self.data.iloc[i, 3] = category

        y = self.data.iloc[:, 1].tolist()
        self.jack_ok = True
        for i in set(y):
            if y.count(i) < 2:
                self.jack_ok = False

        self.rows = len(set(y))
        print("There are %d distinct y-values." % self.rows)
        if self.rows < 2:
            print("Only one distinct y-value; need at least two.")
            return PK.CHECK_Y_ERROR_CONTAIN_VALUES
        if self.rows > 2:
            self.jack_ok = True
        return PK.ALL_CHECKS_OK

    def check_x(self):
        self.data.sort_values('x', inplace=True)
        current = self.data.iloc[0, 0]
        category = 0
        for i in range(self.n_case):
            if current == self.data.iloc[i, 0]:
                self.data.iloc[i, 4] = category
            else:
                current = self.data.iloc[i, 0]
                category += 1
                self.data.iloc[i, 4] = category

        x = self.data.iloc[:, 0].tolist()
        self.cols = len(set(x))
        self.data.sort_values('k', inplace=True)

    def construct_A(self):
        self.A = np.zeros((self.rows, self.cols), dtype=int)
        for k in range(self.n_case):
            i = self.data.iloc[k, 3]
            j = self.data.iloc[k, 4]
            self.A[i, j] = self.A[i, j] + 1

    def construct_S(self):
        self.S = np.zeros((self.rows, self.cols), dtype=int)
        for i in range(self.rows):
            self.S[i, 0] = self.A[i, 0]
            for j in range(1, self.cols):
                self.S[i, j] = self.S[i, j - 1] + self.A[i, j]

    def construct_CDT(self):
        self.C = np.zeros((self.rows, self.cols), dtype=int)
        self.D = np.zeros((self.rows, self.cols), dtype=int)
        self.T = np.zeros((self.rows, self.cols), dtype=int)
        self.SA = np.zeros((self.rows, 2), dtype=int)
        self.CA = np.zeros((self.rows, 2), dtype=int)
        self.DA = np.zeros((self.rows, 2), dtype=int)
        self.TA = np.zeros((self.rows, 2), dtype=int)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.A[i, j] != 0:
                    for ai in range(self.rows):
                        if ai < i:
                            if j > 0:
                                self.C[i, j] = self.C[i, j] + self.S[ai, j - 1]
                            if j < self.cols - 1:
                                self.D[i, j] = self.D[i, j] + \
                                    self.S[ai, self.cols - 1] - self.S[ai, j]
                            self.T[i, j] = self.T[i, j] + self.A[ai, j]
                        elif ai > i:
                            if j < self.cols - 1:
                                self.C[i, j] = self.C[i, j] + \
                                    self.S[ai, self.cols - 1] - self.S[ai, j]
                            if j > 0:
                                self.D[i, j] = self.D[i, j] + self.S[ai, j - 1]
                            self.T[i, j] = self.T[i, j] + self.A[ai, j]
                    self.CA[i, 0] = self.CA[i, 0] + self.A[i, j] * self.C[i, j]
                    self.DA[i, 0] = self.DA[i, 0] + self.A[i, j] * self.D[i, j]
                    self.TA[i, 0] = self.TA[i, 0] + self.A[i, j] * self.T[i, j]
                    self.CA[1, 1] = self.CA[1, 1] + \
                        self.A[i, j] * self.C[i, j] * self.C[i, j]
                    self.DA[1, 1] = self.DA[1, 1] + \
                        self.A[i, j] * self.D[i, j] * self.D[i, j]
                    self.TA[1, 1] = self.TA[1, 1] + \
                        self.A[i, j] * self.C[i, j] * self.D[i, j]
                else:
                    pass
            self.SA[0, 0] = self.SA[0, 0] + self.S[i, self.cols - 1]
            self.CA[0, 1] = self.CA[0, 1] + self.CA[i, 0]
            self.DA[0, 1] = self.DA[0, 1] + self.DA[i, 0]
            self.TA[0, 1] = self.TA[0, 1] + self.TA[i, 0]

    def calculate(self):
        self.dict.update({'n': self.SA[0, 0]})
        self.dict.update({'Qc': self.CA[0, 1]})
        self.dict.update({'Qd': self.DA[0, 1]})
        self.dict.update({'Qtx': self.TA[0, 1]})
        self.dict.update({'Qcdt': self.dict.get('Qc') +
                         self.dict.get('Qd') + self.dict.get('Qtx')})
        self.dict.update(
            {'dyx': (self.dict.get('Qc') - self.dict.get('Qd')) / self.dict.get('Qcdt')})
        self.dict.update({'PK': (self.dict.get('dyx') + 1) / 2})

        self.dict.update({'Qcc': self.CA[1, 1]})
        self.dict.update({'Qdd': self.DA[1, 1]})
        self.dict.update({'Qcd': self.TA[1, 1]})
        self.dict.update({'Term1': self.dict.get('Qcc') - 2 *
                         self.dict.get('Qcd') + self.dict.get('Qdd')})
        self.dict.update({'Term2': 0})
        self.dict.update({'Term3': 0})

        for i in range(self.rows):
            ni = self.S[i, self.cols - 1]
            Qci = self.CA[i, 0]
            Qdi = self.DA[i, 0]
            self.dict.update({'Term2': self.dict.get(
                'Term2') + (self.dict.get('n') - ni) * (Qci - Qdi)})
            self.dict.update({'Term3': self.dict.get(
                'Term3') + ni * (self.dict.get('n') - ni) * (self.dict.get('n') - ni)})
        self.dict.update(
            {'Term2': -2 * self.dict.get('dyx') * self.dict.get('Term2')})
        self.dict.update({'Term3': self.dict.get('dyx') *
                         self.dict.get('dyx') * self.dict.get('Term3')})

        import math
        self.dict.update({'SE1': math.sqrt(self.dict.get(
            'Term1') + self.dict.get('Term2') + self.dict.get('Term3')) / self.dict.get('Qcdt')})
        self.dict.update({'SE0': math.sqrt(self.dict.get('Term1') - (self.dict.get('Qc') - self.dict.get('Qd'))
                         * (self.dict.get('Qc') - self.dict.get('Qd')) / self.dict.get('n')) / self.dict.get('Qcdt')})

        if not self.jack_ok:
            print(
                "Can't do jackknife; for two-level y; need at least two cases for each level.")
            return PK.JACKKNIFE_WARN
        else:
            self.dict.update({'SPKm': 0})
            self.dict.update({'SSPKm': 0})

            for k in range(self.n_case):
                i = self.data.iloc[k, 3]
                j = self.data.iloc[k, 4]
                Crc = self.C[i, j]
                Drc = self.D[i, j]
                Trc = self.T[i, j]
                Qcm = self.dict.get('Qc') - 2 * Crc
                Qdm = self.dict.get('Qd') - 2 * Drc
                Qtxm = self.dict.get('Qtx') - 2 * Trc
                Qcdtm = Qcm + Qdm + Qtxm
                PKm = (Qcm + Qtxm / 2) / Qcdtm
                self.data.iloc[k, 5] = PKm
                self.dict.update({'SPKm': self.dict.get('SPKm') + PKm})
                self.dict.update({'SSPKm': self.dict.get('SSPKm') + PKm * PKm})

            self.dict.update({'PKj': self.n_case *
                              self.dict.get('PK') -
                              (self.n_case -
                               1) *
                              (self.dict.get('SPKm')) /
                              self.n_case})
            self.dict.update({'SEj': math.sqrt((self.n_case - 1) * (self.dict.get('SSPKm') -
                             self.dict.get('SPKm') * self.dict.get('SPKm') / self.n_case) / self.n_case)})
        return PK.ALL_CALCULATION_OK

    def show_result(self):
        print("The result is as following :")
        print("PK is %.3f" % self.dict.get("PK"))
        print("SE0 is %.3f" % self.dict.get("SE0"))
        print("SE1 is %.3f" % self.dict.get("SE1"))
        if self.jack_ok:
            print("PKj is %.3f" % self.dict.get("PKj"))
            print("SEj is %.3f" % self.dict.get("SEj"))
            self.data['PKm'] = self.data['PKm'].map(lambda x: format(x, '.3f'))
        else:
            self.data.drop(labels="PKm", axis=1, inplace=True)
        print("All the data matrix :")
        print("Original")
        print(self.data)
        print("Aij")
        print(self.A)
        print("Sij")
        print(self.S)
        print("Sij Assist")
        print(self.SA)
        print("Cij")
        print(self.C)
        print("Cij Assist")
        print(self.CA)
        print("Dij")
        print(self.D)
        print("Dij Assist")
        print(self.DA)
        print("Tij")
        print(self.T)
        print("Tij Assist")
        print(self.TA)


if __name__ == "__main__":
    # x = [1,1,2,1,2,2,3,3]
    # y = [1,1,2,1,2,2,3,3]
    x = [0, 0, 0, 0, 0, 0]  # , 1, 1, 2]
    y = [1, 1, 1, 1, 1, 2]  # , 3, 3, 4]
    pk = PK()
    pk.calculate_pk(x_in=x, y_in=y)
