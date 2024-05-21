from dash import dcc
from dash import html
from app.database import get_conn
import dash_bootstrap_components as dbc
from psycopg2.extras import RealDictCursor, NamedTupleCursor

def get_projects():
    sql = """
        SELECT 
            distinct 
            name as label, 
            name as value
        FROM final.dim_allocations;
    """
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute(sql)
        projects = cursor.fetchall()
    return projects

def get_leave_types():
    sql = """
        SELECT 
            distinct 
            leave_type_name as label, 
            leave_type_name as value
        FROM final.dim_leave_types;
    """
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute(sql)
        types = cursor.fetchall()
    return types

def get_departments():
    sql = """
        SELECT 
            distinct 
            department_name as label, 
            department_name as value
        FROM final.dim_departments;
    """
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute(sql)
        departments = cursor.fetchall()
    return departments

def get_date_range():
    sql = """
        SELECT 
            min(fiscal_start_date) as lower_bound, 
            max(fiscal_end_date) as upper_bound
        FROM final.dim_fiscal;
    """
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory = NamedTupleCursor)
        cursor.execute(sql)
        date_range = cursor.fetchall()
    return date_range


def get_body():
    """Get the body of the layout for our Dash SPA"""

    projects = get_projects()
    leave_types = get_leave_types()
    departments = get_departments()
    date_range = get_date_range()

    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label('Project', htmlFor='projects_dropdown'),
                dcc.Dropdown(
                    options=projects,
                    value=None,
                    placeholder="Select a Project ...",
                    id="projects_dropdown",
                    style={'width': '100%'}  # Set the width to 100%
                )
            ], width=2),
            dbc.Col([
                html.Label('Leave Type', htmlFor='leave_types_dropdown'),
                dcc.Dropdown(
                    options=leave_types,
                    value=None,
                    placeholder="Select a Leave Type ...",
                    id="leave_types_dropdown",
                    style={'width': '100%'}  # Set the width to 100%
                )
            ], width=2),
            dbc.Col([
                html.Label('Department', htmlFor='departments_dropdown'),
                dcc.Dropdown(
                    options=departments,
                    value=None,
                    placeholder="Select a Department ...",
                    id="departments_dropdown",
                    style={'width': '100%'}  # Set the width to 100%
                )
            ], width=2),
            dbc.Col([
                html.Label('Date Range', htmlFor='date_picker'),
                dcc.DatePickerRange(
                    min_date_allowed=date_range[0].lower_bound if date_range else None,
                    max_date_allowed=date_range[0].upper_bound if date_range else None,
                    id="date_picker",
                    style={'width': '100%'}  # Set the width to 100%
                )
            ], width=4)
        ], align='center')
    ])




def get_chart_row():
    """Create a row and column for our Plotly/Dash time series chart"""
    return html.Div([
        dbc.Row([
            dbc.Col(
                id="leave_count_by_weekday",  
                children=[],
                width = 4,
                style={'height': '50px'} 
            ),
            dbc.Col(
                id="leave_applied_approved",  
                children=[],
                width = 6,
                style={'height': '50px'} 
            )
        ]),
        dbc.Row([
            dbc.Col(
                id="third_chart",  
                children=[],
                width = 4,
                style={'height': '50px'} 
            ),
            dbc.Col(
                id="fourth_chart",  
                children=[],
                width = 4,
                style={'height': '50px'} 
            )
        ])
    ])


def layout():
    """Function to get Dash's "HTML" layout"""
    return dbc.Container(
        [
            get_body(), 
            get_chart_row(),
        ]
    )
