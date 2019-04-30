import math as m
import csv


def containsZeroes(values):
    '''Return True if a list contains a 0, return False else.'''

    result = False
    for element in values:
        if element == 0:
            result = True

    return result


def allTheSame(somevalues):
    '''Return True if all somevalues of a list are the same, return False else.'''

    result = True
    for n in range(0, len(somevalues) - 1):
        if somevalues[n] != somevalues[n + 1]:
            result = False

    return result


def listifyUncertainties(error, samplesize):
    '''Return a list of the length samplesize filled with errors.'''

    if type(error) is type([]):

        if samplesize != len(error):
            raise Exception('Oups, the values and samplesize lists are supposed to be of the same length')
        else:
            return error
    else:
        errors = []
        for n in range(samplesize):
            errors.append(float(error))
        return errors


def weighedDeviation(errors):
    '''Return weighed standard deviation as float.'''

    total = 0
    for value in errors:
        total += (1 / (value**2))

    return float(len(errors) / total)


def weighedAverageDeviation(errors):
    '''Return weighed standard deviation as float.'''

    total = 0
    for value in errors:
        total += (1 / (value**2))

    return m.sqrt(1 / total)


def normalAverage(values, errors):
    '''Return the non weighted average and it`s uncertainty as floats in a dictonary.'''
    samplesize = len(values)

    # Lets calculate the uncertainty.
    error = errors[0] / samplesize

    # And now for the main part:
    total = 0
    for value in values:
        total += value
    average = total / samplesize

    # We want to return a dictonary ... cause you know its two values.
    result = {'average': float(average), 'uncertainty': float(error)}

    return result


def weightedAverage(values, errors):
    '''Return the weighted (1/(sigma/N)^2) average and it's approximate uncertainty in as floats in a dictonary'''
    samplesize = len(values)
    if samplesize != len(errors):
        raise Exception('Oups, the values and errors lists are supposed to be of the same length')

    # If there is a 0 in errors, return normalAverage() since we can't devide by 0!
    if containsZeroes(errors) or allTheSame(errors):
        return normalAverage(values, errors)

    # use the weighed deviation as uncertainty
    error = weighedAverageDeviation(errors)

    total = 0
    for n in range(samplesize):
        weighted = values[n] * (1 / (errors[n]**2))
        total += weighted

    divideBy = 0
    for n in range(samplesize):
        divideBy += (1 / (errors[n]**2))

    # We want to return a dictonary ... cause you know its two values.
    result = {'average': float(total / divideBy), 'uncertainty': float(error)}

    return result


def squaredAverage(values, errors):
    '''Return the weighted (1/(sigma/N)^2) average as integer.'''
    samplesize = len(values)
    if samplesize != len(errors):
        raise Exception('Oups, the values and errors lists are supposed to be of the same length')

    squaredValues = []
    for n in range(samplesize):
        squaredValues.append(values[n]**2)

    return weightedAverage(squaredValues, errors)


def xyAverage(xvalues, yvalues, yerrors):
    '''Return the weighted (1/(sigma/N)^2) average as integer.'''

    # First make sure all the lists are of the same length.
    samplesize = len(xvalues)
    if samplesize != len(yvalues):
        raise Exception('Oups, the xvalues and yvalues lists are supposed to be of the same length')
    if yerrors:
        if samplesize != len(yerrors):
            raise Exception('Oups, the xvalues and yvalues lists are supposed to be of the same length')

    # Then do the necessary precalculations.
    values = []
    for n in range(samplesize):
        values.append(xvalues[n] * yvalues[n])

    return weightedAverage(values, yerrors)


def averageSquared(uncertaintyDictonary):
    '''Return the squared average and it's properly calculated uncertainty as floats in a dictonary.'''

    result = {'average': uncertaintyDictonary['average']**2,
              'uncertainty': 2 * uncertaintyDictonary['average'] * uncertaintyDictonary['uncertainty']}

    return result


def slope(xvalues, yvalues, yerrors):
    '''Return slope m and it's uncertainty as float'''

    xAverage = weightedAverage(xvalues, yerrors)['average']
    yAverage = weightedAverage(yvalues, yerrors)['average']
    xSquaredAverage = squaredAverage(xvalues, yerrors)['average']
    xAverageSquared = averageSquared(weightedAverage(xvalues, yerrors))['average']
    multiAverage = xyAverage(xvalues, yvalues, yerrors)['average']
    resultingSlope = (multiAverage - xAverage * yAverage) / (xSquaredAverage - xAverageSquared)

    if allTheSame(yerrors):
        error = yerrors[0]**2
    else:
        error = weighedDeviation(yerrors)**2

    samplesize = float(len(xvalues))
    uncertainty = error / (samplesize * (xSquaredAverage - xAverageSquared))

    return {'result': resultingSlope, 'uncertainty': uncertainty}


