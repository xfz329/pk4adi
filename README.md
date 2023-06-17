# pk4adi

## Project Information

The package's name pk4adi is short for "PK for anesthetic depth indicators". The PK (Prediction probability) was firstly proposed by [Docor Warren D. Smith](https://www.csus.edu/faculty/s/smithwd/) in the paper [Measuring the Performance of Anesthetic Depth Indicators](https://pubs.asahq.org/anesthesiology/article/84/1/38/35261/Measuring-the-Performance-of-Anesthetic-Depth) in 1996. Docor Warren D. Smith and his team provide a tool to calculate PK writen using the xls macro language.

Our team provide a reimplementation of the PK tools developed using the Python language with easy using apis in this package. The project is fully open source in the [github](https://github.com/xfz329/pk). The lastest version 0.1.0 released on June 17, 2023. 

Please feel free to contact us(silencejiang@zju.edu.cn). Any kind of feedbacks is welcomed. You could report any bugs or issues when using pk4adi in the github [project](https://github.com/xfz329/pk/issues).

Specially, a gui version of pk4adi is under development. We will also open source the gui version project.

## Changelogs

Please refer the [changelog.md](https://github.com/xfz329/pk/blob/main/CHANGELOG.md) for details.

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
calculate_pk(x_in , y_in):

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
compare_pks(pk1, pk2):

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

The best way to use this package is using the Python scripts.

### 1. calculate PK

```python
from pk4adi.pk import calculate_pk

x = [ 0, 0, 0, 0, 0, 0]
y = [ 1, 1, 1, 1, 1, 2]

pk = PK()
pk.calculate_pk(x_in=x, y_in=y)
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

pk1 = calculate_pk(x_in = x1, y_in = y1)

x2 = [ 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6 ]
y2 = [ 1, 1, 2, 1, 1, 2, 1, 2, 3, 3, 2, 2, 1, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 2 ]

pk2 = calculate_pk(x_in = x2, y_in = y2)

ans = compare_pks(pk1, pk2)
```
You will get the following output.
```
==============
PK calculation
==============

   PK    SE0    SE1  jack_ok      PKj    SEj
-----  -----  -----  ---------  -----  -----
0.867  0.065  0.066  True       0.866  0.070


==============
PK calculation
==============

   PK    SE0    SE1  jack_ok      PKj    SEj
-----  -----  -----  ---------  -----  -----
0.798  0.073  0.068  True       0.799  0.073


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

# Development

## Contribute

Please feel free to contact us(silencejiang@zju.edu.cn). Any kind of feedbacks is welcomed and appreciated.
- Check out the wiki for development info (coming soon!).
- Fork us from @xfz329's [main](https://github.com/xfz329/pk).
- Report an issue [here](https://github.com/xfz329/pk/issues).
- Report a bug with data.

## References
1. [Measuring the Performance of Anesthetic Depth Indicators](https://pubs.asahq.org/anesthesiology/article/84/1/38/35261/Measuring-the-Performance-of-Anesthetic-Depth)
2. [A measure of association for assessing prediction accuracy that is a general](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-0258(19960615)15:11%3C1199::AID-SIM218%3E3.0.CO;2-Y)
3. [Excel 4.0 Macro Functions Reference - My Online Training Hub](https://d13ot9o61jdzpp.cloudfront.net/files/Excel%204.0%20Macro%20Functions%20Reference.pdf)

