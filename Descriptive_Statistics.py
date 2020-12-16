import numpy as np
import pandas as pd
import re
from pandas.api.types import is_numeric_dtype


def read(path):
    if re.search('csv$', path):
        return pd.read_csv(path)
    elif re.search('xlsx$', path) or re.search('xls$', path):
        return pd.read_excel(path)
    else:
        raise FileNotFoundError("The specified path doesn't exist or this data type is not supported.")


def count(data):
    counts = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            counts.append(len(data[i]))
        else:
            counts.append("Not numeric.")
    return counts


def mean(data):
    means = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            means.append(data[i].sum()/len(data[i]))
        else:
            means.append("Not numeric.")
    return means


def std(data):
    stds = []
    means = mean(data)
    for i in range(len(data.columns)):
        if is_numeric_dtype(data.iloc[:,i]):
            sum_ = 0
            for j in data.iloc[:,i]:
                sum_ += (j - means[i])**2
            stds.append(np.sqrt(sum_/(len(data.iloc[:,i])-1)))
        else:
            stds.append("Not numeric.")
    return stds



def minimum(data):
    mins = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            mins.append(min(data[i]))
        else:
            mins.append("Not numeric.")
    return mins


def maximum(data):
    maxs = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            maxs.append(max(data[i]))
        else:
            maxs.append("Not numeric.")
    return maxs



def quantile(vec,q):
    vec = sorted(vec)
    q = q/100
    i = q*(len(vec))
    j = int(i)
    return(vec[j-1])


def quantile_25(data):
    quantiles_25 = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            quantiles_25.append(quantile(data[i], 25))
        else:
            quantiles_25.append("Not numeric.")
    return quantiles_25


def quantile_50(data):
    quantiles_50 = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            quantiles_50.append(quantile(data[i], 50))
        else:
            quantiles_50.append("Not numeric.")
    return quantiles_50



def quantile_75(data):
    quantiles_75 = []
    for i in data.columns:
        if is_numeric_dtype(data[i]):
            quantiles_75.append(quantile(data[i], 75))
        else:
            quantiles_75.append("Not numeric.")
    return quantiles_75



def descriptive(data):
    statistics = pd.DataFrame(columns= data.columns, index = ('count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'))
    statistics.loc['count'] = count(data)
    statistics.loc['mean'] = mean(data)
    statistics.loc['std'] = std(data)
    statistics.loc['min'] = minimum(data)
    statistics.loc['max'] = maximum(data)
    statistics.loc['25%'] = quantile_25(data)
    statistics.loc['50%'] = quantile_50(data)
    statistics.loc['75%'] = quantile_75(data)
    return statistics