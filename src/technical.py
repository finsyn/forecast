# technical analysis utility functions 
import numpy as np

def rlog(x, y):
    return np.log(x/y) #Log return 

def ma(t, c):
    ma = c.rolling(t).mean()
    return ma

def asy(t, c):
    r = rlog(c, c.shift(1))
    mar = r.rolling(t).mean()
    return mar
