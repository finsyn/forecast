# OMX30 Index CFD forecasting

An attempt to guess if OMX30 CFD:s will go up or down tomorrow based on historical patterns.

The model is based on the paper [Predicting the Direction of Stock Market Index Movement Using an Optimized Artificial Neural Network Model] by Mingyue Qiu and Yu Song but uses Keras built
in stochastic gradient descent optimizer instead of the genetic algorithm based one used in the paper.

The model uses a bunch of techinical analysis features from the index as input which is fed to small neural network. It outputs probabilities for OMX30 CFD:s going down or up the following day.

Currently the biggest limitation is that we only have CFD data for one year.

## Result
The test sample that one year of data gives us is currently too small to draw any meaningful conclusions of the model's performance.

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

Altogether this made me move from trying to predict OMX30 to predicting the OMX30 CFD instead.

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
- [Predicting the Direction of Stock Market Index Movement Using an Optimized Artificial Neural Network Model]:https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4873195/
