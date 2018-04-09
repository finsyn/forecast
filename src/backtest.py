import numpy as np

res = np.genfromtxt('data/test-output.csv', delimiter=',')
y = res[0]
y_h = res[1]
correct = np.sum(y == y_h)
n_up = np.sum(y == 1.0)
n_down = np.sum(y == 0.0)
print(n_up)
print(n_down)
print(correct)

