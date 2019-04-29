# First import the functions.
from LinFit import (readFromFile, printLinearFit)

# Using it is as easy as first importing the values
xvalues, yvalues, yerrors = readFromFile('input2.txt')

# If necessary you can modify them, they are normal lists.
# The uncertainties can be provided as float (for one shared uncertainty) or as list (for indidual uncertainties).
# yvalues = [1.1, 2.2, 3.2]
# yerrors = 0.5

# 3 is the precision, 'g' is an "intelligent" presentation types, for simple rounding use 'f'. For more info see: http://bit.ly/2UQa3Z6
printLinearFit(xvalues, yvalues, yerrors, 3, 'g')

# Saves the result to 'output.txt' in the same folder as the script. Will create file if not existent.
# printLinearFit(xvalues, yvalues, yerrors, 3, 'g', 'output.txt')
