from load import load_features

features = load_features()
print(features.head(10))
features.to_csv('data/training.csv')
