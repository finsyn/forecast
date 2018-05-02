from load import load_features
from extract import query
from pandas import concat

indexes = query('queries/indexes.sql')
indexes.to_csv('data/indexes.csv')

# groups = query('queries/groups.sql')
# groups.to_csv('data/groups.csv')

# shorts = query('queries/shorts.sql')
# shorts.to_csv('data/shorts.csv')

# insiders = query('queries/insiders.sql')
# insiders.to_csv('data/insiders.csv')

features = load_features()
features.to_csv('data/training.csv')
