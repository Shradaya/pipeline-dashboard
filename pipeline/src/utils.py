def query_reader(filepath):
    with open(filepath, 'r') as file:
        sql_query = "".join(file.readlines())
    return sql_query