def yAxisSection(xvalues, yvalues, yerrors):
    '''Return y-axis section n and it's uncertainty as float'''

    xAverage = weightedAverage(xvalues, yerrors)['average']
    yAverage = weightedAverage(yvalues, yerrors)['average']
    xSquaredAverage = squaredAverage(xvalues, yerrors)['average']
    m = slope(xvalues, yvalues, yerrors)['result']
    mUncertainty = slope(xvalues, yvalues, yerrors)['uncertainty']

    resultingSection = yAverage - (m * xAverage)
    uncertainty = mUncertainty * xSquaredAverage

    return {'result': resultingSection, 'uncertainty': uncertainty}


def printLinearFit(xvalues, yvalues, yerrors, precision=3, presentationType='f', saveToPath=False):
    '''Use the predefined functions to print (and optionally save) a linear fit.'''

    # Make sure yerror is an array, if n,ot create one.
    yerrors = listifyUncertainties(yerrors, len(xvalues))

    # Populate dictonary with results of the averages.
    averages = {
        'X-Durchschnitt:': weightedAverage(xvalues, yerrors),
        'Y-Durchschnitt:': weightedAverage(yvalues, yerrors),
        'XY-Durchschnitt:': xyAverage(xvalues, yvalues, yerrors),
        'X^2-Durchschnitt:': squaredAverage(xvalues, yerrors),
        'X-Durchschnitt^2:': averageSquared(weightedAverage(xvalues, yerrors)),
    }

    # Populate dictonary with results of the fit.
    fit = {
        'Steigung:': slope(xvalues, yvalues, yerrors),
        'Y-Achsenabschnitt:': yAxisSection(xvalues, yvalues, yerrors)
    }

    # Print averages ...
    print("GEWICHTETE DURCHSCHNITTSWERTE:")

    # ... and save if path is specified.
    if saveToPath:
        with open(saveToPath, 'w') as textFile:
            print("GEWICHTETE DURCHSCHNITTSWERTE:", file=textFile)

    for key, value in averages.items():
        template = "{0:<20}" + " {1:<8." + str(precision) + str(presentationType) + "} +/- {2:<8." + str(precision) + str(presentationType) + "}"
        print(template.format(key, value['average'], value['uncertainty']))

        if saveToPath:
            with open(saveToPath, 'a') as textFile:
                print(template.format(key, value['average'], value['uncertainty']), file=textFile)

    # Print/save newline for formatting.
    print()
    if saveToPath:
        with open(saveToPath, 'a') as textFile:
            print("", file=textFile)

    # Print fit ...
    print("GEFITTETE GERADE:")

    # ... and save if path is specified.
    if saveToPath:
        with open(saveToPath, 'a') as textFile:
            print("GEFITTETE GERADE:", file=textFile)

    for key, value in fit.items():
        template = "{0:<20}" + " {1:<8." + str(precision) + str(presentationType) + "} +/- {2:<8." + str(precision) + str(presentationType) + "}"
        print(template.format(key, value['result'], value['uncertainty']))

        if saveToPath:
            with open(saveToPath, 'a') as textFile:
                print(template.format(key, value['result'], value['uncertainty']), file=textFile)


def isValue(input):
    '''Return input as float if it is a number, return None else'''

    try:
        number = float(input)
        return number
    except:
        return None


def readFromFile(path):
    '''Return lists of values from provided file.'''

    # Import data to list of tuples (one per line).
    with open(path) as file:
        next(file)   # Skip first line.
        data = [tuple(line) for line in csv.reader(file, delimiter=" ")]  # Populate line.

    # Let's handle the y-uncertainties:
    if len(data[0]) == 2:  # If none are provided.
        yerrors = None
    else:
        try:  # If a list is provided.
            test = data[1][2]
            yerrors = [isValue(element[2]) for element in data]
        except:  # if only one value is provided.
            yerrors = listifyUncertainties(isValue(data[0][2]), len(data))

    # populate the x and y values
    xvalues = [isValue(element[0]) for element in data]
    yvalues = [isValue(element[1]) for element in data]

    if yerrors:
        return xvalues, yvalues, yerrors
    else:
        return xvalues, yvalues
