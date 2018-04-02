from load import load_features
from extract import query

quotes = query('queries/quotes.sql')
quotes.to_csv('data/quotes.csv')

features = load_features()
features.to_csv('data/training.csv')
