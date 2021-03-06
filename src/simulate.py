import numpy as np

from simulations import simulate

[ actual, predictions ] = np.genfromtxt('data/test-output.csv', delimiter=',')

n_correct = np.sum(actual == predictions)

days = len(actual)
accuracy = n_correct/days
amount = 10000.0
threshold = 0.001
leverage = 4.0
result, benchmark = simulate(actual, predictions, amount=amount, threshold=threshold, leverage=leverage)

print('accuracy: %s' % accuracy)
print('you start with %s SEK' % amount)
print('you end up with %s SEK %s days later' % (result, days))
print('you would have ended up with %s SEK if you just bought' % benchmark)
