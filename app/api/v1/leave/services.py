from ....database import get_conn
from psycopg2.extras import RealDictCursor
from ..utils.sql_query import read_sql_query

def execute_sql_query(query, **kwargs):
    selected_project = kwargs.get('selected_project')
    leave_type = kwargs.get('leave_type')
    department = kwargs.get('department')
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')
    fiscal_year = kwargs.get('fiscal_year')
    query, bind_params = read_sql_query(query,
                                        selected_project = selected_project,
                                        leave_type = leave_type,
                                        department = department,
                                        start_date = start_date,
                                        end_date = end_date,
                                        fiscal_year = fiscal_year)
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, bind_params)
        leaves_per_week_day = cursor.fetchall()
    return leaves_per_week_day