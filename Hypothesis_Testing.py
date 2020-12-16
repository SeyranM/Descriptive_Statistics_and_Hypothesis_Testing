import numpy as np
from scipy.stats import t, f, chi2



# One-tailed critical value.
def critical_value(degrees_of_freedom, alpha):
    cv = t.ppf(1 - alpha, degrees_of_freedom)
    return cv
# Calculating Test Statistics.
def test_statistics_single_sample(data, mu):
    ts = (np.mean(data) - mu)/(np.std(data)/np.sqrt(len(data)-1))
    return ts
# Calculating P-Value
def one_tail_p_val(test_statistics, df):
    p = (1.0 - t.cdf(abs(test_statistics), df))
    return p

# Hypothesis Testing.
def hypothesis_testing_single_sample(data, mu, alpha, tail = 'two-tail'):
    ts = test_statistics_single_sample(data, mu)
    df = len(data) - 1
    p_value = one_tail_p_val(ts, df) * 2
    if tail == 'two-tail':
        cv = critical_value(df, alpha/2)
    elif tail == 'upper-tail':
        cv = critical_value(df, alpha)
    elif tail == 'lower-tail':
        cv = -critical_value(df, alpha)
    else:
        raise NameError('tail must be two-tail, upper-tail or lower-tail')
    
    print("Test Statitsics: "+str(ts))
    print("Critical Value: "+str(cv))
    print("P-Value: "+str(p_value))
        
    if tail == 'two-tail' and (ts > cv or ts < -cv):
        print("We reject the null hypothesis that the mean is equal to %.f." % (mu))
    elif tail == 'upper tail' and ts > cv:
        print("We reject the null hypothesis that the mean is equal to %.f." % (mu))
    elif tail == 'lower-tail' and ts < cv:
        print("We reject the null hypothesis that the mean is equal to %.f." % (mu))
    else:
        print("We can't reject the null hypothesis that the mean is equal to %.f." % (mu))



# Calculating Test Statistics.
def test_statistics_independent_samples(data1, data2):
    #standard error of difference
    se1 = np.std(data1)/np.sqrt(len(data1)-1)
    se2 = np.std(data2)/np.sqrt(len(data2)-1)
    sd = np.sqrt(se1**2 + se2**2)
    ts = (np.mean(data1) - np.mean(data2)) / sd
    return ts



# Hypothesis Testing.
def hypothesis_testing_independent_samples(data1, data2, alpha):
    ts = test_statistics_independent_samples(data1, data2)
    df = len(data1) + len(data2) - 2
    cv = critical_value(df, alpha)
    p_value = one_tail_p_val(ts, df) * 2
    print("Test Statitsics: "+str(ts))
    print("Critical Value: "+str(cv))
    print("P-Value: "+str(p_value))
    if np.abs(ts) < cv:
        print("We can't reject the null hypothesis that the means are equal.")
    else:
        print("We reject the null hypothesis that the means are equal.")



def pearson(x,y,alpha):
    df = len(x) + len(y) - 2
    numerator = 0
    for i in range(len(x)):
        numerator += (x[i] - np.mean(x))*(y[i] - np.mean(y))
    denominator_x = 0 
    for i in x:
        denominator_x += (i - np.mean(x))**2
    denominator_y = 0 
    for i in y:
        denominator_y += (i-np.mean(y))**2
    r = numerator / np.sqrt(denominator_x*denominator_y)
    ts = t_stat_two(r,df)
    cv = two_tail_cv(alpha,df)
    p = two_tail_p(ts,df)
    print("R coefficient = " + str(r) + "\nTest Statistics = " + str(ts) + "\nCritical value = " + str(cv) + "\nP-value = " + str(p))
    if p < alpha or r > 1:
        print("Reject the null hypothesis that the two samples are independent")
    else:
        print("We can't reject the null hypothesis that the two samples are independent")



def t_stat_two(r,df):
        t_stat = (r/np.sqrt(1-r**2))*np.sqrt(df)
        return t_stat


def two_tail_cv(alpha,df):
            cv = t.ppf(1-alpha/2,df)
            return cv



def two_tail_p(t_stat,df):
            p = (1 - t.cdf(abs(t_stat), df))*2
            return p


# ANOVA testing
def anova(data, alpha):
    df_between = len(data.columns) - 1
    df_within = data.count().sum() - len(data.columns)
    F_critical = f.ppf(1 - alpha, df_between, df_within)
    grand_mean = sum(np.mean(data)) / len(np.mean(data))
    ss_between = 0
    for i in range(len(data.columns)):
        ss_between += ((np.mean(data[data.columns[i]])-grand_mean)**2)*data[data.columns[i]].count()
    ss_total = 0
    for i in range(len(data.columns)):
        for j in data.iloc[:,i]:
                ss_total += (j -grand_mean )**2
    ss_within = ss_total-ss_between
    ms_between = ss_between/df_between
    ms_within = ss_within/df_within
    F = ms_between / ms_within
    p_value = (1.0 - f.cdf(F, df_between, df_within))
    print("Test Statitsics: "+str(F))
    print("Critical Value: "+str(F_critical))
    print("P-Value: "+str(p_value))
    if(F < F_critical):
        print("Fail to reject the null hypothesis, that the means are equal")
    else:
        print("Null hypothesis is rejected")


# Jarque-Bera
def jb_statistics(array):
    sk = skewness(array)
    ks = kurtosis(array)
    JB = len(array) * (((sk**2)/6)+((ks - 3)**2)/24)
    return JB


def skewness(array):
    sum_1 = 0
    sum_2 = 0
    for i in array:
        sum_1 += (i - np.mean(array))**3
    for i in array:
        sum_2 += (i - np.mean(array))**2
    sk = (((1/len(array))*sum_1)/np.power((1/len(array))*sum_2,(3/2)))
    return sk


def kurtosis(array):
    sum_1 = 0
    sum_2 = 0
    for i in array:
        sum_1 += (i - np.mean(array))**4
    for i in array:
        sum_2 += (i - np.mean(array))**2
    ks = ((1/len(array))*sum_1)/(((1/len(array))*sum_2)**2)
    return ks


def jb_p_value(test_statistics):
    p = 1 - chi2.cdf(test_statistics, 2)
    return p


def hypothesis_testing_jarque_bera(data, alpha):
    JB = jb_statistics(data)
    p = jb_p_value(JB)
    cv = chi2.ppf(1-alpha, 2)
    print("Test Statitsics: "+str(JB))
    print("Critical Value: "+str(cv))
    print("P-Value: "+str(p))
    if p > alpha:
        print("Fail to reject the null hypothesis, that the sample data is not significantly different than a normal population.")
    else:
        print("Reject the null hypothesis, that the sample data is not significantly different than a normal population.")