import pandas_gbq
import json

projectid = "insikt-e1887"

def query_from_file(filename):
    with open(filename, 'r') as file:
        query=file.read()
    return query

def query(filename):
    query_string = query_from_file(filename)
    return pandas_gbq.read_gbq(
            query_string,
            projectid,
            private_key='key.json',
            index_col='date',
            dialect='standard')


