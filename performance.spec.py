import numpy as np

output = np.array([[0.1, 0.2, 0.9],[0.5,0.1,0.4]])
print(output)
confident = np.dot(np.ones((1, 3)), np.transpose(output > 0.5)).reshape(2).astype(bool)
predictions = np.argmax(output, axis=-1)
print(predictions)
print(confident)
print(predictions[confident])




