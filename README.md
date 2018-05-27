# OMX30 forecasting

An attempt to guess if OMX30 will go up or down tomorrow based on historical patterns.

The model is very simple in order to avoid overfitting and takes the following features as input:

  - up/down for 19 global stock market indexes (including the OMX30 itself) starting from 2012 in trading day frequency

A one layer LSTM model with only one unit is used. To make a prediction it is fed a one year long sequence of the input features. It outputs probabilities for OMX30 going down or up the following day.

## Result
When training on 80% of the data from 2014 and forward up until today it had 60% accuracy on the remaining 20%. Assuming up and down being just as likely that gives a p-value of less than 0.05

![training loss plot](plots/loss.png "training loss")

Keep in mind though that this result hasn't been thoroughly confirmed yet and that the historical patterns of the stock market can very well change in nature in the future of unknowns.


## Usage
My side project [Finsyn](https://app.finsyn.se) currently runs this on GAE in a opt-in alpha :)

![screenshot from finsyn](plots/demo.png "experimental usage")

### IG CFD trading
The model has been used to conduct real trades of OMX30-SEK20 CFD:s on ig.com. 

Unfortunately I have noticed that the opening price I get on IG CFD on market opening
doesn't match what is advertised by Yahoo Finance (which seems to match Nasdaq).

The intraday market direction of the CFD and the actual underlying index seems to be the same only about ~80% of the time the last year.

```
start = datetime(2017, 5, 29)
end = datetime(2018, 5, 25)

IG vs Yahoo/Nasdaq intraday diff direction matches (OMX30)
count      240
unique       2
top       True
freq       200
```

Opening prices during the same timespan differed about 4 points on average with a median of 3.

## Requirements
 - python 2.7 
 - keras, pandas, matplotlib, scikitlearn, docker etc.
 - *training data that hopefully will be made available soon* 

## Development
TBD

## References

- [The calendar effect](https://en.wikipedia.org/wiki/Calendar_effect)
- [Multivariate Time Series Forecasting with LSTMs in Keras](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/) by Jason Brownlee
- [Deep Learning the Stock Market](https://medium.com/@TalPerry/deep-learning-the-stock-market-df853d139e02) by Tal Perry
- [On stock return prediction with LSTM networks](http://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=8911069&fileOId=8911070) by Magnus Hansson

