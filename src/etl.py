from load import load_features

features = load_features()
features.to_csv('data/training.csv')
