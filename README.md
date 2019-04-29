# LinFit

## Description

### Englisch
Naive and easy to understand Python script that calculates a linear-fit (with y-uncertainties) for a provided list of values. It's based on the instructions provided by the experiment-manual from the course [physik261](https://www.praktika.physik.uni-bonn.de/module/physik261) of the Department of Physics and Astronomy at the [Rheinische Friedrich-Wilhelms-Universität Bonn](https://www.uni-bonn.de).

The Script is designed to be be as simple as possible. Computation time was no concern, as the measured data of the experiments is pretty small. It should be fully understandable after having sucessfully completed the Python part of Informatics for Physicist ([physik131](https://www.brock.physik.uni-bonn.de/teaching-1/physik131-edv-fur-physiker-ws-1516)) in the first semester. 

### Deutsch
Einfaches und naives Skript zum berechnen eines Geradenfit. Das Skript basiert auf den Formeln aus dem Praktikumshandbuch des [Physikalischen Praktikum 1](https://www.praktika.physik.uni-bonn.de/module/physik261) des Physikalischen Instituts an der [Rheinische Friedrich-Wilhelms-Universität Bonn](https://www.uni-bonn.de).

Das Skript wurde so simpel wie möglich ausgelegt. Rechenzeit wurde bei der Implementierung der Berechnungen nicht berücksichtigt, da die Anzahl der Messwerte während des ersten Praktikums noch recht gering ist. Stattdessen wurde bewusst auf die Nutzung von Modulen wie NumPy oder SciPy verzichtet, um das Skript so lesbar wie möglich zu halten. Mit den Python-Kenntnissen aus dem Kurs EDV für Physiker ([physik131](https://www.brock.physik.uni-bonn.de/teaching-1/physik131-edv-fur-physiker-ws-1516)) aus dem ersten Semester sollte es möglich sein das Skript zu verstehen und (wenn nötig) zu modifizieren.

## Usage

The file `LinFit.py` contains the functions of the script. Usage is as simple as:

```python
from LinFit import (readFromFile, printLinearFit)

# First import the values ...
xvalues, yvalues, yerrors = readFromFile('input.txt')

# ... then use them to calculate the linear fit.
printLinearFit(xvalues, yvalues, yerrors, 3, 'g')

# Additionally save the result to 'output.txt' in the same folder as the script. Will create file if not existent.
printLinearFit(xvalues, yvalues, yerrors, 3, 'g', 'output.txt')
```

The result will be printed and/or saved in the format:

```text
GEWICHTETE DURCHSCHNITTSWERTE:
X-Durchschnitt:      105      +/- 0.5     
Y-Durchschnitt:      20.9     +/- 0.5     
XY-Durchschnitt:     2.2e+03  +/- 0.5     
X^2-Durchschnitt:    1.58e+04 +/- 0.5     
X-Durchschnitt^2:    1.1e+04  +/- 105     

GEFITTETE GERADE:
Steigung:            0.00115  +/- 6.61e-06
Y-Achsenabschnitt:   20.8     +/- 0.104
```

The script will use weighed averages (and corresponding uncertainty analysis) automatically if provided with a list of individual y-uncertainties. The `'g'` option set's the presentation type of the output from `printLinearFit()`. Other options can be found in the [documentation](https://docs.python.org/2/library/string.html#formatstrings) for Format Specification Mini-Language. The integer `'3'` set's the precision of the output.

