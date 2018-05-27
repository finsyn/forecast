# technical analysis utility functions 
import numpy as np

def rlog(x, y):
    return np.log(x/y) #Log return 

# Variable A is number of rising days in the last n days
# PSYn = (A/n) 
def psy(t, c):
    p = (rlog(c, c.shift(1)) > 0.0).astype(int)
    psy = p.rolling(t).mean()
    return psy

def ma(t, c):
    ma = c.rolling(t).mean()
    return ma


def asy(t, c):
    r = rlog(c, c.shift(1))
    mar = r.rolling(t).mean()
    return mar
