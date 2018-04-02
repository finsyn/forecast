from pandas_gbq import read_gbq

projectid = "insikt-e1887"

def query_from_file(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile

def query(filename):
    query_string = query_from_file(filename)
    return read_gbq(
            query_string,
            projectid,
            index_col='date',
            dialect='standard')


