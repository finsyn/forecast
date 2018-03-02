import numpy as np

from simulations import simulate

[ actual, predictions ] = np.genfromtxt('data/test-output.csv', delimiter=',')

amount = 10000.0
threshold = 0.005
leverage = 2.0
result = simulate(actual, predictions, amount=amount, threshold=threshold, leverage=leverage)

print('you started with %s SEK' % amount)
print('you finished with %s SEK' % result)
