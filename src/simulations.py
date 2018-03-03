# Simulate what an investment following the predictions would have resulted in

def simulate (actual=[], predictions=[], amount=1000.0, threshold=0.2, leverage=1.0):

    result    = amount
    benchmark = amount

    for i in range(len(predictions)):
        pred = predictions[i]
        if (abs(pred) > threshold):

            # we buy bull or bear certs based on prediction
            change_active    = amount * (leverage * pred/pred *actual[i])

            # benchmark against just buying every day 
            change_passive   = amount * actual[i]

            result    = amount + change_active
            benchmark = amount + change_passive

    return result, benchmark
