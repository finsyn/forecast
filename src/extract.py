import pandas_gbq
import json
import os

projectid = "insikt-e1887"
key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'key.json')

def query_from_file(filename):
    with open(filename, 'r') as file:
        query=file.read()
    return query

def query(filename, opt):
    query_string_tmpl = query_from_file(filename)
    query_string = query_string_tmpl.format(**opt)
    return pandas_gbq.read_gbq(
            query_string,
            projectid,
            private_key=key_path,
            index_col='date',
            dialect='standard')
