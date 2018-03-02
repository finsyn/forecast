from parse import get_train_data
import pandas as pd
import unittest

mock = [{'feature': 10, 'feature2': 2, 'target': 200},
        {'feature': 11, 'feature2': 2, 'target': 100 },
        {'feature': 1,  'feature2': 0, 'target': 900}]

mock_df = pd.DataFrame(mock)

class TestDataParsing(unittest.TestCase):

    def test_get(self):
        data = get_train_data(mock_df, 'target')

        values = data.values

        self.assertEqual(data['target(t)'].iloc[0]   , 100)
        self.assertEqual(data['target(t)'].iloc[1]   , 900)
        self.assertEqual(data['feature(t-1)'].iloc[0],  10)


if __name__ == '__main__':
    unittest.main()


print(data)
