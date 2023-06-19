# pk4adi

## Project Information

The package's name pk4adi is short for "PK for anesthetic depth indicators". The PK (Prediction probability) was first proposed by [Dr. Warren D. Smith](https://www.csus.edu/faculty/s/smithwd/) in the paper [Measuring the Performance of Anesthetic Depth Indicators](https://pubs.asahq.org/anesthesiology/article/84/1/38/35261/Measuring-the-Performance-of-Anesthetic-Depth) in 1996. Dr. Warren D. Smith and his team provide a tool to calculate PK written using the MS Excel macro language.

Our team provide a reimplementation of the PK tools developed using the Python language with easy-to-use APIs in this package. The project is fully open source on [github](https://github.com/xfz329/pk4adi). The latest released version could be found [here](https://github.com/xfz329/pk4adi/releases). 

A GUI version of pk4adi called pk4adi_gui is also under development. This project is also open source on [github](https://github.com/xfz329/pk4adi_gui).

Please feel free to contact us (silencejiang@zju.edu.cn). Any kind of feedback is welcome. You could report any bugs or issues when using pk4adi on github [project](https://github.com/xfz329/pk4adi/issues).

## Changelogs

Please refer the [changelog.md](https://github.com/xfz329/pk4adi/blob/main/CHANGELOG.md) for details.

## Requirements

### Python

```
Python 3.8 or greater.
```

### Packages

```
pandas>=0.18.0
numpy>=1.21.6
scipy>=1.9.0
tabulate
```

## Install

To install pk4adi, run the following in the command prompt.
```
pip install pk4adi
```

## APIs

1. calculate_pk of module pk.py.
```
calculate_pk(x_in , y_in , auto_print = True):

Compute the pk value to Measure the Performance of Anesthetic Depth Indicators.
print_pk() will be called before returning ans by default.

Parameters
----------
x_in : a list or a pandas series (pandas.Series()).
    Indicator.
y_in : a list or a pandas series (pandas.Series()).
    State.
auto_print : bool.
    Whether to print the ans before returning it or not.

Returns
-------
ans : a dict.
    A dict containing all the matrix and variables involved.
    Use the script 'print(ans.keys())' to get the details.
    The most important variables have already been printed.
```
2. print_pk of module pk.py.
```
print_pk(result, floatfmt=".3f", tablefmt='simple'):

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

```   
3. compare_pks of module pkc.py.
```
compare_pks(pk1, pk2 , auto_print = True):

Compare two answers of the pk values, which is the output of the function calculate_pk().
print_pks() will be called before returning ans by default.

Parameters
----------
pk1 : a dict.
    The output of the function calculate_pk().
pk2 : a dict.
    The output of the function calculate_pk().
auto_print : bool.
    Whether to print the ans before returning it or not.

Returns
-------
ans : a dict.
    A dict containing all the matrix and variables involved.
    Use the script 'print(ans.keys())' to get the details.
    Specially, the P values and the interval it located will be
    calculated using the scipy.stats packages.
    The most important variables have already been printed.
```
4. print_pks of module pkc.py.
```
print_pks(result, floatfmt=".3f", tablefmt='simple'):

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
```

## Examples

The best way to use this package is to use Python scripts.

### 1. calculate PK

```python
from pk4adi.pk import calculate_pk

x = [ 0, 0, 0, 0, 0, 0]
y = [ 1, 1, 1, 1, 1, 2]
calculate_pk(x, y)

x = [0, 0, 0, 0, 0, 0, 1, 1, 2]
y = [1, 1, 1, 1, 1, 2, 3, 3, 4]
calculate_pk(x, y)
```
You will get the following output.
```
==============
PK calculation
==============

   PK    SE0    SE1  jack_ok      PKj    SEj
-----  -----  -----  ---------  -----  -----
0.500  0.000  0.000  False        nan    nan


==============
PK calculation
==============

   PK    SE0    SE1  jack_ok      PKj    SEj
-----  -----  -----  ---------  -----  -----
0.900  0.124  0.085  True       0.901  0.117
```

### 2. compare results of PK

```python
from pk4adi.pk import calculate_pk
from pk4adi.pkc import compare_pks

x1 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
y1 = [ 1, 1, 1, 1, 1, 2, 1, 1, 3, 3, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3 ]

pk1 = calculate_pk(x_in = x1, y_in = y1 , auto_print = False)

x2 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
y2 = [ 1, 1, 2, 1, 1, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 2 ]

pk2 = calculate_pk(x_in = x2, y_in = y2 , auto_print = False)

ans = compare_pks(pk1, pk2)
```
You will get the following output.
```
==============
PKs comparison
==============

=================
For Group (z-test)
=================

  PKD    SED     ZD    P value  Comment
-----  -----  -----  ---------  ---------
0.068  0.101  0.669      0.504  P > 0.05


=================
For Pair (t-test)
=================

  PKDJ    SEDJ    DF     TD    P value  Comment
------  ------  ----  -----  ---------  ---------
 0.030   0.066    23  0.453      0.327  P > 0.05
```

### 3. more details
You could get the all the matrix and variables in the returned dicts of the function calculate_pk() and compare_pks().
```python
print(pk1.keys())
print(ans.keys())
```
You will get the following output.
```
dict_keys(['type', 'A', 'S', 'C', 'D', 'T', 'SA', 'CA', 'DA', 'TA', 'jack_ok', 'n_case', 'n', 'Qc', 'Qd', 'Qtx', 'Qcdt', 'dyx', 'PK', 'Qcc', 'Qdd', 'Qcd', 'Term1', 'Term2', 'Term3', 'SE1', 'SE0', 'PKm', 'SPKm', 'SSPKm', 'PKj', 'SEj'])
dict_keys(['type', 'n_case', 'PKD', 'SED', 'ZD', 'ZP', 'ZJ', 'PKmD', 'SumD', 'SSD', 'DF', 'PKDJ', 'SEDJ', 'TD', 'TP', 'TJ'])
```
Then just get the value with the key of the dict!

# Development

## Contribute

Please feel free to contact us (silencejiang@zju.edu.cn). Any kind of feedback is welcome and appreciated.
- Check out the wiki for development info (coming soon!).
- Fork us from @xfz329's [main](https://github.com/xfz329/pk4adi) and star us.
- Report an issue or a bug with data [here](https://github.com/xfz329/pk4adi/issues).
- Any other free discussion [here](https://github.com/xfz329/pk4adi/discussions).

## References
1. [Measuring the Performance of Anesthetic Depth Indicators](https://pubs.asahq.org/anesthesiology/article/84/1/38/35261/Measuring-the-Performance-of-Anesthetic-Depth)
2. [A measure of association for assessing prediction accuracy that is a generalization of non-parametric ROC area](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-0258(19960615)15:11%3C1199::AID-SIM218%3E3.0.CO;2-Y)
3. [Excel 4.0 Macro Functions Reference - My Online Training Hub](https://d13ot9o61jdzpp.cloudfront.net/files/Excel%204.0%20Macro%20Functions%20Reference.pdf)
4. [scipy.stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)
5. [scipy.stats.t](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)
