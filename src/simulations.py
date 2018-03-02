# Simulate what an investment following the predictions would have resulted in

def simulate (actual=[], predictions=[], amount=1000.0, threshold=0.2, leverage=1.0):

    for i in range(len(predictions)):
        if (predictions[i] > threshold):
            amount = amount + amount * (leverage * actual[i])

    return amount
