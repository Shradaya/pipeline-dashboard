from jinjasql import JinjaSql

def read_sql_query(template, **kwargs):
    jinjasql = JinjaSql(param_style='pyformat')
    
    query, bind_params = jinjasql.prepare_query(template, kwargs)

    return query, bind_params