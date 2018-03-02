import numpy as np

def confident_precision (probabilities, correct, confidence=0.9):
    n_samples, n_features = probabilities.shape

    confident = np.dot(
            np.ones((1, n_features)),
            np.transpose(probabilities > confidence)
            ).reshape(n_samples).astype(bool)

    predictions = np.argmax(probabilities, axis=-1)

    confident_y    = correct[confident]
    confident_pred = predictions[confident]
    
    return (correct[confident], predictions[confident])



