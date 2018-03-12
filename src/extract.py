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

# quotes = query('queries/quotes.sql')
# quotes.to_csv('data/quotes.csv')

insiders = query('queries/insiders.sql')
insiders.to_csv('data/insiders.csv')

shorts = query('queries/shorts.sql')
shorts.to_csv('data/shorts.csv')
